from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import os
import uuid
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import shap

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# =========================================================
# App
# =========================================================
app = FastAPI(title="GreenVolt EV Cost & Carbon API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3001",
        "http://localhost:3004",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# =========================================================
# Load artifacts
# =========================================================
try:
    cost_model_basic = joblib.load(os.path.join(MODEL_DIR, "cost_model_basic.pkl"))
    carbon_model_basic = joblib.load(os.path.join(MODEL_DIR, "carbon_model_basic.pkl"))
    basic_encoders = joblib.load(os.path.join(MODEL_DIR, "basic_encoders.pkl"))
    basic_features = joblib.load(os.path.join(MODEL_DIR, "basic_features.pkl"))
except Exception:
    cost_model_basic = None
    carbon_model_basic = None
    basic_encoders = {}
    basic_features = []

try:
    cost_model_research = joblib.load(os.path.join(MODEL_DIR, "cost_model_research.pkl"))
    carbon_model_research = joblib.load(os.path.join(MODEL_DIR, "carbon_model_research.pkl"))
    research_encoders = joblib.load(os.path.join(MODEL_DIR, "research_encoders.pkl"))
    research_features = joblib.load(os.path.join(MODEL_DIR, "research_features.pkl"))
except Exception:
    cost_model_research = None
    carbon_model_research = None
    research_encoders = {}
    research_features = []

# =========================================================
# Input schema
# =========================================================
class EVInput(BaseModel):
    distance_km_per_day: float
    fuel_type: str
    vehicle_type: str
    vehicle_age_years: float
    trip_days_per_year: float
    fuel_vehicle_mileage_kmpl: float
    fuel_price_per_liter: float
    ev_efficiency_kwh_per_km: float
    electricity_price_per_kwh: float
    grid_emission_factor: float
    fuel_emission_factor: float
    battery_health_percent: float
    home_charging_ratio: float
    public_charging_ratio: float
    fast_charging_ratio: float = 0.3
    renewable_energy_usage_ratio: float = 0.2
    annual_maintenance_cost_ev_rs: float
    annual_maintenance_cost_fuel_rs: float
    subsidy_amount_rs: float
    road_tax_savings_rs: float = 0
    battery_capacity_kwh: float = 40
    city_traffic_level: str = "medium"
    ac_usage_level: str = "medium"
    charging_type: str = "fast"
    highway_ratio: float = 0.4
    urban_ratio: float = 0.6
    vehicle_purchase_cost_fuel_rs: float = 900000
    vehicle_purchase_cost_ev_rs: float = 1400000

# =========================================================
# Helper functions
# =========================================================
def safe_encode(value, encoder, field_name):
    raw = str(value).strip().lower()
    known = [str(x).strip().lower() for x in encoder.classes_]

    if raw not in known:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid {field_name}: '{value}'. Allowed values: {list(encoder.classes_)}",
        )

    original = encoder.classes_[known.index(raw)]
    return encoder.transform([original])[0]


def get_encoder_value(encoders, col_name, value):
    if col_name not in encoders:
        return value
    return safe_encode(value, encoders[col_name], col_name)


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def add_common_features(data: EVInput):
    annual_distance_km = data.distance_km_per_day * data.trip_days_per_year

    fuel_used_liters_per_year = annual_distance_km / max(data.fuel_vehicle_mileage_kmpl, 0.001)
    fuel_cost_rs_per_year = fuel_used_liters_per_year * data.fuel_price_per_liter
    fuel_emissions_kg_per_year = fuel_used_liters_per_year * data.fuel_emission_factor

    ev_energy_used_kwh_per_year = annual_distance_km * data.ev_efficiency_kwh_per_km
    ev_cost_rs_per_year = ev_energy_used_kwh_per_year * data.electricity_price_per_kwh
    ev_emissions_kg_per_year = ev_energy_used_kwh_per_year * data.grid_emission_factor

    cost_savings_rs_per_year = fuel_cost_rs_per_year - ev_cost_rs_per_year
    carbon_reduction_kg_per_year = fuel_emissions_kg_per_year - ev_emissions_kg_per_year

    fuel_efficiency_cost_per_km = fuel_cost_rs_per_year / max(annual_distance_km, 1)
    ev_cost_per_km = ev_cost_rs_per_year / max(annual_distance_km, 1)
    cost_difference_per_km = fuel_efficiency_cost_per_km - ev_cost_per_km

    monthly_savings_rs = cost_savings_rs_per_year / 12
    battery_degradation_rate = (100 - data.battery_health_percent) / max(data.vehicle_age_years, 1)

    eco_score = clamp((carbon_reduction_kg_per_year / 2000) * 100, 0, 100)
    vehicle_efficiency_score = clamp((data.fuel_vehicle_mileage_kmpl / 25) * 100, 0, 100)

    maintenance_savings_rs_per_year = (
        data.annual_maintenance_cost_fuel_rs - data.annual_maintenance_cost_ev_rs
    )
    total_annual_savings_rs = cost_savings_rs_per_year + maintenance_savings_rs_per_year

    payback_period_years = (
        max(data.vehicle_purchase_cost_ev_rs - data.vehicle_purchase_cost_fuel_rs - data.subsidy_amount_rs, 0)
        / max(total_annual_savings_rs, 1)
    )
    trees_saved_equivalent = max(carbon_reduction_kg_per_year, 0) / 21
    environmental_benefit_score = clamp(
        (carbon_reduction_kg_per_year / 2000) * 70 + data.renewable_energy_usage_ratio * 30,
        0,
        100,
    )
    cost_savings_5yr_rs = cost_savings_rs_per_year * 5
    carbon_reduction_5yr_kg = carbon_reduction_kg_per_year * 5

    return {
        "annual_distance_km": annual_distance_km,
        "fuel_used_liters_per_year": fuel_used_liters_per_year,
        "fuel_cost_rs_per_year": fuel_cost_rs_per_year,
        "fuel_emissions_kg_per_year": fuel_emissions_kg_per_year,
        "ev_energy_used_kwh_per_year": ev_energy_used_kwh_per_year,
        "ev_cost_rs_per_year": ev_cost_rs_per_year,
        "ev_emissions_kg_per_year": ev_emissions_kg_per_year,
        "cost_savings_rs_per_year": cost_savings_rs_per_year,
        "carbon_reduction_kg_per_year": carbon_reduction_kg_per_year,
        "fuel_efficiency_cost_per_km": fuel_efficiency_cost_per_km,
        "ev_cost_per_km": ev_cost_per_km,
        "cost_difference_per_km": cost_difference_per_km,
        "monthly_savings_rs": monthly_savings_rs,
        "battery_degradation_rate": battery_degradation_rate,
        "eco_score": eco_score,
        "vehicle_efficiency_score": vehicle_efficiency_score,
        "maintenance_savings_rs_per_year": maintenance_savings_rs_per_year,
        "total_annual_savings_rs": total_annual_savings_rs,
        "payback_period_years": payback_period_years,
        "trees_saved_equivalent": trees_saved_equivalent,
        "environmental_benefit_score": environmental_benefit_score,
        "cost_savings_5yr_rs": cost_savings_5yr_rs,
        "carbon_reduction_5yr_kg": carbon_reduction_5yr_kg,
    }


def add_research_features(base_row):
    row = dict(base_row)

    # temporal
    row["year"] = 2026
    row["month"] = 4
    row["season"] = "summer"
    row["weekday_travel_ratio"] = 0.75
    row["peak_hour_ratio"] = 0.45

    # battery
    row["charging_cycles_per_year"] = row["ev_energy_used_kwh_per_year"] / max(row["battery_capacity_kwh"], 1)
    row["depth_of_discharge"] = 0.75
    row["battery_temperature"] = 32.0
    row["battery_health_trend"] = (100 - row["battery_health_percent"]) / max(row["vehicle_age_years"], 1)
    row["remaining_useful_life"] = (row["battery_health_percent"] / 100) * 8
    row["battery_stress_score"] = (
        row["battery_temperature"] * 0.4
        + row["depth_of_discharge"] * 100 * 0.3
        + row["fast_charging_ratio"] * 100 * 0.3
    )
    row["battery_efficiency_drop"] = ((100 - row["battery_health_percent"]) / 100) * row["ev_efficiency_kwh_per_km"]

    # driver behavior
    row["driving_style"] = "normal"
    row["speed_variation_index"] = 0.4
    row["braking_frequency"] = 15
    row["idle_time_ratio"] = 0.1
    row["route_type"] = "mixed"
    row["driving_efficiency_score"] = 72.0

    # location
    row["city"] = "Bengaluru"
    row["region"] = "South"
    row["population_density"] = 8000
    row["charging_station_density"] = 7.5
    row["avg_temperature"] = 29.0
    row["elevation"] = 900
    row["charging_accessibility_score"] = 34.0
    row["region_ev_adoption_score"] = 80

    # charging infra
    row["charging_station_distance_km"] = 2.0
    row["avg_wait_time_at_station"] = 12.0
    row["charging_cost_variation"] = 1.2
    row["fast_charging_frequency"] = row["fast_charging_ratio"] * 40
    row["grid_stability_index"] = 88.0
    row["charging_convenience_score"] = 80.0
    row["charging_risk_score"] = 24.0

    # finance
    row["inflation_rate"] = 5.5
    row["fuel_price_growth_rate"] = 6.5
    row["electricity_price_growth_rate"] = 4.0
    row["loan_interest_rate"] = 9.0
    row["vehicle_resale_value"] = row["vehicle_purchase_cost_ev_rs"] * 0.5
    row["battery_replacement_cost"] = row["battery_capacity_kwh"] * 7000
    row["total_cost_of_ownership"] = (
        row["vehicle_purchase_cost_ev_rs"]
        + row["ev_cost_rs_per_year"] * 5
        + row["annual_maintenance_cost_ev_rs"] * 5
        + row["battery_replacement_cost"] * 0.25
        - row["subsidy_amount_rs"]
        - row["road_tax_savings_rs"]
        - row["vehicle_resale_value"]
    )

    # environment
    row["co2_per_km"] = row["carbon_reduction_kg_per_year"] / max(row["annual_distance_km"], 1)
    row["co2_offset_cost"] = row["carbon_reduction_kg_per_year"] * 1.0
    row["air_pollution_index"] = 95
    row["green_energy_availability"] = 0.45
    row["carbon_tax_rate"] = 0.8
    row["environmental_impact_score"] = 76.0
    row["carbon_savings_monetary_value"] = row["carbon_reduction_kg_per_year"] * row["carbon_tax_rate"]

    # fleet
    row["fleet_size"] = 5
    row["fleet_usage_hours"] = 6.0
    row["fleet_energy_consumption"] = row["ev_energy_used_kwh_per_year"] * row["fleet_size"]
    row["fleet_savings"] = row["cost_savings_rs_per_year"] * row["fleet_size"]
    row["fleet_emission_reduction"] = row["carbon_reduction_kg_per_year"] * row["fleet_size"]

    # derived
    row["cost_per_km_difference"] = row["cost_difference_per_km"]
    row["energy_cost_ratio"] = row["fuel_cost_rs_per_year"] / max(row["ev_cost_rs_per_year"], 1)
    row["fuel_vs_ev_efficiency_ratio"] = row["fuel_vehicle_mileage_kmpl"] / max(row["ev_efficiency_kwh_per_km"], 0.001)
    row["maintenance_cost_ratio"] = row["annual_maintenance_cost_fuel_rs"] / max(row["annual_maintenance_cost_ev_rs"], 1)
    row["charging_cost_percentage"] = row["ev_cost_rs_per_year"] / max(row["total_cost_of_ownership"], 1) * 100

    # scores
    row["economic_score"] = clamp(
        (row["cost_savings_rs_per_year"] / 100000) * 50
        + (row["cost_savings_5yr_rs"] / 500000) * 30
        + (row["maintenance_savings_rs_per_year"] / 20000) * 20,
        0,
        100,
    )
    row["environment_score"] = clamp(
        (row["carbon_reduction_kg_per_year"] / 2000) * 60
        + row["green_energy_availability"] * 20
        + (100 - min(row["battery_stress_score"], 100)) * 0.2,
        0,
        100,
    )
    row["overall_ev_benefit_score"] = (
        row["economic_score"] * 0.4
        + row["environment_score"] * 0.4
        + row["battery_health_percent"] * 0.2
    )
    row["risk_score"] = (
        row["battery_stress_score"] * 0.35
        + row["charging_risk_score"] * 0.35
        + (100 - row["battery_health_percent"]) * 0.3
    )

    return row


def encode_row(row_dict, feature_list, encoders):
    encoded = {}
    for col in feature_list:
        value = row_dict.get(col, 0)

        if col in encoders:
            value = get_encoder_value(encoders, col, value)

        encoded[col] = value

    return pd.DataFrame([encoded], columns=feature_list)


def save_bar_chart(fuel_cost, ev_cost, savings, carbon):
    filename = f"chart_{uuid.uuid4().hex}.png"
    path = os.path.join(STATIC_DIR, filename)

    labels = ["Fuel Cost", "EV Cost", "Savings", "Carbon Reduction"]
    values = [fuel_cost, ev_cost, savings, carbon]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)
    plt.title("EV Cost & Carbon Comparison")
    plt.ylabel("Value")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

    return f"/static/{filename}"


def get_shap_values(model, input_df):
    try:
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(input_df)
        feature_impact = {
            col: float(val) for col, val in zip(input_df.columns, shap_values[0])
        }
        sorted_impacts = sorted(feature_impact.items(), key=lambda x: abs(x[1]), reverse=True)[:5]
        return [{"feature": k, "impact": round(v, 4)} for k, v in sorted_impacts]
    except Exception:
        return []


def build_base_row(data: EVInput):
    common = add_common_features(data)

    row = {
        "distance_km_per_day": data.distance_km_per_day,
        "annual_distance_km": common["annual_distance_km"],
        "fuel_type": data.fuel_type,
        "vehicle_type": data.vehicle_type,
        "vehicle_age_years": data.vehicle_age_years,
        "trip_days_per_year": data.trip_days_per_year,
        "fuel_vehicle_mileage_kmpl": data.fuel_vehicle_mileage_kmpl,
        "fuel_price_per_liter": data.fuel_price_per_liter,
        "ev_efficiency_kwh_per_km": data.ev_efficiency_kwh_per_km,
        "electricity_price_per_kwh": data.electricity_price_per_kwh,
        "grid_emission_factor": data.grid_emission_factor,
        "fuel_emission_factor": data.fuel_emission_factor,
        "battery_health_percent": data.battery_health_percent,
        "home_charging_ratio": data.home_charging_ratio,
        "public_charging_ratio": data.public_charging_ratio,
        "fast_charging_ratio": data.fast_charging_ratio,
        "renewable_energy_usage_ratio": data.renewable_energy_usage_ratio,
        "annual_maintenance_cost_fuel_rs": data.annual_maintenance_cost_fuel_rs,
        "annual_maintenance_cost_ev_rs": data.annual_maintenance_cost_ev_rs,
        "subsidy_amount_rs": data.subsidy_amount_rs,
        "road_tax_savings_rs": data.road_tax_savings_rs,
        "battery_capacity_kwh": data.battery_capacity_kwh,
        "city_traffic_level": data.city_traffic_level,
        "ac_usage_level": data.ac_usage_level,
        "charging_type": data.charging_type,
        "highway_ratio": data.highway_ratio,
        "urban_ratio": data.urban_ratio,
        "vehicle_purchase_cost_fuel_rs": data.vehicle_purchase_cost_fuel_rs,
        "vehicle_purchase_cost_ev_rs": data.vehicle_purchase_cost_ev_rs,
        **common,
    }
    return row

# =========================================================
# Routes
# =========================================================
@app.get("/")
def home():
    return {
        "message": "GreenVolt API running",
        "available_endpoints": [
            "/predict/basic",
            "/predict/research",
            "/model-info",
        ],
    }


@app.get("/model-info")
def model_info():
    basic_encoder_info = {
        k: list(v.classes_) for k, v in basic_encoders.items()
    } if basic_encoders else {}

    research_encoder_info = {
        k: list(v.classes_) for k, v in research_encoders.items()
    } if research_encoders else {}

    return {
        "basic_model_loaded": cost_model_basic is not None and carbon_model_basic is not None,
        "research_model_loaded": cost_model_research is not None and carbon_model_research is not None,
        "basic_features_count": len(basic_features),
        "research_features_count": len(research_features),
        "basic_allowed_categories": basic_encoder_info,
        "research_allowed_categories": research_encoder_info,
    }


@app.post("/predict/basic")
def predict_basic(data: EVInput):
    if cost_model_basic is None or carbon_model_basic is None:
        raise HTTPException(status_code=500, detail="Basic model files not loaded.")

    base_row = build_base_row(data)
    input_df = encode_row(base_row, basic_features, basic_encoders)

    cost_pred = float(cost_model_basic.predict(input_df)[0])
    carbon_pred = float(carbon_model_basic.predict(input_df)[0])

    chart_url = save_bar_chart(
        base_row["fuel_cost_rs_per_year"],
        base_row["ev_cost_rs_per_year"],
        cost_pred,
        carbon_pred,
    )

    return {
        "model_type": "basic",
        "annual_distance_km": round(base_row["annual_distance_km"], 2),
        "fuel_cost_rs_per_year": round(base_row["fuel_cost_rs_per_year"], 2),
        "ev_cost_rs_per_year": round(base_row["ev_cost_rs_per_year"], 2),
        "predicted_cost_savings_rs_per_year": round(cost_pred, 2),
        "predicted_carbon_reduction_kg_per_year": round(carbon_pred, 2),
        "predicted_5yr_savings_rs": round(cost_pred * 5, 2),
        "trees_saved_equivalent": round(max(carbon_pred, 0) / 21, 2),
        "chart_url": chart_url,
        "top_cost_features": get_shap_values(cost_model_basic, input_df),
        "top_carbon_features": get_shap_values(carbon_model_basic, input_df),
    }


@app.post("/predict/research")
def predict_research(data: EVInput):
    if cost_model_research is None or carbon_model_research is None:
        raise HTTPException(status_code=500, detail="Research model files not loaded.")

    base_row = build_base_row(data)
    research_row = add_research_features(base_row)
    input_df = encode_row(research_row, research_features, research_encoders)

    cost_pred = float(cost_model_research.predict(input_df)[0])
    carbon_pred = float(carbon_model_research.predict(input_df)[0])

    chart_url = save_bar_chart(
        research_row["fuel_cost_rs_per_year"],
        research_row["ev_cost_rs_per_year"],
        cost_pred,
        carbon_pred,
    )

    return {
        "model_type": "research",
        "annual_distance_km": round(research_row["annual_distance_km"], 2),
        "fuel_cost_rs_per_year": round(research_row["fuel_cost_rs_per_year"], 2),
        "ev_cost_rs_per_year": round(research_row["ev_cost_rs_per_year"], 2),
        "predicted_cost_savings_rs_per_year": round(cost_pred, 2),
        "predicted_carbon_reduction_kg_per_year": round(carbon_pred, 2),
        "predicted_5yr_savings_rs": round(cost_pred * 5, 2),
        "trees_saved_equivalent": round(max(carbon_pred, 0) / 21, 2),
        "overall_ev_benefit_score": round(research_row["overall_ev_benefit_score"], 2),
        "risk_score": round(research_row["risk_score"], 2),
        "economic_score": round(research_row["economic_score"], 2),
        "environment_score": round(research_row["environment_score"], 2),
        "chart_url": chart_url,
        "top_cost_features": get_shap_values(cost_model_research, input_df),
        "top_carbon_features": get_shap_values(carbon_model_research, input_df),
    }


# =========================================================
# Run directly
# =========================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8002, reload=True)
