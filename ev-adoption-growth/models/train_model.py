import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
# Load dataset
df = pd.read_csv("data/ev_sales_by_makers_and_cat_15-24.csv")

# Convert wide → long
df_long = df.melt(
    id_vars=["Cat", "Maker"],
    var_name="Year",
    value_name="Sales"
)

df_long["Year"] = df_long["Year"].astype(int)
df_long = df_long.dropna()
df_long = df_long[df_long["Sales"] > 0]

# Aggregate yearly sales
yearly_sales = df_long.groupby("Year")["Sales"].sum().reset_index()

X = yearly_sales[["Year"]]
y = yearly_sales["Sales"]

# Apply log transformation
y_log = np.log(y)

# Train linear regression on log data
model = LinearRegression()
model.fit(X, y_log)

# Predict on training years (2015–2024)
log_predictions = model.predict(X)
predictions = np.exp(log_predictions)

# Add predictions to dataframe
yearly_sales["Predicted_Sales"] = predictions

print("\n📊 Year-wise Evaluation:\n")
print(yearly_sales)

# Evaluation Metrics
mae = mean_absolute_error(y, predictions)
rmse = np.sqrt(mean_squared_error(y, predictions))
r2 = r2_score(y, predictions)

print("\n📈 Model Evaluation Metrics:")
print("MAE :", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R2 Score:", round(r2, 4))

# Save model
joblib.dump(model, "models/ev_growth_model.pkl")

print("\n✅ Exponential Growth Model Saved Successfully!")

# Save model
joblib.dump(model, "models/ev_growth_model.pkl")

print("Exponential Growth Model Saved!")
