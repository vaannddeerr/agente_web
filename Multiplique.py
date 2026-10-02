import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta

# 1. Dataset Inicial
data = [
    {"timestamp": datetime.now() - timedelta(seconds=100), "multiplier": 1.12},
    {"timestamp": datetime.now() - timedelta(seconds=80),  "multiplier": 1.04},
    {"timestamp": datetime.now() - timedelta(seconds=60),  "multiplier": 1.79},
    {"timestamp": datetime.now() - timedelta(seconds=40),  "multiplier": 1.10},
    {"timestamp": datetime.now() - timedelta(seconds=20),  "multiplier": 4.16},
]

df = pd.DataFrame(data)

def treinar_e_prever(df_atual):
    # Cria os Lags com base no histórico acumulado
    df_feat = df_atual.copy()
    df_feat['lag_1'] = df_feat['multiplier'].shift(1)
    df_feat['lag_2'] = df_feat['multiplier'].shift(2)
    df_feat['target'] = df_feat['multiplier']
    
    df_train = df_feat.dropna()
    
    if len(df_train) < 2:
        return 2.00, datetime.now() + timedelta(seconds=20)
    
    X = df_train[['lag_1', 'lag_2']]
    y = df_train['target']
    
    # Treina o modelo com o histórico atualizado
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Pega os últimos 2 multiplicadores para prever o próximo
    ultimos_valores = np.array([[df_atual['multiplier'].iloc[-1], df_atual['multiplier'].iloc[-2]]])
    predicao_mult = model.predict(ultimos_valores)[0]
    
    # Estima o horário da próxima rodada (adicionando 20 segundos)
    proximo_horario = datetime.now() + timedelta(seconds=20)
    
    return predicao_mult, proximo_horario

# LOOP EM TEMPO REAL
print("=== SISTEMA PREDITIVO DINÂMICO INICIADO ===")
while True:
    pred_mult, pred_hora = treinar_e_prever(df)
    
    print("\n--------------------------------------------------")
    print(f" PREVISÃO PARA A PRÓXIMA RODADA:")
    print(f"   Multiplicador Estimado: {pred_mult:.2f}x")
    print(f"   Horário da Entrada   : {pred_hora.strftime('%H:%M:%S')}")
    print("--------------------------------------------------")
    
    # Entrada do usuário para a rodada real que acabou de acontecer
    entrada = input("Digite o multiplicador REAL que saiu agora (ou 'sair'): ")
    if entrada.lower() == 'sair':
        break
        
    try:
        val_real = float(entrada)
        # Adiciona o novo dado ao dataset e recalcula
        novo_registro = {"timestamp": datetime.now(), "multiplier": val_real}
        df = pd.concat([df, pd.DataFrame([novo_registro])], ignore_index=True)
    except ValueError:
        print("Valor inválido! Digite um número como 1.50 ou 2.10")
