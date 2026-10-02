import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

# ==========================================
# 1. SIMULAÇÃO / CARREGAMENTO DO DATASET
# (Substitua esta lista pelos seus dados reais)
# ==========================================
# Exemplo com histórico recente e timestamps em segundos
base_time = datetime.now()
data = [
    {"timestamp": base_time - timedelta(seconds=300), "multiplier": 1.12},
    {"timestamp": base_time - timedelta(seconds=280), "multiplier": 1.04},
    {"timestamp": base_time - timedelta(seconds=260), "multiplier": 1.79},
    {"timestamp": base_time - timedelta(seconds=240), "multiplier": 1.10},
    {"timestamp": base_time - timedelta(seconds=210), "multiplier": 4.16},
    {"timestamp": base_time - timedelta(seconds=190), "multiplier": 1.68},
    {"timestamp": base_time - timedelta(seconds=170), "multiplier": 2.37},
    {"timestamp": base_time - timedelta(seconds=150), "multiplier": 1.15},
    {"timestamp": base_time - timedelta(seconds=130), "multiplier": 1.15},
    {"timestamp": base_time - timedelta(seconds=110), "multiplier": 2.40},
    {"timestamp": base_time - timedelta(seconds=90),  "multiplier": 5.16},
    {"timestamp": base_time - timedelta(seconds=70),  "multiplier": 2.77},
    {"timestamp": base_time - timedelta(seconds=50),  "multiplier": 1.00},
    {"timestamp": base_time - timedelta(seconds=30),  "multiplier": 1.00},
    {"timestamp": base_time - timedelta(seconds=10),  "multiplier": 1.22},
]

df = pd.DataFrame(data)

# ==========================================
# 2. ENGENHARIA DE FEATURES (TEMPO E MULTIPLICADOR)
# ==========================================
def create_features(df):
    df = df.copy()
    
    # Lags de multiplicadores anteriores
    for i in range(1, 4):
        df[f'lag_mult_{i}'] = df['multiplier'].shift(i)
        
    # Intervalo de tempo entre rodadas (em segundos)
    df['time_diff'] = df['timestamp'].diff().dt.total_seconds()
    for i in range(1, 4):
        df[f'lag_time_{i}'] = df['time_diff'].shift(i)
        
    # Médias móveis
    df['rolling_mean_3'] = df['multiplier'].rolling(3).mean().shift(1)
    
    # Target 1: Próximo Multiplicador
    df['target_multiplier'] = df['multiplier']
    
    # Target 2: Próximo Intervalo de Tempo (Segundos)
    df['target_time_diff'] = df['time_diff']
    
    return df.dropna()

featured_df = create_features(df)

# Separação de Features (X) e Targets (y)
feature_cols = ['lag_mult_1', 'lag_mult_2', 'lag_mult_3', 
                'lag_time_1', 'lag_time_2', 'lag_time_3', 'rolling_mean_3']

X = featured_df[feature_cols]
y_mult = featured_df['target_multiplier']
y_time = featured_df['target_time_diff']

# ==========================================
# 3. TREINAMENTO DOS MODELOS
# ==========================================
# Modelo 1: Random Forest para estimar o Valor do Multiplicador
model_mult = RandomForestRegressor(n_estimators=100, random_state=42)
model_mult.fit(X, y_mult)

# Modelo 2: Regressão para estimar o Horário (Tempo do próximo intervalo)
model_time = LinearRegression()
model_time.fit(X, y_time)

# ==========================================
# 4. INFERÊNCIA / PREDIÇÃO DA PRÓXIMA RODADA
# ==========================================
# Pega o último estado registrado na base para prever o próximo evento
last_row = df.tail(4)
last_time = last_row['timestamp'].iloc[-1]

latest_features = np.array([[
    last_row['multiplier'].iloc[-1], # lag_mult_1
    last_row['multiplier'].iloc[-2], # lag_mult_2
    last_row['multiplier'].iloc[-3], # lag_mult_3
    20.0, # lag_time_1 (estimado 20s)
    20.0, # lag_time_2
    20.0, # lag_time_3
    last_row['multiplier'].tail(3).mean() # rolling_mean_3
]])

# Executa as predições
predicted_multiplier = model_mult.predict(latest_features)[0]
predicted_seconds_wait = model_time.predict(latest_features)[0]

# Estima o horário exato no relógio
predicted_timestamp = last_time + timedelta(seconds=max(15, predicted_seconds_wait))

# ==========================================
# 5. EXIBIÇÃO DOS RESULTADOS
# ==========================================
print("==============================================")
print("       PAINEL DE INFERÊNCIA DO MODELO IA      ")
print("==============================================")
print(f"Última rodada registrada: {last_row['multiplier'].iloc[-1]}x às {last_time.strftime('%H:%M:%S')}")
print("----------------------------------------------")
print(f"PREDIÇÃO DO PRÓXIMO MULTIPLICADOR: {predicted_multiplier:.2f}x")
print(f"PREDIÇÃO DO HORÁRIO DA ENTRADA : {predicted_timestamp.strftime('%H:%M:%S')} (em aprox. {int(predicted_seconds_wait)}s)")
print("==============================================")
