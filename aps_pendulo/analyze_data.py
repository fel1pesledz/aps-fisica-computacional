import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import zscore

def oscilacao_amortecida(tempo, constante, amplitude, amortecimento, omega, fase):
    return constante + amplitude * np.exp(-amortecimento * tempo) * np.cos(omega * tempo + fase)

ARQUIVO_TEMPOS = "./output/tempos.txt"
ARQUIVO_ESPACOS = "./output/espacos.txt"

try:
    tempos = np.loadtxt(ARQUIVO_TEMPOS, dtype=float)
    posicoes = np.loadtxt(ARQUIVO_ESPACOS, dtype=float)
except Exception as erro:
    print(f"Erro ao carregar os dados: {erro}")
    exit()

# Remoção de outliers via Z-score
z_scores = np.abs(zscore(posicoes))
mascara = z_scores < 2

tempos_filtrados = tempos[mascara]
posicoes_filtradas = posicoes[mascara]

palpite_inicial = [26, 18, 0.01, 2 * np.pi, 0]

limites = (
    [0, 0, 0, 0, -np.pi],
    [50, 50, 1, 10 * np.pi, np.pi]
)

try:
    parametros_otimizados, matriz_covariancia = curve_fit(
        oscilacao_amortecida,
        tempos_filtrados,
        posicoes_filtradas,
        p0=palpite_inicial,
        bounds=limites
    )
except Exception as erro:
    print(f"Erro no ajuste da curva: {erro}")
    exit()

constante, amplitude, amortecimento, omega, fase = parametros_otimizados

frequencia_natural = np.sqrt(omega**2 + amortecimento**2)
massa = 0.250
fator_qualidade = frequencia_natural / (2 * amortecimento)

with open("./output/fqualidade.txt", "w") as arquivo:
    arquivo.write(f"{fator_qualidade}")

tempo_ajuste = np.linspace(min(tempos) - 1, max(tempos) + 1, 1000)
posicao_ajuste = oscilacao_amortecida(tempo_ajuste, *parametros_otimizados)

plt.figure(figsize=(8, 5))
plt.scatter(tempos_filtrados, posicoes_filtradas, label="Dados filtrados")
plt.plot(tempo_ajuste, posicao_ajuste, label="Curva ajustada")
plt.xlabel("Tempo (s)")
plt.ylabel("Posição (cm)")
plt.title("Ajuste de Oscilação Amortecida")
plt.legend()
plt.grid(True)
plt.show()
