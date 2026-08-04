from fastapi import FastAPI
import pandas as pd
import numpy as np
import joblib
import torch
import torch.nn as nn
from pymongo import MongoClient
import shap
import os
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# =========================
# LOAD MODELS
# =========================


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "xgb_classifier.pkl")

xgb_model = joblib.load(model_path)

xgb_scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))

lstm_X_scaler = joblib.load(os.path.join(BASE_DIR, "lstm_X_scaler.pkl"))

lstm_y_scaler = joblib.load(os.path.join(BASE_DIR, "lstm_y_scaler.pkl"))



explainer = shap.TreeExplainer(xgb_model)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# CNN-LSTM MODEL
# =========================

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

cnn_model.load_state_dict(
    torch.load(os.path.join(BASE_DIR, "cnn_lstm_model.pth"), map_location="cpu")
)

cnn_model.eval()

# =========================
# LOAD DATA
# =========================

df = pd.read_csv(
    os.path.join(BASE_DIR, "data", "EV_Predictive_Maintenance_Dataset_15min.csv")
)
df = df.drop(columns=["Timestamp","Maintenance_Type"], errors="ignore")
df = df.dropna()

feature_cols = df.drop(columns=["Failure_Probability"]).columns

# =========================
# MONGODB CONNECTION
# =========================

client = MongoClient("mongodb+srv://priya:Priya123@cluster0.iaigmsi.mongodb.net/?appName=Cluster0")
db = client["ev_fleet_db"]
collection = db["fleet_data"]

# =========================
# API ENDPOINTS
# =========================

@app.get("/")
def home():
    return {"message": "EV Predictive Maintenance API Running 🚀"}

# 1️⃣ Fleet Data
@app.get("/fleet")
def get_fleet():

    sample = df.sample(5)
    X_live = sample[feature_cols]
    preds = xgb_model.predict_proba(
        xgb_scaler.transform(X_live)
    )[:,1]

    sample["Failure_Probability"] = preds

    result = []

    for i,row in sample.iterrows():

        vehicle = {
            "id": int(i),
            "probability": float(row["Failure_Probability"]),
            "risk": (
                "High" if row["Failure_Probability"] > 0.8
                else "Medium" if row["Failure_Probability"] > 0.5
                else "Low"
            )
        }

        collection.insert_one(vehicle)

        # IMPORTANT FIX 👇
        clean_vehicle = vehicle.copy()
        clean_vehicle.pop("_id", None)

        result.append(clean_vehicle)

    return result


@app.get("/fleet-history")
def fleet_history():

    records = list(collection.find({}, {"_id": 0}))

    return records

# 2️⃣ Top Vehicle
@app.get("/top-vehicle")
def get_top_vehicle():

    sample = df.sample(5)
    X_live = sample[feature_cols]
    preds = xgb_model.predict_proba(
        xgb_scaler.transform(X_live)
    )[:,1]

    sample["Failure_Probability"] = preds
    ranked = sample.sort_values(
        by="Failure_Probability",
        ascending=False
    )

    top = ranked.iloc[0]

    return {
        "probability": float(top["Failure_Probability"]),
        "risk_percent": round(float(top["Failure_Probability"])*100),
    }

@app.get("/fleet-health")
def fleet_health():

    records = list(collection.find({}, {"_id": 0}))

    if not records:
        return {"health_score": 100}

    avg_risk = np.mean([r["probability"] for r in records])
    health_score = round((1 - avg_risk) * 100)

    return {"health_score": health_score}

@app.get("/vehicle-history")
def vehicle_history():

    records = list(collection.find({}, {"_id": 0}))

    return records

@app.get("/shap-analysis")
def shap_analysis():

    sample = df.sample(1)
    X_live = sample[feature_cols]

    shap_values = explainer.shap_values(
        xgb_scaler.transform(X_live)
    )

    feature_importance = {}

    for i, col in enumerate(feature_cols):
        feature_importance[col] = round(float(shap_values[0][i]), 4)

    return {
        "features": feature_importance
    }
print(df.columns)

@app.get("/vehicle-analysis")
def vehicle_analysis():
    vehicle = df.sample(1)

    vehicle_df = df.copy()

    if vehicle_df.empty:
        return {"error": "Dataset empty"}

    # =============================
    # 1️⃣ Correct Features
    # =============================

    XGB_FEATURES = list(xgb_scaler.feature_names_in_)
    LSTM_FEATURES = list(lstm_X_scaler.feature_names_in_)

    # =============================
    # 2️⃣ Failure Probability (XGBoost)
    # =============================

    latest = vehicle_df.tail(1)

    X_xgb = latest[XGB_FEATURES]
    X_xgb_scaled = xgb_scaler.transform(X_xgb)

    failure_prob = float(
        xgb_model.predict_proba(X_xgb_scaled)[0][1]
    )

    # -------------------------
    # Failure Prediction
    # -------------------------

    features = xgb_scaler.feature_names_in_

    X = vehicle[features]

    prob = xgb_model.predict_proba(
        xgb_scaler.transform(X)
    )[0][1]

    failure_percent = round(prob*100)

    # =============================
    # 3️⃣ RUL Prediction (CNN-LSTM)
    # =============================

    seq_len = 10

    if len(vehicle_df) < seq_len:
        return {"error": "Not enough data for LSTM"}

    X_lstm = vehicle_df[LSTM_FEATURES].tail(seq_len)

    seq_scaled = lstm_X_scaler.transform(X_lstm)
    seq_scaled = seq_scaled.reshape(1, seq_len, len(LSTM_FEATURES))

    seq_tensor = torch.tensor(seq_scaled, dtype=torch.float32)

    with torch.no_grad():
        predicted_rul = cnn_model(seq_tensor).item()

    # =============================
    # 4️⃣ Maintenance Cost
    # =============================

    base_cost = 20000

    cost_now = int(base_cost * failure_prob)
    cost_delayed = int(cost_now * 1.5)

    # -------------------------
    # Vehicle Health Score
    # -------------------------

    battery_health = float(vehicle["SoH"].values[0] * 100)

    motor_health = 100 - abs(vehicle["Motor_Vibration"].values[0] * 10)

    brake_health = 100 - vehicle["Brake_Pad_Wear"].values[0]

    overall_health = round(
        (battery_health + motor_health + brake_health)/3
    )

    # =============================
    # 5️⃣ Trend Summary
    # =============================

    trend_summary = {}

    for col in [
        "Battery_Temperature",
        "Motor_Temperature",
        "Motor_Vibration",
        "SoH"
    ]:
        if col in vehicle_df.columns:

            change = vehicle_df[col].iloc[-1] - vehicle_df[col].iloc[0]

            trend_summary[col] = round(float(change), 2)

    # -------------------------
    # Range Prediction
    # -------------------------

    soc = vehicle["SoC"].values[0]

    range_km = int(soc * 3)

    # -------------------------
    # Charging Advice
    # -------------------------

    if soc < 20:
        charging_advice = "Charge Immediately"
    elif soc < 40:
        charging_advice = "Charging Recommended Soon"
    else:
        charging_advice = "Battery Level Normal"

    # -------------------------
    # Component Risk
    # -------------------------

    component_risk = {

        "battery":
        "High" if vehicle["SoH"].values[0] < 0.6 else "Low",

        "motor":
        "High" if vehicle["Motor_Temperature"].values[0] > 80 else "Low",

        "brake":
        "High" if vehicle["Brake_Pad_Wear"].values[0] > 70 else "Low"
    }

    # -------------------------
    # Maintenance Recommendation
    # -------------------------

    recommendations = []

    if component_risk["battery"]=="High":
        recommendations.append("Battery inspection required")

    if component_risk["motor"]=="High":
        recommendations.append("Motor cooling system check")

    if component_risk["brake"]=="High":
        recommendations.append("Replace brake pads")

    if len(recommendations)==0:
        recommendations.append("Vehicle operating normally")

    # -------------------------
    # Trend Summary
    # -------------------------

    trend_summary = {}

    for col in [
        "Battery_Temperature",
        "Motor_Temperature",
        "Motor_Vibration",
        "SoH"
    ]:

        change = df[col].iloc[-1] - df[col].iloc[-20]

        trend_summary[col] = round(float(change),2)

    # -------------------------
    # Alerts
    # -------------------------

    alerts = []

    if vehicle["Battery_Temperature"].values[0] > 60:
        alerts.append("Battery temperature high")

    if vehicle["Motor_Vibration"].values[0] > 5:
        alerts.append("Motor vibration abnormal")

    if vehicle["Brake_Pad_Wear"].values[0] > 80:
        alerts.append("Brake wear critical")



    # =============================
    # 6️⃣ Final Response
    # =============================

    return {
        "failure_probability": round(failure_prob, 3),
        "predicted_rul_hours": round(predicted_rul, 2),
        "maintenance_cost_now": cost_now,
        "maintenance_cost_if_delayed": cost_delayed,
        "trend_summary": trend_summary,
       
        "failure_risk_percent": failure_percent,
        "maintenance_cost":{

            "cost_now":cost_now,
            "cost_delayed":cost_delayed
        },

        

        "vehicle_health":{

            "battery_health":round(battery_health),
            "motor_health":round(motor_health),
            "brake_health":round(brake_health),
            "overall_health":overall_health
        },

        "range_prediction":range_km,

        "charging_advice":charging_advice,

        "component_risk":component_risk,

        "recommendations":recommendations,

        "trend_summary":trend_summary,

        "alerts":alerts
    }

