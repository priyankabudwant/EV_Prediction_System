import pandas as pd
import matplotlib.pyplot as plt

# =============================
# Load dataset
# =============================

df = pd.read_csv("data/ev_cat_01-24.csv")

# Clean column names first
df.columns = df.columns.str.strip()
df.columns = df.columns.str.upper()

print("Columns Available:\n", df.columns)

# =============================
# Clean Date column
# =============================

df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")
df = df.dropna(subset=["DATE"])

df["YEAR"] = df["DATE"].dt.year

# =============================
# Combine 2W categories
# =============================

df["TWO_WHEELER_TOTAL"] = (
    df["TWO WHEELER(T)"] +
    df["TWO WHEELER(NT)"] +
    df["TWO WHEELER (INVALID CARRIAGE)"]
)

# =============================
# Define 4W properly
# =============================

df["FOUR_WHEELER_TOTAL"] = (
    df["LIGHT MOTOR VEHICLE"] +
    df["HEAVY MOTOR VEHICLE"] +
    df["LIGHT PASSENGER VEHICLE"] +
    df["HEAVY PASSENGER VEHICLE"]
)

# =============================
# Aggregate yearly
# =============================

yearly = df.groupby("YEAR")[["TWO_WHEELER_TOTAL", "FOUR_WHEELER_TOTAL"]].sum()

print("\nYearly Data:\n", yearly)

# =============================
# Plot comparison
# =============================

plt.figure(figsize=(10,6))

plt.plot(yearly.index, yearly["TWO_WHEELER_TOTAL"], label="Two Wheeler")
plt.plot(yearly.index, yearly["FOUR_WHEELER_TOTAL"], label="Four Wheeler")

plt.legend()
plt.title("2W vs 4W EV Growth Comparison")
plt.xlabel("Year")
plt.ylabel("Registrations")
plt.grid(True)

plt.show()
