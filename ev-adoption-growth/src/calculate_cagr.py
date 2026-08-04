import pandas as pd
import numpy as np

df = pd.read_csv("data/ev_cat_01-24.csv")

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"])
df["Year"] = df["Date"].dt.year

df = df.drop(columns=["Date"])

yearly = df.groupby("Year").sum()

print("\n📊 CAGR Per Category:\n")

years = yearly.index.max() - yearly.index.min()

for col in yearly.columns:
    start = yearly[col].iloc[0]
    end = yearly[col].iloc[-1]

    if start > 0:
        cagr = ((end / start) ** (1 / years) - 1) * 100
        print(f"{col} : {round(cagr,2)} %")
