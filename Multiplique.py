import torch
import torch.nn as nn
import numpy as np
import pandas as pd

# =========================================================
# 1. DEFINIÇÃO DA ARQUITETURA DA REDE NEURAL (LSTM)
# =========================================================
class CrashPredictorLSTM(nn.Module):
    def __init__(self, input_size=1, hidden_layer_size=128, output_size=1):
        super(CrashPredictorLSTM, self).__init__()
        self.hidden_layer_size = hidden_layer_size
        self.lstm = nn.LSTM(input_size, hidden_layer_size, num_layers=2, batch_first=True, dropout=0.2)
        self.linear = nn.Linear(hidden_layer_size, output_size)

    def forward(self, input_seq):
        lstm_out, _ = self.lstm(input_seq)
        predictions = self.linear(lstm_out[:, -1, :])
        return predictions

# =========================================================
# 2. PREPARAÇÃO E TRATAMENTO DOS DADOS (DATASET)
# =========================================================
# Substitua por seu arquivo real (ex: pd.read_csv('historico_crash.csv'))
# Exemplo com dados simulados:
dados_brutos = [1.12, 1.04, 1.79, 1.10, 4.16, 1.22, 2.45, 1.14, 1.14, 6.55, 334.77, 1.05, 1.80, 2.10]

def criar_sequencias(dados, janela=5):
    """
    Transforma a lista de multiplicadores em janelas de treino.
    Exemplo (janela=5): usa 5 multiplicadores passados para prever o 6º.
    """
    X, y = [], []
    for i in range(len(dados) - janela):
        X.append(dados[i : i + janela])
        y.append(dados[i + janela])
    return torch.tensor(X, dtype=torch.float32).unsqueeze(-1), torch.tensor(y, dtype=torch.float32).unsqueeze(-1)

JANELA_CONTEXTO = 5  # Número de rodadas passadas observadas
X_train, y_train = criar_sequencias(dados_brutos, janela=JANELA_CONTEXTO)

# =========================================================
# 3. LOOP DE TREINAMENTO DO MODELO
# =========================================================
modelo = CrashPredictorLSTM()
criterio_perda = nn.MSELoss()  # Erro Quadrático Médio
otimizador = torch.optim.Adam(modelo.parameters(), lr=0.001)

EPOCHS = 100  # Quantas vezes o modelo vai passar por todo o dataset

print("=== INICIANDO O TREINAMENTO DA REDE NEURAL ===")
modelo.train()

for epoch in range(EPOCHS):
    otimizador.zero_grad()
    
    # 1. Passada para frente (Forward Pass)
    predicoes = modelo(X_train)
    
    # 2. Cálculo do Erro (Loss)
    perda = criterio_perda(predicoes, y_train)
    
    # 3. Passada para trás (Backpropagation - Aprendizado)
    perda.backward()
    otimizador.step()
    
    if (epoch + 1) % 20 == 0:
        print(f"Época [{epoch+1}/{EPOCHS}] - Perda (Loss): {perda.item():.4f}")

# =========================================================
# 4. SALVANDO O MODELO TREINADO
# =========================================================
torch.save(modelo.state_dict(), "modelo_crash_lstm.pth")
print("\n[SUCESSO] Treinamento concluído e modelo salvo como 'modelo_crash_lstm.pth'!")
