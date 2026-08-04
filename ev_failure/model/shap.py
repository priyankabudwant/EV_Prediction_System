import shap
import joblib

model = joblib.load("xgboost_failure_model.pkl")

explainer = shap.Explainer(model)
shap_values = explainer(X_test)

shap.summary_plot(shap_values, X_test)