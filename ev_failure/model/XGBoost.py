import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier

# Load dataset
df = pd.read_csv("EV_Predictive_Maintenance_Dataset_15min.csv")

df = df.dropna()

# Select features (adjust based on your dataset)
feature_columns = ['voltage', 'current', 'temperature', 'power_load', 'vibration']
feature_columns = [col for col in feature_columns if col in df.columns]

X = df[feature_columns]
y = df['failure']  # change if needed

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# XGBoost Model
model = XGBClassifier(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=6,
    random_state=42
)

model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:,1]

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save model
import joblib
joblib.dump(model, "xgboost_failure_model.pkl")