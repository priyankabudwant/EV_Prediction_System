import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# =========================================================
# Utility functions
# =========================================================
def evaluate_model(name, y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = mse ** 0.5
    r2 = r2_score(y_true, y_pred)

    print(f"\n{name}")
    print("-" * len(name))
    print(f"MAE  : {mae:.2f}")
    print(f"MSE  : {mse:.2f}")
    print(f"RMSE : {rmse:.2f}")
    print(f"R2   : {r2:.4f}")


def encode_columns(df, categorical_cols):
    encoders = {}
    df_encoded = df.copy()

    for col in categorical_cols:
        le = LabelEncoder()
        df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
        encoders[col] = le

    return df_encoded, encoders


def train_and_save_models(
    df,
    features,
    categorical_cols,
    cost_target,
    carbon_target,
    cost_model_path,
    carbon_model_path,
    encoder_path,
    feature_path,
    model_tag,
):
    print(f"\n==============================")
    print(f"Training {model_tag}")
    print(f"==============================")

    # Encode categorical columns
    df_encoded, encoders = encode_columns(df, categorical_cols)

    # Inputs and targets
    X = df_encoded[features]
    y_cost = df_encoded[cost_target]
    y_carbon = df_encoded[carbon_target]

    # Split once so both models use same rows
    X_train, X_test, y_cost_train, y_cost_test, y_carbon_train, y_carbon_test = train_test_split(
        X, y_cost, y_carbon, test_size=0.2, random_state=42
    )

    # Models
    cost_model = RandomForestRegressor(
        n_estimators=300,
        max_depth=18,
        min_samples_split=4,
        random_state=42,
        n_jobs=-1
    )

    carbon_model = RandomForestRegressor(
        n_estimators=300,
        max_depth=18,
        min_samples_split=4,
        random_state=42,
        n_jobs=-1
    )

    # Train
    cost_model.fit(X_train, y_cost_train)
    carbon_model.fit(X_train, y_carbon_train)

    # Predict
    y_cost_pred = cost_model.predict(X_test)
    y_carbon_pred = carbon_model.predict(X_test)

    # Evaluate
    evaluate_model(f"{model_tag} - Cost Model", y_cost_test, y_cost_pred)
    evaluate_model(f"{model_tag} - Carbon Model", y_carbon_test, y_carbon_pred)

    # Save
    os.makedirs("model", exist_ok=True)
    joblib.dump(cost_model, cost_model_path)
    joblib.dump(carbon_model, carbon_model_path)
    joblib.dump(encoders, encoder_path)
    joblib.dump(features, feature_path)

    print(f"\nSaved {model_tag} models successfully.")
    print(f"Cost model   -> {cost_model_path}")
    print(f"Carbon model -> {carbon_model_path}")
    print(f"Encoders     -> {encoder_path}")
    print(f"Features     -> {feature_path}")


# =========================================================
# 1. BASIC / OLD MODEL
# =========================================================
def train_basic_model():
    basic_file = "greenvolt_ev_dataset_final.csv"

    if not os.path.exists(basic_file):
        print(f"\nBasic dataset not found: {basic_file}")
        return

    df = pd.read_csv(basic_file)

    basic_features = [
        "distance_km_per_day",
        "annual_distance_km",
        "fuel_type",
        "vehicle_type",
        "vehicle_age_years",
        "trip_days_per_year",
        "fuel_vehicle_mileage_kmpl",
        "fuel_price_per_liter",
        "ev_efficiency_kwh_per_km",
        "electricity_price_per_kwh",
        "grid_emission_factor",
        "fuel_emission_factor",
        "battery_health_percent",
        "home_charging_ratio",
        "public_charging_ratio",
        "fast_charging_ratio",
        "renewable_energy_usage_ratio",
        "annual_maintenance_cost_fuel_rs",
        "annual_maintenance_cost_ev_rs",
        "subsidy_amount_rs",
        "road_tax_savings_rs",
        "fuel_cost_rs_per_year",
        "ev_cost_rs_per_year",
        "fuel_efficiency_cost_per_km",
        "ev_cost_per_km",
        "cost_difference_per_km",
        "monthly_savings_rs",
        "eco_score",
        "battery_degradation_rate",
        "vehicle_efficiency_score",
        "maintenance_savings_rs_per_year",
        "total_annual_savings_rs",
    ]

    basic_categorical = [
        "fuel_type",
        "vehicle_type",
    ]

    # keep only columns that actually exist
    basic_features = [col for col in basic_features if col in df.columns]
    basic_categorical = [col for col in basic_categorical if col in df.columns]

    train_and_save_models(
        df=df,
        features=basic_features,
        categorical_cols=basic_categorical,
        cost_target="cost_savings_rs_per_year",
        carbon_target="carbon_reduction_kg_per_year",
        cost_model_path="model/cost_model_basic.pkl",
        carbon_model_path="model/carbon_model_basic.pkl",
        encoder_path="model/basic_encoders.pkl",
        feature_path="model/basic_features.pkl",
        model_tag="BASIC MODEL",
    )


# =========================================================
# 2. RESEARCH / ADVANCED MODEL
# =========================================================
def train_research_model():
    research_file = "greenvolt_ev_dataset_research.csv"

    if not os.path.exists(research_file):
        print(f"\nResearch dataset not found: {research_file}")
        return

    df = pd.read_csv(research_file)

    research_features = [
        "distance_km_per_day",
        "annual_distance_km",
        "fuel_type",
        "fuel_vehicle_mileage_kmpl",
        "fuel_price_per_liter",
        "ev_efficiency_kwh_per_km",
        "electricity_price_per_kwh",
        "grid_emission_factor",
        "fuel_emission_factor",
        "vehicle_type",
        "vehicle_age_years",
        "trip_days_per_year",
        "city_traffic_level",
        "ac_usage_level",
        "highway_ratio",
        "urban_ratio",
        "battery_capacity_kwh",
        "battery_health_percent",
        "home_charging_ratio",
        "public_charging_ratio",
        "fast_charging_ratio",
        "charging_type",
        "renewable_energy_usage_ratio",
        "annual_maintenance_cost_fuel_rs",
        "annual_maintenance_cost_ev_rs",
        "subsidy_amount_rs",
        "road_tax_savings_rs",
        "vehicle_purchase_cost_fuel_rs",
        "vehicle_purchase_cost_ev_rs",
        "payback_period_years",
        "trees_saved_equivalent",
        "environmental_benefit_score",
        "cost_savings_5yr_rs",
        "carbon_reduction_5yr_kg",
        "fuel_efficiency_cost_per_km",
        "ev_cost_per_km",
        "battery_degradation_rate",
        "monthly_savings_rs",
        "eco_score",
        "year",
        "month",
        "season",
        "weekday_travel_ratio",
        "peak_hour_ratio",
        "charging_cycles_per_year",
        "depth_of_discharge",
        "battery_temperature",
        "battery_health_trend",
        "remaining_useful_life",
        "battery_stress_score",
        "battery_efficiency_drop",
        "driving_style",
        "speed_variation_index",
        "braking_frequency",
        "idle_time_ratio",
        "route_type",
        "driving_efficiency_score",
        "city",
        "region",
        "population_density",
        "charging_station_density",
        "avg_temperature",
        "elevation",
        "charging_accessibility_score",
        "region_ev_adoption_score",
        "charging_station_distance_km",
        "avg_wait_time_at_station",
        "charging_cost_variation",
        "fast_charging_frequency",
        "grid_stability_index",
        "charging_convenience_score",
        "charging_risk_score",
        "inflation_rate",
        "fuel_price_growth_rate",
        "electricity_price_growth_rate",
        "loan_interest_rate",
        "vehicle_resale_value",
        "battery_replacement_cost",
        "total_cost_of_ownership",
        "co2_per_km",
        "co2_offset_cost",
        "air_pollution_index",
        "green_energy_availability",
        "carbon_tax_rate",
        "environmental_impact_score",
        "carbon_savings_monetary_value",
        "fleet_size",
        "fleet_usage_hours",
        "fleet_energy_consumption",
        "fleet_savings",
        "fleet_emission_reduction",
        "cost_per_km_difference",
        "energy_cost_ratio",
        "fuel_vs_ev_efficiency_ratio",
        "maintenance_cost_ratio",
        "charging_cost_percentage",
        "economic_score",
        "environment_score",
        "overall_ev_benefit_score",
        "risk_score",
    ]

    research_categorical = [
        "fuel_type",
        "vehicle_type",
        "city_traffic_level",
        "ac_usage_level",
        "charging_type",
        "season",
        "driving_style",
        "route_type",
        "city",
        "region",
    ]

    # keep only columns that actually exist
    research_features = [col for col in research_features if col in df.columns]
    research_categorical = [col for col in research_categorical if col in df.columns]

    train_and_save_models(
        df=df,
        features=research_features,
        categorical_cols=research_categorical,
        cost_target="cost_savings_rs_per_year",
        carbon_target="carbon_reduction_kg_per_year",
        cost_model_path="model/cost_model_research.pkl",
        carbon_model_path="model/carbon_model_research.pkl",
        encoder_path="model/research_encoders.pkl",
        feature_path="model/research_features.pkl",
        model_tag="RESEARCH MODEL",
    )


# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    print("Starting training for both basic and research models...")

    train_basic_model()
    train_research_model()

    print("\nAll available training completed.")