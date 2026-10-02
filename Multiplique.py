import pandas as pd
import numpy as np
from datetime import datetime, timedelta

HOUSE_EDGE = 0.03  # Margem padrão de 3% da casa

def calcular_probabilidade(target):
    if target < 1.01:
        return 0.0
    return (1.0 - HOUSE_EDGE) / target

def estimar_tempo_proxima_rodada(historico_mults, ultimo_horario):
    # Duração aproximada do gráfico: 10s de espera + (multiplicador * 1.2s)
    duracao_media = np.mean([10.0 + (m * 1.2) for m in historico_mults[-5:]])
    proximo_horario = ultimo_horario + timedelta(seconds=duracao_media)
    return proximo_horario, duracao_media

# Base de histórico inicial
historico_mults = [1.12, 1.04, 1.79, 1.10, 4.16, 1.22]
ultimo_horario = datetime.now()

print("==================================================")
print("   SISTEMA DINÂMICO DE PROBABILIDADE E TEMPO    ")
print("==================================================")

while True:
    print("\n--------------------------------------------------")
    try:
        # 1. Você escolhe o Cashout que quer testar agora
        alvo_str = input("Qual multiplicador você quer buscar agora? (ex: 1.50, 2.50) ou 'sair': ")
        if alvo_str.lower() == 'sair':
            break
        
        alvo_desejado = float(alvo_str)
        
        # 2. Re-calcula a probabilidade do seu novo alvo
        prob = calcular_probabilidade(alvo_desejado)
        
        # 3. Calcula a estimativa de tempo baseada nas últimas rodadas
        horario_estimado, tempo_espera = estimar_tempo_proxima_rodada(historico_mults, ultimo_horario)
        
        print("\n[RESULTADO DA INFERÊNCIA]")
        print(f" -> Alvo Selecionado        : {alvo_desejado:.2f}x")
        print(f" -> Probabilidade Real      : {prob * 100:.2f}%")
        print(f" -> Horário Estimado Entrada: {horario_estimado.strftime('%H:%M:%S')}")
        print(f" -> Tempo Espera Aproximado : ~{int(tempo_espera)} segundos")
        print("--------------------------------------------------")
        
        # 4. Atualiza o sistema com o resultado que acabou de sair no jogo
        novo_resultado = input("O que saiu na tela do jogo agora? (ex: 1.15): ")
        if novo_resultado.lower() == 'sair':
            break
            
        val_real = float(novo_resultado)
        historico_mults.append(val_real)
        ultimo_horario = datetime.now()
        
    except ValueError:
        print(">> Entrada inválida! Digite números usando ponto (ex: 1.80)")
