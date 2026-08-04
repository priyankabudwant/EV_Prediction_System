import torch
import torch.nn as nn

class Attention(nn.Module):
    def __init__(self, hidden_size):
        super().__init__()
        self.attn = nn.Linear(hidden_size, 1)

    def forward(self, lstm_out):
        weights = torch.softmax(self.attn(lstm_out), dim=1)
        context = torch.sum(weights * lstm_out, dim=1)
        return context, weights

class CNN_LSTM_Attention(nn.Module):
    def __init__(self):
        super().__init__()
        self.cnn = nn.Conv1d(5, 32, kernel_size=3)
        self.lstm = nn.LSTM(32, 64, batch_first=True)
        self.attention = Attention(64)
        self.fc = nn.Linear(64, 1)

    def forward(self, x, return_attention=False):
        x = x.permute(0,2,1)
        x = torch.relu(self.cnn(x))
        x = x.permute(0,2,1)
        lstm_out,_ = self.lstm(x)

        context, weights = self.attention(lstm_out)

        output = self.fc(context)

        if return_attention:
            return output, weights
        return output
    





