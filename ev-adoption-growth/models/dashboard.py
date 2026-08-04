import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# ===============================
# 1️⃣ EV Growth Prediction (5–10 Years)
# ===============================

def ev_growth_forecast():

    df = pd.read_csv("data/ev_sales_by_makers_and_cat_15-24.csv")

    df_long = df.melt(
        id_vars=["Cat", "Maker"],
        var_name="Year",
        value_name="Sales"
    )

    df_long["Year"] = df_long["Year"].astype(int)
    df_long = df_long[df_long["Sales"] > 0]

    yearly_sales = df_long.groupby("Year")["Sales"].sum().reset_index()

    X = yearly_sales[["Year"]]
    y = yearly_sales["Sales"]

    # Log-based exponential growth model
    model = LinearRegression()
    model.fit(X, np.log(y))

    future_years = list(range(2015, 2035))
    future_df = pd.DataFrame({"Year": future_years})

    log_preds = model.predict(future_df)
    predictions = np.exp(log_preds)

    plt.figure()
    plt.plot(future_years, predictions)
    plt.title("EV Adoption Growth Forecast")
    plt.xlabel("Year")
    plt.ylabel("Total EV Sales")
    plt.show()

    return predictions


# ===============================
# 2️⃣ State-wise Comparison
# ===============================

def state_wise_comparison():

    df = pd.read_csv("data/OperationalPC.csv")

    df = df.sort_values("No. of Operational PCS", ascending=False)

    plt.figure()
    plt.bar(df["State"], df["No. of Operational PCS"])
    plt.xticks(rotation=90)
    plt.title("State-wise Charging Infrastructure")
    plt.xlabel("State")
    plt.ylabel("Operational Charging Points")
    plt.show()


# ===============================
# 3️⃣ Vehicle Category-wise Adoption
# ===============================

def category_wise_adoption():

    df = pd.read_csv("data/ev_cat_01-24.csv")

    df["Year"] = pd.to_datetime(df["Date"]).dt.year

    category_totals = df.groupby("Year").sum(numeric_only=True)

    latest_year = category_totals.index.max()

    latest_data = category_totals.loc[latest_year]

    plt.figure()
    plt.bar(latest_data.index, latest_data.values)
    plt.xticks(rotation=90)
    plt.title(f"Vehicle Category Adoption - {latest_year}")
    plt.xlabel("Vehicle Category")
    plt.ylabel("Total Registrations")
    plt.show()


# ===============================
# 4️⃣ Petrol/Diesel Replacement Impact
# ===============================

def fuel_replacement_impact():

    df = pd.read_csv("data/ev_sales_by_makers_and_cat_15-24.csv")

    df_long = df.melt(
        id_vars=["Cat", "Maker"],
        var_name="Year",
        value_name="Sales"
    )

    df_long["Year"] = df_long["Year"].astype(int)
    df_long = df_long[df_long["Sales"] > 0]

    yearly_sales = df_long.groupby("Year")["Sales"].sum().reset_index()

    # Assume each EV replaces 1 petrol vehicle
    # Average CO2 emission per petrol vehicle per year ≈ 2.3 tons

    yearly_sales["CO2_Reduced_Tons"] = yearly_sales["Sales"] * 2.3

    plt.figure()
    plt.plot(yearly_sales["Year"], yearly_sales["CO2_Reduced_Tons"])
    plt.title("Estimated CO2 Reduction from EV Adoption")
    plt.xlabel("Year")
    plt.ylabel("CO2 Reduced (Tons)")
    plt.show()


# ===============================
# RUN ALL VISUALS
# ===============================

if __name__ == "__main__":

    ev_growth_forecast()
    state_wise_comparison()
    category_wise_adoption()
    fuel_replacement_impact()
