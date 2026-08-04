import pandas as pd
import joblib
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Load dataset
df = pd.read_csv("data/EV_Predictive_Maintenance_Dataset_15min.csv")

# Drop non-numeric / unused columns
drop_cols = ["Timestamp", "Maintenance_Type"]
df = df.drop(columns=drop_cols, errors='ignore')

# Target
y = df["Failure_Probability"]

# Features
X = df.drop(columns=["Failure_Probability"])

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train XGBoost model
model = xgb.XGBRegressor(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.05
)

model.fit(X_train, y_train)

# Save model
joblib.dump(model, "model.pkl")

print("Model trained and saved successfully!")