import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load dataset
df = pd.read_csv("greenvolt_ev_dataset_enhanced.csv")


# Encode fuel_type
le = LabelEncoder()
df["fuel_type"] = le.fit_transform(df["fuel_type"])  # petrol/diesel -> 0/1

# Input features
X = df[
    [
        "distance_km_per_day",
        "annual_distance_km",
        "fuel_type",
        "fuel_vehicle_mileage_kmpl",
        "fuel_price_per_liter",
        "ev_efficiency_kwh_per_km",
        "electricity_price_per_kwh",
        "grid_emission_factor",
        "fuel_emission_factor",
    ]
]

# Targets
y_cost = df["cost_savings_rs_per_year"]
y_carbon = df["carbon_reduction_kg_per_year"]

# Split data
X_train, X_test, y_cost_train, y_cost_test = train_test_split(
    X, y_cost, test_size=0.2, random_state=42
)

_, _, y_carbon_train, y_carbon_test = train_test_split(
    X, y_carbon, test_size=0.2, random_state=42
)

# Train cost model
cost_model = RandomForestRegressor(n_estimators=200, random_state=42)
cost_model.fit(X_train, y_cost_train)

# Train carbon model
carbon_model = RandomForestRegressor(n_estimators=200, random_state=42)
carbon_model.fit(X_train, y_carbon_train)

# Predictions
y_cost_pred = cost_model.predict(X_test)
y_carbon_pred = carbon_model.predict(X_test)

# Metrics function
def evaluate_model(name, y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = mse ** 0.5
    r2 = r2_score(y_true, y_pred)

    print(f"\n{name} Model Performance")
    print(f"MAE  : {mae:.2f}")
    print(f"MSE  : {mse:.2f}")
    print(f"RMSE : {rmse:.2f}")
    print(f"R2   : {r2:.4f}")

evaluate_model("Cost Savings", y_cost_test, y_cost_pred)
evaluate_model("Carbon Reduction", y_carbon_test, y_carbon_pred)

# Save models
os.makedirs("model", exist_ok=True)
joblib.dump(cost_model, "model/cost_model.pkl")
joblib.dump(carbon_model, "model/carbon_model.pkl")
joblib.dump(le, "model/label_encoder.pkl")

print("\nModels saved successfully.")