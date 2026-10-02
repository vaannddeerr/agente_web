import numpy as np
from datetime import datetime, timedelta

HOUSE_EDGE = 0.03  # Margem teórica de 3% da casa

class PredictorEngine:
    def __init__(self):
        # Histórico inicial mínimo para calibrar a frequência
        self.historico = [1.50, 1.20, 2.10, 1.05]
        self.ultimo_horario = datetime.now()

    def processar_ultimo_multiplicador(self, ultimo_val):
        self.historico.append(ultimo_val)
        self.ultimo_horario = datetime.now()
        
        # 1. PREVISÃO DO PRÓXIMO MULTIPLICADOR (Regressão Estocástica Média)
        # Calcula a tendência de oscilação baseada nas últimas 5 rodadas
        ultimos_5 = self.historico[-5:]
        media_recente = np.mean(ultimos_5)
        mediana_recente = np.median(ultimos_5)
        
        # Ponderação do próximo multiplicador esperado
        proximo_mult_estimado = round((media_recente * 0.4) + (mediana_recente * 0.6), 2)
        
        # Garante limite mínimo real do jogo (1.00x)
        if proximo_mult_estimado < 1.00:
            proximo_mult_estimado = 1.00

        # 2. CÁLCULO DA PORCENTAGEM (Probabilidade Causal do valor estimado)
        if proximo_mult_estimado <= 1.00:
            porcentagem = 99.0
        else:
            porcentagem = ((1.0 - HOUSE_EDGE) / proximo_mult_estimado) * 100

        # 3. ESTIMATIVA DO HORÁRIO (Animação do gráfico + intervalo de aposta)
        # O tempo de tela da rodada é proporcional ao multiplicador que saiu
        duracao_estimada_rodada = 10.0 + (ultimo_val * 1.3)
        horario_proxima_entrada = self.ultimo_horario + timedelta(seconds=duracao_estimada_rodada)

        return proximo_mult_estimado, porcentagem, horario_proxima_entrada, duracao_estimada_rodada

# --- EXECUÇÃO EM TEMPO REAL ---
engine = PredictorEngine()

print("=========================================================")
print("   SISTEMA DE PREVISÃO DADOS -> PRÓXIMO / % / HORÁRIO   ")
print("=========================================================")

while True:
    print("\n---------------------------------------------------------")
    entrada = input("Digite o ÚLTIMO multiplicador que deu na tela (ou 'sair'): ")
    
    if entrada.lower() == 'sair':
        break

    try:
        ultimo_mult = float(entrada.replace(',', '.'))
        
        if ultimo_mult < 1.00:
            print(">> O multiplicador precisa ser igual ou maior que 1.00x.")
            continue

        # Executa o cálculo da inferência
        pred_mult, prob_pct, hora_entrada, tempo_espera = engine.processar_ultimo_multiplicador(ultimo_mult)

        print("\n[PAINEL DE INFERÊNCIA DA PRÓXIMA RODADA]")
        print(f" -> Próximo Multiplicador Estimado : {pred_mult:.2f}x")
        print(f" -> Porcentagem (Probabilidade)   : {prob_pct:.1f}%")
        print(f" -> Horário Estimado de Entrada   : {hora_entrada.strftime('%H:%M:%S')}")
        print(f" -> Tempo de Espera               : ~{int(tempo_espera)} segundos")
        print("---------------------------------------------------------")

    except ValueError:
        print(">> Digite um número válido. Exemplo: 1.75, 2.10, 1.00")
