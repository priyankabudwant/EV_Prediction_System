import pandas as pd
import numpy as np
import joblib
import os

# Load dataset
df = pd.read_csv("data/ev_cat_01-24.csv")

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"])
df["Year"] = df["Date"].dt.year
df = df.drop(columns=["Date"])

yearly = df.groupby("Year").sum()

# Load ALL category models (dictionary)
model_path = "models/category_future_model1.pkl"

if not os.path.exists(model_path):
    print("❌ Model file not found")
    exit()

models = joblib.load(model_path)   # This is a dictionary

future_year = 2035
growth_data = []

for col in yearly.columns:

    # Skip if model not trained for that category
    if col not in models:
        continue

    model = models[col]   # Get individual model

    current_value = yearly[col].iloc[-1]

    # Predict (remember we trained using log1p)
    future_log = model.predict(np.array([[future_year]]))
    future_value = np.expm1(future_log)[0]   # use expm1 not exp

    growth = future_value - current_value

    growth_data.append((col, current_value, future_value, growth))

# Sort by highest growth
growth_data.sort(key=lambda x: x[3], reverse=True)

top5 = growth_data[:5]

print("\n🔥 Top 5 Growing Categories by 2035:\n")

for cat, curr, future, growth in top5:
    print(f"{cat}")
    print(f"Current: {int(curr)}")
    print(f"2035 Prediction: {int(future)}")
    print(f"Growth: {int(growth)}\n")


# --------------------------
# 🌱 CO2 Reduction Estimation
# --------------------------

CO2_PER_VEHICLE = 2.3  # tons/year

print("\n🌱 Estimated CO2 Reduction by 2035:\n")

for cat, curr, future, growth in top5:
    co2_reduction = growth * CO2_PER_VEHICLE
    print(f"{cat} -> {round(co2_reduction,2)} tons CO2 avoided per year")
