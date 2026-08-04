from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import numpy as np

app = FastAPI(title="EV Charging Demand Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3002",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained model (optional now since you're using logic)
model = joblib.load("model/demand_model.pkl")

# Load city dataset
city_df = pd.read_csv("city_demand_index.csv")


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

        base = row["demand_index"]

        city_factor = (
            row["fast_ratio"] * 0.3 +
            row["avg_sessions"] * 0.2 +
            row["occupancy"] * 0.2 +
            row["ev_growth"] * 0.2 +
            row["population_density"] * 0.0001
        )

        user_factor = (
            data.fast_ratio * 0.3 +
            data.avg_sessions * 0.01 +
            data.occupancy * 0.3 +
            data.ev_growth * 0.2 +
            data.population_density * 0.0001
        )

        score = base * 0.4 + (
    data.charger_count * 5 +
    data.fast_ratio * 50 +
    data.avg_sessions * 20 +
    data.occupancy * 30 +
    data.ev_growth * 25 +
    data.population_density * 0.05
)

        #score = base * 0.6 + (city_factor * user_factor) * 100

        results.append({
            "city": row["city"],
            "score": int(round(score)),   # ✅ integer now
            "latitude": float(row["latitude"]),
            "longitude": float(row["longitude"]),
            # ✅ include user inputs for frontend
            "charger_count": data.charger_count,
            "fast_ratio": data.fast_ratio,
            "avg_sessions": data.avg_sessions,
            "occupancy": data.occupancy,
            "ev_growth": data.ev_growth,
            "population_density": data.population_density
        })

    # -----------------------------
    # Rank cities
    # -----------------------------
    scores = np.array([r["score"] for r in results])

    low_th = np.percentile(scores, 33)
    high_th = np.percentile(scores, 66)

    for r in results:
        demand_index = r["score"] * (1 + data.ev_growth)

        if demand_index < 3600:
            r["level"] = "Low"
        elif demand_index < 3800:
            r["level"] = "Medium"
        else:
            r["level"] = "High"

 

    return {r["city"]: r for r in results}
    

