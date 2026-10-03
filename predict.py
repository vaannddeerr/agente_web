import torch
from model import CrashPredictorLSTM

modelo = CrashPredictorLSTM()
modelo.load_state_dict(torch.load("../models/modelo_crash_lstm.pth"))
modelo.eval()

print("=== SISTEMA PREDITIVO CARREGADO ===")
# Exemplo de entrada com as últimas 5 rodadas
ultimas_5 = [1.14, 1.14, 6.55, 2.45, 334.77]
entrada_tensor = torch.tensor(ultimas_5, dtype=torch.float32).unsqueeze(0).unsqueeze(-1)

with torch.no_grad():
    predicao = modelo(entrada_tensor)

print(f"Próxima estimativa do modelo: {predicao.item():.2f}x")
