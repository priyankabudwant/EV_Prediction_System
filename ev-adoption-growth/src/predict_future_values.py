import numpy as np
import joblib

models = joblib.load("models/category_future_model.pkl")

future_years = np.array([[2026], [2027], [2028], [2029], [2030]])

for category, model in models.items():
    
    pred_log = model.predict(future_years)
    predictions = np.expm1(pred_log)   # Convert back
    
    print(f"\n📊 Future prediction for {category}:")
    for year, value in zip(future_years.flatten(), predictions):
        print(f"{year} → {int(value)} vehicles")
