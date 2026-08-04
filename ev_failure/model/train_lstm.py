import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import joblib
from sklearn.preprocessing import MinMaxScaler
from torch.utils.data import DataLoader, TensorDataset

# 🔹 Import Attention Model
from attention_cnn_lstm import CNN_LSTM_Attention

# Load dataset
df = pd.read_csv("data/EV_Predictive_Maintenance_Dataset_15min.csv")

features = [
    "Battery_Temperature",
    "Motor_Temperature",
    "Motor_Vibration",
    "SoH",
    "Power_Consumption"
]

target = "RUL"

df = df[features + [target]].dropna()

# Separate
X_data = df[features]
y_data = df[target].values.reshape(-1, 1)

# Scale separately
feature_scaler = MinMaxScaler()
target_scaler = MinMaxScaler()

X_scaled = feature_scaler.fit_transform(X_data)
y_scaled = target_scaler.fit_transform(y_data)

sequence_length = 10
X_seq, y_seq = [], []

for i in range(len(X_scaled) - sequence_length):
    X_seq.append(X_scaled[i:i+sequence_length])
    y_seq.append(y_scaled[i+sequence_length])

X_seq = torch.tensor(np.array(X_seq), dtype=torch.float32)
y_seq = torch.tensor(np.array(y_seq), dtype=torch.float32)

dataset = TensorDataset(X_seq, y_seq)
loader = DataLoader(dataset, batch_size=64, shuffle=True)

# 🔥 Use Attention Model
model = CNN_LSTM_Attention()

criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.003)

epochs = 20

for epoch in range(epochs):
    total_loss = 0

    for batch_X, batch_y in loader:

        optimizer.zero_grad()
        output = model(batch_X)
        loss = criterion(output, batch_y)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1}, Loss: {total_loss/len(loader):.6f}")

# Save
torch.save(model.state_dict(), "attention_lstm_model.pth")
joblib.dump(feature_scaler, "attention_feature_scaler.pkl")
joblib.dump(target_scaler, "attention_target_scaler.pkl")

print("✅ Attention CNN-LSTM Training Complete")