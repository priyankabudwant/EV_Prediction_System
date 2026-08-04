from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import random


app = FastAPI(title="EV Charging Demand Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3002",
    ],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],   # IMPORTANT: allow POST
    allow_headers=["*"],
)

# Load trained model
model = joblib.load("model/demand_model.pkl")
# ✅ Load city data (same as training data)
city_df = pd.read_csv("city_demand_index.csv")

# Input schema
class InputData(BaseModel):
    charger_count: int
    fast_ratio: float
    avg_sessions: int
    occupancy: float
    ev_growth: float
    population_density: int

# Root endpoint
@app.get("/")
def home():
    return {"message": "EV Charging Demand Prediction API is running"}

# Prediction endpoint
@app.post("/predict")
def predict(data: InputData):

    results = []

    for _, row in city_df.iterrows():

        # city-specific base
        base = row["demand_index"]

        # city-specific multiplier (THIS IS THE KEY)
        city_factor = (
            row["fast_ratio"] * 0.3 +
            row["avg_sessions"] * 0.2 +
            row["occupancy"] * 0.2 +
            row["ev_growth"] * 0.2 +
            row["population_density"] * 0.0001
        )

        # user impact (same input, different effect)
        user_factor = (
            data.fast_ratio * 0.3 +
            data.avg_sessions * 0.01 +
            data.occupancy * 0.3 +
            data.ev_growth * 0.2 +
            data.population_density * 0.0001
        )

        score = base * 0.6 + (city_factor * user_factor) * 100

        results.append({
            "city": row["city"],
            "score": round(score, 2),
            "latitude": row["latitude"],
            "longitude": row["longitude"]
        })

    # 🔥 Rank cities by score
    scores = [r["score"] for r in results]
    low_th = sorted(scores)[int(len(scores) * 0.33)]
    high_th = sorted(scores)[int(len(scores) * 0.66)]

    # 🔥 Assign levels RELATIVELY
    for r in results:
        if r["score"] <= low_th:
            r["level"] = "Low"
        elif r["score"] <= high_th:
            r["level"] = "Medium"
        else:
            r["level"] = "High"

    return {r["city"]: r for r in results}



   

 


