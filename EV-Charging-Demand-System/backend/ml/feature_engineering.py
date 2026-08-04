import pandas as pd
import os

# Absolute path (safe)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "Indian_EV_Stations_Simplified1.csv")

# Load dataset
df = pd.read_csv(DATA_PATH)

print("Original Columns:")
print(df.columns)

# Fix column name
df = df.rename(columns={"lattitude": "latitude"})

# Select required columns
df = df[
    [
        "state",
        "city",
        "latitude",
        "longitude",
        "charger_count",
        "fast_charger_count",
        "avg_daily_sessions",
        "occupancy_rate",
        "ev_growth_rate",
        "population_density"
    ]
]

# Convert numeric columns safely
numeric_cols = [
    "latitude",
    "longitude",
    "charger_count",
    "fast_charger_count",
    "avg_daily_sessions",
    "occupancy_rate",
    "ev_growth_rate",
    "population_density"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Drop invalid rows (THIS FIXES YOUR ERROR)
df.dropna(inplace=True)

# Fast charger ratio
df["fast_ratio"] = df["fast_charger_count"] / df["charger_count"]

# City-level aggregation
city_df = df.groupby("city").agg(
    state=("state", "first"),
    charger_count=("charger_count", "sum"),
    fast_ratio=("fast_ratio", "mean"),
    avg_sessions=("avg_daily_sessions", "mean"),
    occupancy=("occupancy_rate", "mean"),
    ev_growth=("ev_growth_rate", "mean"),
    population_density=("population_density", "mean"),
    latitude=("latitude", "mean"),
    longitude=("longitude", "mean")
).reset_index()

# Demand Index
city_df["demand_index"] = (
    city_df["fast_ratio"] * 30 +
    city_df["avg_sessions"] * 0.25 +
    city_df["occupancy"] * 25 +
    city_df["ev_growth"] * 10 +
    city_df["population_density"] * 0.0005
)

# Demand labels
city_df["demand_level"] = pd.qcut(
    city_df["demand_index"],
    q=3,
    labels=["Low", "Medium", "High"]
)


# Save output
OUTPUT_PATH = os.path.join(BASE_DIR, "..", "city_demand_index.csv")
city_df.to_csv(OUTPUT_PATH, index=False)

print("✅ Feature engineering completed successfully")
print(city_df.head())
