import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import joblib
from sklearn.preprocessing import MinMaxScaler
from torch.utils.data import DataLoader, TensorDataset

# =========================
# LOAD DATA
# =========================

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

X_data = df[features]
y_data = df[target].values.reshape(-1, 1)

# =========================
# SCALE DATA
# =========================

feature_scaler = MinMaxScaler()
target_scaler = MinMaxScaler()

X_scaled = feature_scaler.fit_transform(X_data)
y_scaled = target_scaler.fit_transform(y_data)

# =========================
# CREATE SEQUENCES
# =========================

sequence_length = 10

X_seq = []
y_seq = []

for i in range(len(X_scaled) - sequence_length):
    X_seq.append(X_scaled[i:i+sequence_length])
    y_seq.append(y_scaled[i+sequence_length])

X_seq = torch.tensor(np.array(X_seq), dtype=torch.float32)
y_seq = torch.tensor(np.array(y_seq), dtype=torch.float32)

dataset = TensorDataset(X_seq, y_seq)
loader = DataLoader(dataset, batch_size=64, shuffle=True)

# =========================
# DEFINE CNN-LSTM MODEL
# =========================

class CNN_LSTM(nn.Module):
    def __init__(self):
        super().__init__()

        self.cnn = nn.Conv1d(
            in_channels=5,
            out_channels=32,
            kernel_size=3
        )

        self.lstm = nn.LSTM(
            input_size=32,
            hidden_size=64,
            batch_first=True
        )

        self.fc = nn.Linear(64, 1)

    def forward(self, x):
        x = x.permute(0, 2, 1)
        x = torch.relu(self.cnn(x))
        x = x.permute(0, 2, 1)
        x, _ = self.lstm(x)
        x = self.fc(x[:, -1, :])
        return x

# =========================
# TRAINING SETUP
# =========================

model = CNN_LSTM()

criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

epochs = 30

# =========================
# TRAIN LOOP
# =========================

for epoch in range(epochs):

    total_loss = 0

    for batch_X, batch_y in loader:

        optimizer.zero_grad()

        output = model(batch_X)

        loss = criterion(output, batch_y)

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1}/{epochs} | Loss: {total_loss/len(loader):.6f}")

# =========================
# SAVE MODEL + SCALERS
# =========================

torch.save(model.state_dict(), "cnn_lstm_model.pth")

joblib.dump(feature_scaler, "lstm_X_scaler.pkl")
joblib.dump(target_scaler, "lstm_y_scaler.pkl")

print("\n✅ CNN-LSTM model saved successfully!")