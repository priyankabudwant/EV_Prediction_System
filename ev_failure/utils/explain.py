import shap
import joblib
import pandas as pd

model = joblib.load("model/xgboost_failure_model.pkl")

def explain_prediction(data_dict):
    explainer = shap.Explainer(model)
    df = pd.DataFrame([data_dict])
    shap_values = explainer(df)
    return shap_values.values.tolist()