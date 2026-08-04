# 1_pcs_state_growth_model.py

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.linear_model import LinearRegression

# Load dataset
df = pd.read_csv("data/OperationalPC.csv")

# Clean
df = df.dropna()
df = df.sort_values("No. of Operational PCS", ascending=False)

# Create artificial index for modeling
df["Rank"] = range(1, len(df)+1)

X = df[["Rank"]]
y = df["No. of Operational PCS"]

model = LinearRegression()
model.fit(X, y)

os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/pcs_state_growth_model.pkl")

print("PCS state growth model saved!")
