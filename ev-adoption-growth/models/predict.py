import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

model = joblib.load("models/ev_growth_model.pkl")

future_years = list(range(2015, 2036))

future_df = pd.DataFrame({
    "Year": future_years
})

# Predict log values
log_predictions = model.predict(future_df)

# Convert back from log
predictions = np.exp(log_predictions)

print("\nEV Adoption Forecast:\n")

for year, pred in zip(future_years, predictions):
    print(f"{year} -> {int(pred)} EVs")

plt.figure()
plt.plot(future_years, predictions)
plt.xlabel("Year")
plt.ylabel("Predicted EV Sales")
plt.title("EV Adoption Growth Forecast (Exponential Model)")
plt.show()
