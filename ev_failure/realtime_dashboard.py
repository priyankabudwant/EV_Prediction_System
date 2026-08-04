import streamlit as st
import pandas as pd
import numpy as np
import joblib
import torch
import torch.nn as nn
import time
import seaborn as sns
import matplotlib.pyplot as plt
from model.attention_cnn_lstm import CNN_LSTM_Attention
import shap


# =========================
# LOAD MODELS
# =========================

xgb_model = joblib.load("xgb_classifier.pkl")
xgb_scaler = joblib.load("scaler.pkl")

lstm_X_scaler = joblib.load("lstm_X_scaler.pkl")
lstm_y_scaler = joblib.load("lstm_y_scaler.pkl")

# =========================
# CNN-LSTM MODEL
# =========================

# -------------------------------
# Load Normal CNN-LSTM
# -------------------------------

class CNN_LSTM(nn.Module):
    def __init__(self):
        super().__init__()
        self.cnn = nn.Conv1d(5, 32, kernel_size=3)
        self.lstm = nn.LSTM(32, 64, batch_first=True)
        self.fc = nn.Linear(64, 1)

    def forward(self, x):
        x = x.permute(0,2,1)
        x = torch.relu(self.cnn(x))
        x = x.permute(0,2,1)
        x,_ = self.lstm(x)
        return self.fc(x[:, -1, :])

cnn_model = CNN_LSTM()
cnn_model.load_state_dict(torch.load("cnn_lstm_model.pth", map_location="cpu"))
cnn_model.eval()

model = CNN_LSTM_Attention()
model.load_state_dict(torch.load("attention_lstm_model.pth", map_location="cpu"))
model.eval()

feature_scaler = joblib.load("attention_feature_scaler.pkl")
target_scaler = joblib.load("attention_target_scaler.pkl")



# =========================
# LOAD DATASET
# =========================

df = pd.read_csv("data/EV_Predictive_Maintenance_Dataset_15min.csv")
df = df.drop(columns=["Timestamp", "Maintenance_Type"], errors="ignore")
df = df.dropna()

feature_cols = df.drop(columns=["Failure_Probability"]).columns

# =========================
# HELPER FUNCTIONS
# =========================

def predict_failure(X):
    X_scaled = xgb_scaler.transform(X)
    return xgb_model.predict_proba(X_scaled)[:, 1]


def predict_rul(sequence_df):
    seq_features = [
        "Battery_Temperature",
        "Motor_Temperature",
        "Motor_Vibration",
        "SoH",
        "Power_Consumption"
    ]

    scaled = lstm_X_scaler.transform(sequence_df[seq_features])
    seq = torch.tensor(scaled[np.newaxis, :, :], dtype=torch.float32)

    with torch.no_grad():
        pred_scaled = model(seq)

    # 🔥 Inverse transform RUL
    pred_actual = lstm_y_scaler.inverse_transform(
        pred_scaled.numpy()
    )

    return float(pred_actual[0][0])

def predict_cnn_rul(sequence):

    seq_features = [
        "Battery_Temperature",
        "Motor_Temperature",
        "Motor_Vibration",
        "SoH",
        "Power_Consumption"
    ]

    scaled = lstm_X_scaler.transform(sequence[seq_features])
    tensor = torch.tensor([scaled], dtype=torch.float32)

    with torch.no_grad():
        pred_scaled = cnn_model(tensor)

    rul = lstm_y_scaler.inverse_transform(pred_scaled.numpy())

    return float(rul[0][0])

def predict_attention_rul(sequence):

    scaled = feature_scaler.transform(sequence)
    tensor = torch.tensor([scaled], dtype=torch.float32)

    with torch.no_grad():
        prediction, attn_weights = model(tensor, return_attention=True)

    rul = target_scaler.inverse_transform(prediction.numpy())

    return rul[0][0], attn_weights.squeeze().numpy()








def monte_carlo(prob):
    sims = np.random.normal(prob, 0.05, 500)
    sims = np.clip(sims, 0, 1)
    return np.mean(sims > 0.7)


def recommend(prob, rul):
    if prob > 0.8 or rul < 20:
        return "🔴 Immediate Maintenance Required"
    elif prob > 0.5:
        return "🟠 Schedule Maintenance Soon"
    else:
        return "🟢 Operating Normally"


def classify_dynamic(preds):
    high = np.percentile(preds, 80)
    med = np.percentile(preds, 50)

    def level(x):
        if x >= high:
            return "🔴 High"
        elif x >= med:
            return "🟠 Medium"
        else:
            return "🟢 Low"

    return [level(p) for p in preds]



#autoencoder

auto_scaler = joblib.load("autoencoder_scaler.pkl")

class AutoEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(5, 32),
            nn.ReLU(),
            nn.Linear(32, 8)
        )
        self.decoder = nn.Sequential(
            nn.Linear(8, 32),
            nn.ReLU(),
            nn.Linear(32, 5)
        )

    def forward(self, x):
        return self.decoder(self.encoder(x))

auto_model = AutoEncoder()
auto_model.load_state_dict(torch.load("autoencoder_model.pth", map_location="cpu"))
auto_model.eval()

def detect_anomaly(X_live):

    auto_features = [
        "Battery_Temperature",
        "Motor_Temperature",
        "Motor_Vibration",
        "SoH",
        "Power_Consumption"
    ]

    X_subset = X_live[auto_features]

    scaled = auto_scaler.transform(X_subset)
    tensor = torch.tensor(scaled, dtype=torch.float32)

    with torch.no_grad():
        reconstruction = auto_model(tensor)

    error = torch.mean((tensor - reconstruction) ** 2, dim=1)

    return error.numpy()


def calculate_health_score(prob, anomaly_score, rul):

    # Convert everything into penalty values
    risk_penalty = prob * 50          # max 50 points
    anomaly_penalty = anomaly_score * 100  # scaled
    rul_penalty = max(0, (50 - rul)) * 0.5  # penalize low RUL

    score = 100 - (risk_penalty + anomaly_penalty + rul_penalty)

    # Keep score between 0–100
    score = max(0, min(100, score))

    return int(score)

#shap

explainer = shap.TreeExplainer(xgb_model)
xgb_model = joblib.load("xgb_classifier.pkl")

def explain_failure(X_row):

    shap_values = explainer.shap_values(X_row)

    contributions = shap_values[0]
    feature_names = X_row.columns

    explanation = []

    for feature, value in zip(feature_names, contributions):

        if abs(value) > 0.02:   # ignore tiny impacts

            percent = int(round(abs(value) * 100))

            if value > 0:
                explanation.append(
                    f"High {feature.replace('_',' ')} (+{percent}%)"
                )
            else:
                explanation.append(
                    f"Low {feature.replace('_',' ')} (+{percent}%)"
                )
        

    return explanation

def generate_trend_summary(history_df):

    summary = []

    trend_features = [
        "Battery_Temperature",
        "Motor_Temperature",
        "Motor_Vibration",
        "SoH"
    ]

    for feature in trend_features:

        if len(history_df) > 1:

            change = history_df[feature].iloc[-1] - history_df[feature].iloc[0]

            change = round(change, 2)

            if change > 0:
                summary.append(f"{feature.replace('_',' ')} increased by {change}")
            elif change < 0:
                summary.append(f"{feature.replace('_',' ')} decreased by {abs(change)}")
            else:
                summary.append(f"{feature.replace('_',' ')} stable")

    return summary


def estimate_cost(prob, rul):
    base_cost = 10000

    risk_factor = prob * 20000
    urgency_factor = max(0, (50 - rul)) * 200

    estimated = base_cost + risk_factor + urgency_factor
    delayed = estimated * 1.5

    return int(estimated), int(delayed)


# =========================
# STREAMLIT UI
# =========================

st.title("🚗 Explainable AI-Based Real-Time EV Fleet Predictive Maintenance System")

fleet_size = st.slider("Select Fleet Size", 3, 15, 5)

if st.button("Start Real-Time Monitoring"):

    placeholder = st.empty()

    for cycle in range(15):

        with placeholder.container():

            st.subheader(f"🔄 Live Cycle {cycle+1}")

            sample = df.sample(fleet_size)

            X_live = sample[feature_cols]
            preds = predict_failure(X_live)

            sample["Failure_Probability"] = preds
            sample["Risk_Level"] = classify_dynamic(preds)


            ranked = sample.sort_values(
                by="Failure_Probability",
                ascending=False
            )
            top_vehicle_index = ranked.index[0]

            history_window = 30  # last 30 records

            vehicle_history = df.iloc[
                max(0, top_vehicle_index - history_window): top_vehicle_index
            ]


            # Fleet Ranking
            st.write("### 📊 Fleet Risk Ranking")
            st.dataframe(
                ranked[["Failure_Probability", "Risk_Level"]]
            )
            top_vehicle = ranked.iloc[[0]]  # keep as dataframe
            reason_list = explain_failure(top_vehicle[feature_cols])

            st.write("### 📌 Failure Explanation")

            for reason in reason_list[:3]:  # top 3 reasons
                st.write(f"- {reason}")

        
            # Highest Risk Vehicle
            top_prob = ranked.iloc[0]["Failure_Probability"]
            st.write(f"## 🚨 Failure Risk: {round(top_prob*100)}%")


            # Last 10 records for RUL
            seq_features = [
                "Battery_Temperature",
                "Motor_Temperature",
                "Motor_Vibration",
                "SoH",
                "Power_Consumption"
            ]

            sequence = df[seq_features].tail(10)
            predicted_rul = predict_rul(sequence)

            st.metric("🚨 Highest Failure Probability", round(top_prob, 3))
            st.metric("⏳ Predicted RUL (Hours)", round(predicted_rul, 2))

            cost_now, cost_late = estimate_cost(top_prob, predicted_rul)

            if top_prob > 0.8:
                st.error("⚠ Critical Alert: Immediate Action Required")

            st.write("### 💰 Maintenance Cost Analysis")
            st.metric("Estimated Cost Now (₹)", cost_now)
            st.metric("Cost if Delayed (₹)", cost_late)

            trend_summary = generate_trend_summary(vehicle_history)

            st.write("### 📜 Vehicle History Trend Summary")

            for line in trend_summary:
                st.write("- " + line)
                
            st.write("### 📈 Vehicle Historical Trend")

            fig, ax = plt.subplots()

            trend_features = [
                "Battery_Temperature",
                "Motor_Temperature",
                "Motor_Vibration",
                "SoH"
            ]

            for feature in trend_features:
                ax.plot(vehicle_history[feature], label=feature)

            ax.set_title("Vehicle Parameter Trend (Last 30 Records)")
            ax.set_xlabel("Time Step")
            ax.set_ylabel("Value")
            ax.legend()

            st.pyplot(fig)
            plt.close(fig)

            anomaly_scores = detect_anomaly(X_live)
            sample["Anomaly_Score"] = anomaly_scores

            st.write("### 🚨 Anomaly Scores")
            st.dataframe(sample[["Anomaly_Score"]])

            avg_anomaly = np.mean(anomaly_scores)

            health_score = calculate_health_score(
                top_prob,
                avg_anomaly,
                predicted_rul
            )

            st.write("### 💚 Fleet Health Score")

            st.metric(
                label="Overall Fleet Health",
                value=f"{health_score} / 100"
            )

            rul, weights = predict_attention_rul(sequence)
            st.write("### 🔍 Attention Weights Over Time")

            
            

            plt.figure()
            plt.plot(weights)
            plt.title("Attention Weight per Time Step")
            plt.xlabel("Time Step")
            plt.ylabel("Importance")
            st.pyplot(plt)

            cnn_rul = predict_cnn_rul(sequence)
            attention_rul, weights = predict_attention_rul(sequence)

            

            st.write("### 📊 CNN-LSTM vs Attention Comparison")

            import matplotlib.pyplot as plt

            plt.figure()

            models = ["CNN-LSTM", "Attention LSTM"]
            predictions = [cnn_rul, attention_rul]

            plt.bar(models, predictions)
            plt.ylabel("Predicted RUL (Hours)")
            plt.title("Model Comparison")

            st.pyplot(plt)

            # Monte Carlo
            future_risk = monte_carlo(top_prob)
            st.metric("🔮 30-Day Failure Risk", round(future_risk, 3))

            # AI Recommendation
            policy = recommend(top_prob, predicted_rul)
            st.success(f"📋 AI Recommendation: {policy}")

            # -----------------------------
            # DOWNLOAD REPORT BUTTON
            # -----------------------------

            st.write("### 📄 Download Vehicle Report")

            report = f"""
            EV FAILURE REPORT
            -----------------
            Failure Risk: {round(top_prob*100)}%
            Predicted RUL: {round(predicted_rul)} hours
            AI Recommendation: {policy}
            Fleet Health Score: {health_score}/100
            """

            st.download_button(
                label="Download Report",
                data=report,
                file_name="vehicle_report.txt",
                mime="text/plain",
                key=f"download_report_{cycle}"  # dynamic key
            )

            # Heatmap
            st.write("### 🌍 Fleet Risk Heatmap")
            heatmap_data = ranked[["Failure_Probability"]]
            fig, ax = plt.subplots()
            sns.heatmap(
                heatmap_data.T,
                cmap="Reds",
                annot=True,
                ax=ax
            )
            st.pyplot(fig)

            

           

        time.sleep(3)
    
    