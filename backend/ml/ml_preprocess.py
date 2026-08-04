import pandas as pd

# Load dataset
df = pd.read_csv("Indian_EV_Stations_Simplified1.csv")

print("Original columns:")
print(df.columns)

# Fix typo in latitude column
df = df.rename(columns={"lattitude": "latitude"})

# Keep important columns (AVAILABLE in your dataset)
df = df[
    [
        "state",
        "city",
        "latitude",
        "longitude",
        "charger_count",
        "fast_charger_count",
        "avg_daily_sessions",
        "occupancy_rate"
    ]
]

# Convert numeric columns
numeric_cols = [
    "charger_count",
    "fast_charger_count",
    "avg_daily_sessions",
    "occupancy_rate"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Drop missing values
df.dropna(inplace=True)

print(df.head())
