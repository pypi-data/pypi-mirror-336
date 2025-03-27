import torch.nn as nn
import torch

class RNN(nn.Module):
    def __init__(self, vocab_size, embed_size, hidden_size, num_layers):
        super().__init__()
        self.hidden_size = hidden_size
        self.embed = nn.Embedding(vocab_size, embed_size)
        self.lstm = nn.LSTM(embed_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, x, hidden, cell):
        x = self.embed(x).unsqueeze(1)  
        out, (hidden, cell) = self.lstm(x, (hidden, cell))
        out = self.fc(out).reshape(out.size(0), -1)
        return out, hidden, cell
    
    def init_hidden(self, batch_size):
        hidden = torch.zeros(self.lstm.num_layers, batch_size, self.hidden_size)
        cell = torch.zeros(self.lstm.num_layers, batch_size, self.hidden_size)
        return hidden, cell 