import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/ev_cat_01-24.csv")
print(df.columns)
# Convert Date safely
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
print(df["Date"].unique()[:20])

# Drop invalid date rows
df = df.dropna(subset=["Date"])

# Extract Year
df["Year"] = df["Date"].dt.year

# Remove Date column
df = df.drop(columns=["Date"])

# Group by year
yearly = df.groupby("Year").sum()


# Plot category-wise adoption
plt.figure()
yearly.plot()
plt.title("Vehicle Category-wise EV Adoption")
plt.ylabel("Registrations")
plt.show()
