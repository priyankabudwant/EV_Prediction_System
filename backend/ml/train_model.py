import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# -----------------------------
# 1️⃣ Load dataset
# -----------------------------
df = pd.read_csv("city_demand_index.csv")

print("Columns used for training:")
print(df.columns)

# -----------------------------
# 2️⃣ Create Balanced Demand Levels FIRST
# -----------------------------
df["demand_level"] = pd.qcut(
    df["demand_index"],   # make sure this column exists
    q=3,
    labels=["Low", "Medium", "High"]
)

print("Distribution after balancing:")
print(df["demand_level"].value_counts())

# -----------------------------
# 3️⃣ Features
# -----------------------------
X = df[
    [
        "charger_count",
        "fast_ratio",
        "avg_sessions",
        "occupancy",
        "ev_growth",
        "population_density"
    ]
]

# -----------------------------
# 4️⃣ Target Encoding
# -----------------------------
le = LabelEncoder()
y = le.fit_transform(df["demand_level"])

# -----------------------------
# 5️⃣ Train Model
# -----------------------------
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    max_depth=None
)

model.fit(X, y)

# -----------------------------
# 6️⃣ Save Model
# -----------------------------
MODEL_DIR = "../model"
os.makedirs(MODEL_DIR, exist_ok=True)

joblib.dump(model, os.path.join(MODEL_DIR, "demand_model.pkl"))
joblib.dump(le, os.path.join(MODEL_DIR, "label_encoder.pkl"))

print("Model saved at:", os.path.abspath(MODEL_DIR))
print("✅ Model trained & saved successfully")
print("Classes:", le.classes_)
