import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. Configurações da Casa
HOUSE_EDGE = 0.03  # Margem padrão de 3%

def calcular_probabilidade_multiplicador(target):
    """Calcula a probabilidade matemática exata de atingir um multiplicador."""
    if target < 1.01:
        return 0.0
    return (1.0 - HOUSE_EDGE) / target

def estimar_tempo_proxima_rodada(historico_timestamps, historico_multiplicadores):
    """
    Calcula a duração média das rodadas anteriores para projetar
    o horário aproximado do próximo gatilho.
    """
    # Tempo médio de subida do gráfico: aprox. 1.2 segundos por ponto de multiplicador + 10s de intervalo
    tempos_estimados = [10.0 + (m * 1.2) for m in historico_multiplicadores]
    tempo_medio_rodada = np.mean(tempos_estimados)
    
    ultimo_horario = historico_timestamps[-1]
    proxima_janela = ultimo_horario + timedelta(seconds=tempo_medio_rodada)
    
    return proxima_janela, tempo_medio_rodada

# ==========================================
# SIMULAÇÃO DE ENTRADA DO USUÁRIO
# ==========================================

# Histórico recente de rodadas (últimos multiplicadores e horários)
agora = datetime.now()
historico_mults = [1.12, 1.04, 1.79, 1.10, 4.16, 1.22]
historico_tempos = [agora - timedelta(seconds=i*25) for i in range(len(historico_mults))][::-1]

# Multiplicador que você deseja tentar no Auto Cashout
ALVO_DESEJADO = 2.00 

# Execução dos cálculos
prob = calcular_probabilidade_multiplicador(ALVO_DESEJADO)
horario_estimado, espera_segundos = estimar_tempo_proxima_rodada(historico_tempos, historico_mults)

print("==================================================")
print("     PAINEL PROBABILÍSTICO DE ENTRADA TEMPORAL    ")
print("==================================================")
print(f"Alvo Definido no Auto Cashout : {ALVO_DESEJADO:.2f}x")
print(f"Probabilidade Estatística    : {prob * 100:.2f}%")
print("--------------------------------------------------")
print(f"Horário Atual                : {datetime.now().strftime('%H:%M:%S')}")
print(f"Horário Estimado da Entrada  : {horario_estimado.strftime('%H:%M:%S')}")
print(f"Tempo de Espera Aproximado   : ~{int(espera_segundos)} segundos")
print("==================================================")
