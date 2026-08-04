from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

app = FastAPI(title="EV Charging Demand Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3002",
        "http://localhost:3003",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optional model load
# model = joblib.load("model/demand_model.pkl")

# Load city dataset relative to this file so startup works from any cwd.
BASE_DIR = Path(__file__).resolve().parent
city_df = pd.read_csv(BASE_DIR / "city_demand_index.csv")


# -----------------------------
# Input Schema
# -----------------------------
class InputData(BaseModel):
    charger_count: int
    fast_ratio: float
    avg_sessions: int
    occupancy: float
    ev_growth: float
    population_density: int


# -----------------------------
# Root
# -----------------------------
@app.get("/")
def home():
    return {"message": "EV Charging Demand Prediction API is running"}


# -----------------------------
# Predict
# -----------------------------
@app.post("/predict")
def predict(data: InputData):

    results = []

    for _, row in city_df.iterrows():

        # City-side infrastructure
        city_infra = row["charger_count"] * (1 + row["fast_ratio"])
        if city_infra == 0:
            city_infra = 1

        # User-side pressure
        user_pressure = (
            data.avg_sessions * 8 +
            data.occupancy * 200 +
            data.ev_growth * 250 +
            data.population_density * 0.01
        )

        # Compare user demand vs city capacity
        infra_gap = max(0, user_pressure - city_infra)

        # Combine city baseline + user effect
        demand_score = (
            row["ev_growth"] * 300 +
            row["occupancy"] * 250 +
            row["population_density"] * 0.015 +
            data.charger_count * 5 +
            data.fast_ratio * 100 +
            data.avg_sessions * 10 +
            data.occupancy * 180 +
            data.ev_growth * 220 +
            data.population_density * 0.02 +
            infra_gap * 2
        )

        results.append({
            "city": row["city"],
            "score": demand_score,
            "charger_count": int(row["charger_count"]) if pd.notna(row["charger_count"]) else None,
            "fast_ratio": float(row["fast_ratio"]) if pd.notna(row["fast_ratio"]) else None,
            "latitude": float(row["latitude"]),
            "longitude": float(row["longitude"])
        })

    df = pd.DataFrame(results)

    # Normalize score to 0-100
    df["normalized"] = (
        (df["score"] - df["score"].min()) /
        (df["score"].max() - df["score"].min() + 1e-9)
    ) * 100

    # Dynamic classification using score thresholds
    def classify(score):
        if score < 35:
            return "Low"
        elif score < 70:
            return "Medium"
        else:
            return "High"

    df["demand_level"] = df["normalized"].apply(classify)
    df["normalized"] = df["normalized"].round(2)
    df["score"] = df["score"].round(2)

    return {"cities": df.to_dict(orient="records")}
