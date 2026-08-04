import pandas as pd
import xgboost as xgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv("data/EV_Predictive_Maintenance_Dataset_15min.csv")

# Drop non-numeric columns
df = df.drop(columns=["Timestamp", "Maintenance_Type"], errors="ignore")

# Remove missing values
df = df.dropna()

# Convert Failure_Probability to Binary Label
df["Failure_Label"] = (df["Failure_Probability"] > 0.5).astype(int)

# Features
X = df.drop(columns=["Failure_Probability", "Failure_Label"])

# Target
y = df["Failure_Label"]

# Scale features (important)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Handle imbalance automatically
model = xgb.XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    scale_pos_weight=(len(y_train) - sum(y_train)) / sum(y_train),
    use_label_encoder=False,
    eval_metric="logloss"
)

model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model & scaler
joblib.dump(model, "xgb_classifier.pkl")
joblib.dump(scaler, "scaler.pkl")

print("✅ Classifier trained and saved successfully!")