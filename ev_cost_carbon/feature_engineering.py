import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("greenvolt_ev_dataset_enhanced.csv")

# -----------------------------
# Basic sanity checks
# -----------------------------
print("Loaded columns:")
print(df.columns.tolist())

# -----------------------------
# Create missing base columns if needed
# -----------------------------
if "annual_distance_km" not in df.columns:
    df["annual_distance_km"] = df["distance_km_per_day"] * df["trip_days_per_year"]

if "ev_energy_used_kwh_per_year" not in df.columns:
    df["ev_energy_used_kwh_per_year"] = (
        df["annual_distance_km"] * df["ev_efficiency_kwh_per_km"]
    )

if "fuel_used_liters_per_year" not in df.columns:
    df["fuel_used_liters_per_year"] = (
        df["annual_distance_km"] / df["fuel_vehicle_mileage_kmpl"]
    )

# -----------------------------
# A. Efficiency features
# -----------------------------
df["fuel_efficiency_cost_per_km"] = (
    df["fuel_cost_rs_per_year"] / df["annual_distance_km"]
)

df["ev_cost_per_km"] = (
    df["ev_cost_rs_per_year"] / df["annual_distance_km"]
)

df["cost_difference_per_km"] = (
    df["fuel_efficiency_cost_per_km"] - df["ev_cost_per_km"]
)

df["fuel_consumption_per_day"] = (
    df["fuel_used_liters_per_year"] / df["trip_days_per_year"]
)

df["energy_consumption_per_day"] = (
    df["ev_energy_used_kwh_per_year"] / df["trip_days_per_year"]
)

# -----------------------------
# B. Financial features
# -----------------------------
df["total_ownership_cost_fuel_5yr"] = (
    (df["fuel_cost_rs_per_year"] + df["annual_maintenance_cost_fuel_rs"]) * 5
    + df["vehicle_purchase_cost_fuel_rs"]
)

df["total_ownership_cost_ev_5yr"] = (
    (df["ev_cost_rs_per_year"] + df["annual_maintenance_cost_ev_rs"]) * 5
    + df["vehicle_purchase_cost_ev_rs"]
    - df["subsidy_amount_rs"]
    - df["road_tax_savings_rs"]
)

df["net_savings_5yr"] = (
    df["total_ownership_cost_fuel_5yr"] - df["total_ownership_cost_ev_5yr"]
)

df["roi_percentage"] = np.where(
    df["vehicle_purchase_cost_ev_rs"] > 0,
    (df["net_savings_5yr"] / df["vehicle_purchase_cost_ev_rs"]) * 100,
    0
)

df["monthly_savings_rs"] = df["cost_savings_rs_per_year"] / 12

# -----------------------------
# C. Environmental features
# -----------------------------
df["carbon_reduction_per_km"] = np.where(
    df["annual_distance_km"] > 0,
    df["carbon_reduction_kg_per_year"] / df["annual_distance_km"],
    0
)

df["carbon_reduction_per_day"] = np.where(
    df["trip_days_per_year"] > 0,
    df["carbon_reduction_kg_per_year"] / df["trip_days_per_year"],
    0
)

df["lifetime_carbon_savings"] = df["carbon_reduction_kg_per_year"] * 10

max_carbon = df["carbon_reduction_kg_per_year"].max()
df["eco_score"] = np.where(
    max_carbon > 0,
    (df["carbon_reduction_kg_per_year"] / max_carbon) * 100,
    0
)

# -----------------------------
# D. Charging behavior features
# -----------------------------
df["effective_electricity_price"] = (
    df["home_charging_ratio"] * df["electricity_price_per_kwh"]
    + df["public_charging_ratio"] * (df["electricity_price_per_kwh"] + 2)
)

df["charging_efficiency"] = 0.90

df["charging_loss_kwh"] = (
    df["ev_energy_used_kwh_per_year"] * (1 - df["charging_efficiency"])
)

# -----------------------------
# E. Performance / battery features
# -----------------------------
df["battery_degradation_rate"] = np.where(
    df["vehicle_age_years"] > 0,
    (100 - df["battery_health_percent"]) / df["vehicle_age_years"],
    0
)

df["range_efficiency_score"] = (
    df["battery_health_percent"] / 100
) / df["ev_efficiency_kwh_per_km"]

max_mileage = df["fuel_vehicle_mileage_kmpl"].max()
df["vehicle_efficiency_score"] = np.where(
    max_mileage > 0,
    (df["fuel_vehicle_mileage_kmpl"] / max_mileage) * 100,
    0
)

# -----------------------------
# F. Extra helpful features
# -----------------------------
df["maintenance_savings_rs_per_year"] = (
    df["annual_maintenance_cost_fuel_rs"] - df["annual_maintenance_cost_ev_rs"]
)

df["total_annual_savings_rs"] = (
    df["cost_savings_rs_per_year"] + df["maintenance_savings_rs_per_year"]
)

df["public_charging_cost_penalty"] = (
    df["public_charging_ratio"] * 2 * df["ev_energy_used_kwh_per_year"]
)

df["renewable_adjusted_emission"] = (
    df["ev_emissions_kg_per_year"] * (1 - df["renewable_energy_usage_ratio"])
)

# -----------------------------
# Replace inf / NaN if any
# -----------------------------
df.replace([np.inf, -np.inf], 0, inplace=True)
df.fillna(0, inplace=True)

# -----------------------------
# Save final dataset
# -----------------------------
df.to_csv("greenvolt_ev_dataset_final.csv", index=False)

print("\nFeature engineering completed successfully.")
print("Saved as: greenvolt_ev_dataset_final.csv")
print("\nNew columns added:")
new_cols = [
    "ev_energy_used_kwh_per_year",
    "fuel_used_liters_per_year",
    "fuel_efficiency_cost_per_km",
    "ev_cost_per_km",
    "cost_difference_per_km",
    "fuel_consumption_per_day",
    "energy_consumption_per_day",
    "total_ownership_cost_fuel_5yr",
    "total_ownership_cost_ev_5yr",
    "net_savings_5yr",
    "roi_percentage",
    "monthly_savings_rs",
    "carbon_reduction_per_km",
    "carbon_reduction_per_day",
    "lifetime_carbon_savings",
    "eco_score",
    "effective_electricity_price",
    "charging_efficiency",
    "charging_loss_kwh",
    "battery_degradation_rate",
    "range_efficiency_score",
    "vehicle_efficiency_score",
    "maintenance_savings_rs_per_year",
    "total_annual_savings_rs",
    "public_charging_cost_penalty",
    "renewable_adjusted_emission",
]
print([c for c in new_cols if c in df.columns])

print("\nPreview:")
print(df.head())