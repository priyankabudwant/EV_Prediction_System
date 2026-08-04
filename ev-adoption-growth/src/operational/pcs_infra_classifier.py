# 4_pcs_infra_classifier.py

import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
import os

df = pd.read_csv("data/OperationalPC.csv")

# Define thresholds
high = df["No. of Operational PCS"].quantile(0.75)
low = df["No. of Operational PCS"].quantile(0.25)

def classify(x):
    if x >= high:
        return 2  # High
    elif x <= low:
        return 0  # Low
    else:
        return 1  # Medium

df["Category"] = df["No. of Operational PCS"].apply(classify)

X = df[["No. of Operational PCS"]]
y = df["Category"]

model = RandomForestClassifier()
model.fit(X, y)

os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/pcs_infra_classifier.pkl")

print("Infrastructure classifier saved!")
