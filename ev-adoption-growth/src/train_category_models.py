import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import os

# Load dataset
df = pd.read_csv("data/ev_cat_01-24.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Convert Date column
df['Date'] = pd.to_datetime(df['Date'])

# Extract Year
df['Year'] = df['Date'].dt.year

# Group yearly
yearly = df.groupby("Year").sum(numeric_only=True).reset_index()

# Get vehicle categories
categories = yearly.columns.drop("Year")

models = {}

for col in categories:

    # Replace negative values with 0
    yearly[col] = yearly[col].clip(lower=0)

    # Replace NaN with 0
    yearly[col] = yearly[col].fillna(0)

    # If all values are zero, skip category
    if yearly[col].sum() == 0:
        print(f"⚠ Skipping {col} (all zero values)")
        continue

    X = yearly[['Year']].values

    # ✅ Use log1p instead of log
    y = np.log1p(yearly[col].values)

    # Extra safety: remove inf if any
    if np.isinf(y).any():
        print(f"⚠ Skipping {col} due to infinity values")
        continue

    model = LinearRegression()
    model.fit(X, y)

    models[col] = model
    print(f"✅ Trained model for {col}")

# Create models folder
os.makedirs("models", exist_ok=True)

# Save models
joblib.dump(models, "models/category_future_model1.pkl")

print("\n🎯 All valid models trained and saved successfully!")
