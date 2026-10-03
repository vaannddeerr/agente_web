import torch
import torch.nn as nn
import pandas as pd
from model import CrashPredictorLSTM

def criar_sequencias(dados, janela=5):
    X, y = [], []
    for i in range(len(dados) - janela):
        X.append(dados[i : i + janela])
        y.append(dados[i + janela])
    return torch.tensor(X, dtype=torch.float32).unsqueeze(-1), torch.tensor(y, dtype=torch.float32).unsqueeze(-1)

# 1. Carregar dados
# df = pd.read_csv('../data/historico_crash.csv')
dados_brutos = [1.12, 1.04, 1.79, 1.10, 4.16, 1.22, 2.45, 1.14, 1.14, 6.55, 334.77, 1.05]

X_train, y_train = criar_sequencias(dados_brutos, janela=5)

# 2. Treinar
modelo = CrashPredictorLSTM()
criterio = nn.MSELoss()
otimizador = torch.optim.Adam(modelo.parameters(), lr=0.001)

for epoch in range(100):
    otimizador.zero_grad()
    pred = modelo(X_train)
    loss = criterio(pred, y_train)
    loss.backward()
    otimizador.step()

# 3. Salvar o .pth dentro da pasta models/
torch.save(modelo.state_dict(), "../models/modelo_crash_lstm.pth")
print("Modelo treinado e salvo em 'models/modelo_crash_lstm.pth'")
