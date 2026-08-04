import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor

# Load dataset
df = pd.read_csv("greenvolt_ev_dataset_final.csv")

# Encode categorical
le_fuel = LabelEncoder()
le_vehicle = LabelEncoder()

df["fuel_type"] = le_fuel.fit_transform(df["fuel_type"])
df["vehicle_type"] = le_vehicle.fit_transform(df["vehicle_type"])

# =========================
# FEATURES (advanced)
# =========================
features = [
    "distance_km_per_day",
    "annual_distance_km",
    "fuel_type",
    "vehicle_type",
    "vehicle_age_years",
    "fuel_vehicle_mileage_kmpl",
    "fuel_price_per_liter",
    "ev_efficiency_kwh_per_km",
    "battery_health_percent",
    "electricity_price_per_kwh",
    "home_charging_ratio",
    "annual_maintenance_cost_ev_rs",
    "annual_maintenance_cost_fuel_rs",
    "subsidy_amount_rs",
    "grid_emission_factor",

    # NEW FEATURES
    "fuel_efficiency_cost_per_km",
    "ev_cost_per_km",
    "monthly_savings_rs",
    "eco_score",
    "battery_degradation_rate"
]

X = df[features]

# Targets
y_cost = df["cost_savings_rs_per_year"]
y_carbon = df["carbon_reduction_kg_per_year"]

# Split
X_train, X_test, y_cost_train, y_cost_test = train_test_split(
    X, y_cost, test_size=0.2, random_state=42
)

_, _, y_carbon_train, y_carbon_test = train_test_split(
    X, y_carbon, test_size=0.2, random_state=42
)

# Models
cost_model = RandomForestRegressor(n_estimators=300, max_depth=15)
carbon_model = RandomForestRegressor(n_estimators=300, max_depth=15)

cost_model.fit(X_train, y_cost_train)
carbon_model.fit(X_train, y_carbon_train)

# Save models
os.makedirs("model", exist_ok=True)
joblib.dump(cost_model, "model/cost_model_adv.pkl")
joblib.dump(carbon_model, "model/carbon_model_adv.pkl")
joblib.dump(le_fuel, "model/fuel_encoder.pkl")
joblib.dump(le_vehicle, "model/vehicle_encoder.pkl")

print("✅ Advanced models trained and saved")