import pandas as pd
import numpy as np

np.random.seed(42)

# Load your current dataset
df = pd.read_csv("greenvolt_ev_dataset_final.csv")

# -----------------------------
# Base safety columns
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
# 1. Smart temporal features
# -----------------------------
df["year"] = np.random.choice([2024, 2025, 2026], size=len(df))
df["month"] = np.random.randint(1, 13, size=len(df))

def get_season(month):
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "summer"
    elif month in [6, 7, 8, 9]:
        return "monsoon"
    return "autumn"

df["season"] = df["month"].apply(get_season)
df["weekday_travel_ratio"] = np.round(np.random.uniform(0.6, 0.9, len(df)), 2)
df["peak_hour_ratio"] = np.round(np.random.uniform(0.2, 0.7, len(df)), 2)

# -----------------------------
# 2. Battery & degradation features
# -----------------------------
df["charging_cycles_per_year"] = np.round(
    df["ev_energy_used_kwh_per_year"] / df["battery_capacity_kwh"], 0
)

df["depth_of_discharge"] = np.round(np.random.uniform(0.5, 0.95, len(df)), 2)
df["battery_temperature"] = np.round(np.random.uniform(25, 45, len(df)), 2)

df["battery_health_trend"] = np.round(
    (100 - df["battery_health_percent"]) / np.maximum(df["vehicle_age_years"], 1), 2
)

df["remaining_useful_life"] = np.round(
    (df["battery_health_percent"] / 100) * np.random.uniform(5, 10, len(df)), 2
)

df["battery_stress_score"] = np.round(
    (df["battery_temperature"] * 0.4)
    + (df["depth_of_discharge"] * 100 * 0.3)
    + (df["fast_charging_ratio"] * 100 * 0.3),
    2
)

df["battery_efficiency_drop"] = np.round(
    ((100 - df["battery_health_percent"]) / 100) * df["ev_efficiency_kwh_per_km"],
    4
)

# -----------------------------
# 3. Driver behavior features
# -----------------------------
df["driving_style"] = np.random.choice(
    ["eco", "normal", "aggressive"], size=len(df), p=[0.3, 0.5, 0.2]
)

df["speed_variation_index"] = np.round(np.random.uniform(0.1, 0.9, len(df)), 2)
df["braking_frequency"] = np.random.randint(5, 40, len(df))
df["idle_time_ratio"] = np.round(np.random.uniform(0.05, 0.25, len(df)), 2)

df["route_type"] = np.random.choice(
    ["urban", "highway", "mixed"], size=len(df), p=[0.4, 0.2, 0.4]
)

style_score_map = {"eco": 90, "normal": 70, "aggressive": 45}
df["driving_efficiency_score"] = (
    df["driving_style"].map(style_score_map)
    - df["speed_variation_index"] * 10
    - df["idle_time_ratio"] * 20
    - df["braking_frequency"] * 0.3
).round(2)

# -----------------------------
# 4. Geo & location features
# -----------------------------
cities = ["Bengaluru", "Mumbai", "Delhi", "Chennai", "Hyderabad", "Pune"]
regions = {
    "Bengaluru": "South",
    "Mumbai": "West",
    "Delhi": "North",
    "Chennai": "South",
    "Hyderabad": "South",
    "Pune": "West",
}

df["city"] = np.random.choice(cities, size=len(df))
df["region"] = df["city"].map(regions)
df["population_density"] = np.random.randint(2000, 15000, len(df))
df["charging_station_density"] = np.round(np.random.uniform(1, 15, len(df)), 2)
df["avg_temperature"] = np.round(np.random.uniform(18, 40, len(df)), 2)
df["elevation"] = np.round(np.random.uniform(10, 950, len(df)), 2)

df["charging_accessibility_score"] = np.round(
    (df["charging_station_density"] * 5) - (df["population_density"] / 5000),
    2
)

region_score_map = {"North": 65, "South": 80, "West": 75}
df["region_ev_adoption_score"] = df["region"].map(region_score_map)

# -----------------------------
# 5. Charging infrastructure features
# -----------------------------
df["charging_station_distance_km"] = np.round(np.random.uniform(0.5, 10, len(df)), 2)
df["avg_wait_time_at_station"] = np.round(np.random.uniform(5, 45, len(df)), 2)
df["charging_cost_variation"] = np.round(np.random.uniform(0.5, 3, len(df)), 2)

df["fast_charging_frequency"] = np.round(
    df["fast_charging_ratio"] * np.random.uniform(20, 80, len(df)),
    2
)

df["grid_stability_index"] = np.round(np.random.uniform(70, 100, len(df)), 2)

df["charging_convenience_score"] = np.round(
    100
    - (df["charging_station_distance_km"] * 4)
    - (df["avg_wait_time_at_station"] * 0.8)
    + (df["grid_stability_index"] * 0.2),
    2
)

df["charging_risk_score"] = np.round(
    (df["avg_wait_time_at_station"] * 0.5)
    + (df["charging_station_distance_km"] * 2)
    + ((100 - df["grid_stability_index"]) * 0.7),
    2
)

# -----------------------------
# 6. Financial intelligence features
# -----------------------------
df["inflation_rate"] = np.round(np.random.uniform(4, 8, len(df)), 2)
df["fuel_price_growth_rate"] = np.round(np.random.uniform(3, 10, len(df)), 2)
df["electricity_price_growth_rate"] = np.round(np.random.uniform(2, 7, len(df)), 2)
df["loan_interest_rate"] = np.round(np.random.uniform(7, 13, len(df)), 2)

df["vehicle_resale_value"] = np.round(
    df["vehicle_purchase_cost_ev_rs"] * np.random.uniform(0.35, 0.65, len(df)),
    2
)

df["battery_replacement_cost"] = np.round(
    df["battery_capacity_kwh"] * np.random.uniform(5000, 9000, len(df)),
    2
)

df["total_cost_of_ownership"] = np.round(
    (
        df["vehicle_purchase_cost_ev_rs"]
        + (df["ev_cost_rs_per_year"] * 5)
        + (df["annual_maintenance_cost_ev_rs"] * 5)
        + (df["battery_replacement_cost"] * 0.25)
        - df["subsidy_amount_rs"]
        - df["road_tax_savings_rs"]
        - df["vehicle_resale_value"]
    ),
    2
)

# -----------------------------
# 7. Environmental features
# -----------------------------
df["co2_per_km"] = np.round(
    df["carbon_reduction_kg_per_year"] / np.maximum(df["annual_distance_km"], 1),
    4
)

df["co2_offset_cost"] = np.round(
    df["carbon_reduction_kg_per_year"] * np.random.uniform(0.5, 2.0, len(df)),
    2
)

df["air_pollution_index"] = np.random.randint(40, 180, len(df))
df["green_energy_availability"] = np.round(np.random.uniform(0.1, 0.9, len(df)), 2)
df["carbon_tax_rate"] = np.round(np.random.uniform(0.1, 1.5, len(df)), 2)

df["environmental_impact_score"] = np.round(
    (df["carbon_reduction_kg_per_year"] / df["carbon_reduction_kg_per_year"].max()) * 50
    + (df["green_energy_availability"] * 30)
    + ((200 - df["air_pollution_index"]) / 200 * 20),
    2
)

df["carbon_savings_monetary_value"] = np.round(
    df["carbon_reduction_kg_per_year"] * df["carbon_tax_rate"],
    2
)

# -----------------------------
# 8. Fleet features
# -----------------------------
df["fleet_size"] = np.random.randint(1, 21, len(df))
df["fleet_usage_hours"] = np.round(np.random.uniform(1, 12, len(df)), 2)

df["fleet_energy_consumption"] = np.round(
    df["ev_energy_used_kwh_per_year"] * df["fleet_size"],
    2
)

df["fleet_savings"] = np.round(
    df["cost_savings_rs_per_year"] * df["fleet_size"],
    2
)

df["fleet_emission_reduction"] = np.round(
    df["carbon_reduction_kg_per_year"] * df["fleet_size"],
    2
)

# -----------------------------
# 9. Advanced derived features
# -----------------------------
df["cost_per_km_difference"] = np.round(
    (df["fuel_cost_rs_per_year"] - df["ev_cost_rs_per_year"]) / np.maximum(df["annual_distance_km"], 1),
    4
)

df["energy_cost_ratio"] = np.round(
    df["fuel_cost_rs_per_year"] / np.maximum(df["ev_cost_rs_per_year"], 1),
    4
)

df["fuel_vs_ev_efficiency_ratio"] = np.round(
    df["fuel_vehicle_mileage_kmpl"] / np.maximum(df["ev_efficiency_kwh_per_km"], 0.001),
    2
)

df["maintenance_cost_ratio"] = np.round(
    df["annual_maintenance_cost_fuel_rs"] / np.maximum(df["annual_maintenance_cost_ev_rs"], 1),
    4
)

df["charging_cost_percentage"] = np.round(
    (df["ev_cost_rs_per_year"] / np.maximum(df["total_cost_of_ownership"], 1)) * 100,
    2
)

# -----------------------------
# 10. AI scoring features
# -----------------------------
df["economic_score"] = np.round(
    (
        (df["cost_savings_rs_per_year"] / df["cost_savings_rs_per_year"].max()) * 50
        + (df["net_savings_5yr"] / np.maximum(df["net_savings_5yr"].max(), 1)) * 30
        + (df["maintenance_savings_rs_per_year"] / np.maximum(df["maintenance_savings_rs_per_year"].max(), 1)) * 20
    ),
    2
)

df["environment_score"] = np.round(
    (
        (df["carbon_reduction_kg_per_year"] / df["carbon_reduction_kg_per_year"].max()) * 60
        + (df["green_energy_availability"] * 20)
        + ((100 - np.minimum(df["battery_stress_score"], 100)) * 0.2)
    ),
    2
)

df["overall_ev_benefit_score"] = np.round(
    (df["economic_score"] * 0.4)
    + (df["environment_score"] * 0.4)
    + (df["battery_health_percent"] * 0.2),
    2
)

df["risk_score"] = np.round(
    (df["battery_stress_score"] * 0.35)
    + (df["charging_risk_score"] * 0.35)
    + ((100 - df["battery_health_percent"]) * 0.3),
    2
)

# -----------------------------
# Clean up
# -----------------------------
df.replace([np.inf, -np.inf], 0, inplace=True)
df.fillna(0, inplace=True)

# -----------------------------
# Save
# -----------------------------
df.to_csv("greenvolt_ev_dataset_research.csv", index=False)

print("Advanced feature engineering completed successfully.")
print("Saved file: greenvolt_ev_dataset_research.csv")
print("\nTotal columns:", len(df.columns))
print("\nPreview:")
print(df.head())