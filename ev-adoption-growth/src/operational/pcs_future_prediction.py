# 2_pcs_future_prediction.py

import pandas as pd
import numpy as np

df = pd.read_csv("data/OperationalPC.csv")

GROWTH_RATE = 0.20  # assume 20% annual infra growth

years = 5  # next 5 years

df["Projected_PCS_5Y"] = df["No. of Operational PCS"] * ((1+GROWTH_RATE)**years)

print("\n🔮 PCS Projection After 5 Years:\n")
print(df[["State", "Projected_PCS_5Y"]].sort_values(
    "Projected_PCS_5Y", ascending=False))

df = df.sort_values("No. of Operational PCS", ascending=False)

df["Rank"] = range(1, len(df)+1)

print("\n🏆 State-wise Charging Infrastructure Ranking:\n")
print(df[["Rank", "State", "No. of Operational PCS"]])