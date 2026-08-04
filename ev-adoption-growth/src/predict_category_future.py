import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import os

# Load dataset
df = pd.read_csv("data/ev_cat_01-24.csv")

# Remove spaces in column names
df.columns = df.columns.str.strip()

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Extract Year
df['Year'] = df['Date'].dt.year

# Group by Year and sum all vehicle categories
yearly = df.groupby("Year").sum(numeric_only=True).reset_index()

print("Yearly Data Preview:")
print(yearly.head())

# Remove Year column from category list
categories = yearly.columns.drop("Year")

models = {}

for col in categories:
    
    # Remove negative values (if any)
    yearly[col] = yearly[col].clip(lower=0)
    
    X = yearly[['Year']].values
    y = np.log1p(yearly[col].values)   # Safe log
    
    model = LinearRegression()
    model.fit(X, y)
    
    models[col] = model

# Create models folder if not exists
os.makedirs("models", exist_ok=True)

# Save model
joblib.dump(models, "models/category_future_model.pkl")

print("✅ Model trained and saved successfully!")
