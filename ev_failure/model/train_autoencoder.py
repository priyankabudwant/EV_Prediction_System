import pandas as pd
import torch
import torch.nn as nn
import joblib
from sklearn.preprocessing import MinMaxScaler
from torch.utils.data import DataLoader, TensorDataset

# Load data
df = pd.read_csv("data/EV_Predictive_Maintenance_Dataset_15min.csv")

features = [
    "Battery_Temperature",
    "Motor_Temperature",
    "Motor_Vibration",
    "SoH",
    "Power_Consumption"
]

df = df[features].dropna()

# Scale
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(df)

X_tensor = torch.tensor(X_scaled, dtype=torch.float32)

dataset = TensorDataset(X_tensor)
loader = DataLoader(dataset, batch_size=512, shuffle=True)

# Autoencoder Model
class AutoEncoder(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 8)
        )
        self.decoder = nn.Sequential(
            nn.Linear(8, 32),
            nn.ReLU(),
            nn.Linear(32, input_dim)
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

model = AutoEncoder(input_dim=5)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Train
for epoch in range(10):
    total_loss = 0
    for (xb,) in loader:
        optimizer.zero_grad()
        reconstruction = model(xb)
        loss = criterion(reconstruction, xb)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    print(f"Epoch {epoch+1}, Loss: {total_loss:.6f}")

# Save
torch.save(model.state_dict(), "autoencoder_model.pth")
joblib.dump(scaler, "autoencoder_scaler.pkl")

print("✅ Autoencoder saved!")