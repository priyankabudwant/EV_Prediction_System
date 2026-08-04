from xgboost import XGBRegressor

y_rul = df['RUL']

rul_model = XGBRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=6
)

rul_model.fit(X, y_rul)

joblib.dump(rul_model, "rul_model.pkl")

print("RUL model saved!")