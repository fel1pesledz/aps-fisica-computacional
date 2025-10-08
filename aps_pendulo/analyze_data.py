import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import zscore

# Função de ajuste
def curva_amortecida(t, cte, amplitude, b, omega, phi):
    return cte + amplitude * np.exp(-b * t) * np.cos(omega * t + phi)

# Carregando os dados
TEMPOS_FILE = "./output/tempos.txt"
ESPACOS_FILE = "./output/espacos.txt"
try:
    x_data = np.loadtxt(TEMPOS_FILE, dtype=float)
    y_data = np.loadtxt(ESPACOS_FILE, dtype=float)
except Exception as e:
    print(f"Erro ao carregar os dados: {e}")
    exit()

# Filtragem de outliers usando Z-score
z_scores = np.abs(zscore(y_data))
mask = z_scores < 2  # Mantém apenas os pontos dentro de 2 desvios padrões
x_filtered = x_data[mask]
y_filtered = y_data[mask]

# Palpite inicial para os parâmetros do ajuste
guess = [26, 18, 0.01, 2 * np.pi, 0]

# Definindo limites para os parâmetros
bounds = ([0, 0, 0, 0, -np.pi], [50, 50, 1, 10 * np.pi, np.pi])

# Ajustando a curva
try:
    popt, pcov = curve_fit(curva_amortecida, x_filtered, y_filtered, p0=guess, bounds=bounds)
except Exception as e:
    print(f"Erro no ajuste da curva: {e}")
    exit()

# Extraindo os parâmetros ajustados
cte, amplitude, b, omega, phi = popt

w0 = np.sqrt(omega**2 + b**2)  # Freqüência angular natural
m = 0.250  # Massa do pêndulo em kg
q = w0 / (2 * b)  # Fator de qualidade (Q)

# Salvando o fator de qualidade
with open("./output/fqualidade.txt", "w") as f:
    f.write(f"{q}")

# Gerando os dados ajustados (expansão do intervalo)
x_fit = np.linspace(min(x_data) - 1, max(x_data) + 1, 1000)
y_fit = curva_amortecida(x_fit, *popt)

# Plotando somente a curva ajustada e os pontos
plt.figure(figsize=(8, 5))
plt.scatter(x_filtered, y_filtered, color="blue", label="Dados filtrados")
plt.plot(x_fit, y_fit, color="red", label="Curva ajustada")
plt.xlabel("Tempo (s)")
plt.ylabel("Posição (cm)")
plt.title("Ajuste de Oscilação Amortecida")
plt.legend()
plt.grid(True)
plt.show()
