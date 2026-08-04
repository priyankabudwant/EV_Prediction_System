from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load data
df = pd.read_csv(os.path.join(BASE_DIR, "data", "ev_cat_01-24.csv"))
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"])
df["Year"] = df["Date"].dt.year

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.json
    year = int(data.get("year", 2030))
    category = data.get("category", "TWO WHEELER(T)")
    
    models = joblib.load(os.path.join(BASE_DIR, "models", "category_future_model1.pkl"))
    
    if category not in models:
        return jsonify({"error": "Category not found"}), 404
    
    model = models[category]
    pred_log = model.predict(np.array([[year]]))
    prediction = int(np.expm1(pred_log)[0])
    
    return jsonify({"year": year, "category": category, "prediction": prediction})



@app.route("/api/top5-growth")
def top5_growth():
    try:
        df_numeric = df.select_dtypes(include=[np.number])
        yearly = df_numeric.groupby(df["Year"]).sum()
        models = joblib.load(os.path.join(BASE_DIR, "models", "category_future_model1.pkl"))
        
        future_year = 2035
        growth_data = []
        
        for col in yearly.columns:
            if col not in models:
                continue
            
            model = models[col]
            current_value = yearly[col].iloc[-1]
            future_log = model.predict(np.array([[future_year]]))
            future_value = np.expm1(future_log)[0]
            growth = future_value - current_value
            
            growth_data.append({
                "category": col,
                "current": int(current_value),
                "future": int(future_value),
                "growth": int(growth)
            })
        
        growth_data.sort(key=lambda x: x["growth"], reverse=True)
        return jsonify(growth_data[:5])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/co2-reduction")
def co2_reduction():
    try:
        df_numeric = df.select_dtypes(include=[np.number])
        yearly = df_numeric.groupby(df["Year"]).sum()
        models = joblib.load(os.path.join(BASE_DIR, "models", "category_future_model1.pkl"))
        
        CO2_PER_VEHICLE = 2.3
        future_year = 2035
        co2_data = []
        
        for col in yearly.columns:
            if col not in models:
                continue
            
            model = models[col]
            current_value = yearly[col].iloc[-1]
            future_log = model.predict(np.array([[future_year]]))
            future_value = np.expm1(future_log)[0]
            growth = future_value - current_value
            co2_reduction = growth * CO2_PER_VEHICLE
            
            co2_data.append({
                "category": col,
                "co2_reduction": round(co2_reduction, 2)
            })
        
        co2_data.sort(key=lambda x: x["co2_reduction"], reverse=True)
        return jsonify(co2_data[:5])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/2w-vs-4w")
def compare_2w_4w():
    df_clean = df.copy()
    df_clean.columns = df_clean.columns.str.strip().str.upper()
    
    df_clean["TWO_WHEELER_TOTAL"] = (
        df_clean.get("TWO WHEELER(T)", 0) +
        df_clean.get("TWO WHEELER(NT)", 0) +
        df_clean.get("TWO WHEELER (INVALID CARRIAGE)", 0)
    )
    
    df_clean["FOUR_WHEELER_TOTAL"] = (
        df_clean.get("LIGHT MOTOR VEHICLE", 0) +
        df_clean.get("HEAVY MOTOR VEHICLE", 0) +
        df_clean.get("LIGHT PASSENGER VEHICLE", 0) +
        df_clean.get("HEAVY PASSENGER VEHICLE", 0)
    )
    
    yearly = df_clean.groupby("YEAR")[["TWO_WHEELER_TOTAL", "FOUR_WHEELER_TOTAL"]].sum()
    
    result = {
        "years": yearly.index.tolist(),
        "two_wheeler": yearly["TWO_WHEELER_TOTAL"].tolist(),
        "four_wheeler": yearly["FOUR_WHEELER_TOTAL"].tolist()
    }
    
    return jsonify(result)

@app.route("/api/categories")
def get_categories():
    models = joblib.load(os.path.join(BASE_DIR, "models", "category_future_model1.pkl"))
    return jsonify(list(models.keys()))

@app.route("/api/yearly-trend")
def yearly_trend():
    try:
        df_numeric = df.select_dtypes(include=[np.number])
        yearly = df_numeric.groupby(df["Year"]).sum()
        total_by_year = yearly.sum(axis=1)
        
        result = {
            "years": total_by_year.index.tolist(),
            "total": total_by_year.tolist()
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/comprehensive-predict", methods=["POST"])
def comprehensive_predict():
    try:
        data = request.json
        year = int(data.get("year", 2030))
        category = data.get("category")
        state = data.get("state", "")
        
        models = joblib.load(os.path.join(BASE_DIR, "models", "category_future_model1.pkl"))
        
        if category not in models:
            return jsonify({"error": "Category not found"}), 404
        
        model = models[category]
        pred_log = model.predict(np.array([[year]]))
        vehicle_prediction = int(np.expm1(pred_log)[0])
        
        # Calculate additional metrics
        df_numeric = df.select_dtypes(include=[np.number])
        yearly = df_numeric.groupby(df["Year"]).sum()
        current_value = yearly[category].iloc[-1] if category in yearly.columns else 0
        
        growth = vehicle_prediction - current_value
        years_diff = year - df["Year"].max()
        growth_rate = round(((vehicle_prediction / current_value) ** (1/years_diff) - 1) * 100, 2) if current_value > 0 and years_diff > 0 else 0
        
        co2_reduction = round(growth * 2.3, 2)
        required_pcs = round(vehicle_prediction / 50)
        market_value = round(vehicle_prediction * 8 / 10000000)
        energy_demand = round(vehicle_prediction * 15 / 1000)
        
        insights = [
            f"Expected {growth:,} new {category} registrations by {year}",
            f"Infrastructure needs to grow by {round(required_pcs * 0.2):,} charging stations",
            f"Potential to reduce {co2_reduction:,} tons of CO2 emissions annually",
            f"Market opportunity worth ₹{market_value:,} Crores"
        ]
        
        if state:
            insights.append(f"State-specific analysis for {state} included")
        
        result = {
            "vehicle_prediction": vehicle_prediction,
            "growth_rate": growth_rate,
            "co2_reduction": co2_reduction,
            "required_pcs": required_pcs,
            "market_value": market_value,
            "energy_demand": energy_demand,
            "insights": insights,
            "category": category,
            "year": year
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/pcs-clustering")
def pcs_clustering():
    try:
        from sklearn.cluster import KMeans
        df = pd.read_csv(os.path.join(BASE_DIR, "data", "OperationalPC.csv"))
        X = df[["No. of Operational PCS"]]
        kmeans = KMeans(n_clusters=3, random_state=42)
        df["Cluster"] = kmeans.fit_predict(X)
        
        result = df[["State", "No. of Operational PCS", "Cluster"]].to_dict('records')
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/pcs-projection")
def pcs_projection():
    try:
        df = pd.read_csv(os.path.join(BASE_DIR, "data", "OperationalPC.csv"))
        GROWTH_RATE = 0.20
        years = 5
        df["Projected_PCS_5Y"] = df["No. of Operational PCS"] * ((1+GROWTH_RATE)**years)
        df = df.sort_values("Projected_PCS_5Y", ascending=False)
        
        result = df[["State", "No. of Operational PCS", "Projected_PCS_5Y"]].head(10).to_dict('records')
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/pcs-ranking")
def pcs_ranking():
    try:
        df = pd.read_csv(os.path.join(BASE_DIR, "data", "OperationalPC.csv"))
        df = df.sort_values("No. of Operational PCS", ascending=False)
        df["Rank"] = range(1, len(df)+1)
        
        result = df[["Rank", "State", "No. of Operational PCS"]].head(15).to_dict('records')
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/forecast")
def forecast():
    try:
        model = joblib.load(os.path.join(BASE_DIR, "models", "ev_growth_model.pkl"))
        future_years = list(range(2015, 2036))
        future_df = pd.DataFrame({"Year": future_years})
        log_predictions = model.predict(future_df)
        predictions = np.exp(log_predictions)
        
        result = {
            "years": future_years,
            "predictions": [int(p) for p in predictions]
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
