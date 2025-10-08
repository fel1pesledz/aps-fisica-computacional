import numpy as np
import matplotlib.pyplot as plt

# Definir os parâmetros para o ciclo de Stirling
V_min = 1  # Volume mínimo arbitrário
V_max = 3  # Volume máximo arbitrário
P_min = 1  # Pressão mínima arbitrária
P_max = 3  # Pressão máxima arbitrária
T_min = 300  # Temperatura mínima em K
T_max = 600  # Temperatura máxima em K

# Diagrama PV - Curvas isotérmicas
V = np.linspace(V_min, V_max, 100)

# Expansão isotérmica (P * V = constante)
P_expansion = P_min * (V_max / V)

# Compressão isotérmica (P * V = constante)
P_compression = P_max * (V_min / V)

# Curvas adiabáticas (aproximação simples para visualização)
P_adiabatic1 = P_max * (V_min / V) ** 1.4  # Processos adiabáticos
P_adiabatic2 = P_min * (V_max / V) ** 1.4

# Plotando o gráfico do ciclo Stirling (PV)
plt.figure(figsize=(14, 6))

# Diagrama PV (sentido horário, máquina térmica)
plt.subplot(1, 2, 1)
plt.plot(V, P_expansion, label="Expansão isotérmica", color='b')
plt.plot(V, P_compression, label="Compressão isotérmica", color='r')
plt.plot(V, P_adiabatic1, label="Processo adiabático 1", linestyle='--', color='g')
plt.plot(V, P_adiabatic2, label="Processo adiabático 2", linestyle='--', color='g')
plt.xlabel("Volume (V)")
plt.ylabel("Pressão (P)")
plt.title("Diagrama PV do Ciclo de Stirling")
plt.legend()
plt.grid()

# Diagrama TS (Temperatura vs Entropia)
S_min = 1  # Entropia mínima arbitrária
S_max = 3  # Entropia máxima arbitrária

# Expansão isotérmica
T_expansion = np.linspace(T_min, T_max, 100)
T_compression = np.linspace(T_max, T_min, 100)

# Aproximação para as curvas de entropia
S_expansion = S_min + 0.5 * np.sqrt(T_expansion)
S_compression = S_max - 0.5 * np.sqrt(T_compression)

# Plotando o gráfico TS (ciclo de Stirling)
plt.subplot(1, 2, 2)
plt.plot(T_expansion, S_expansion, label="Expansão isotérmica", color='b')
plt.plot(T_compression, S_compression, label="Compressão isotérmica", color='r')
plt.plot([T_min, T_max], [S_min, S_max], linestyle='--', label="Processo adiabático", color='g')
plt.plot([T_max, T_min], [S_max, S_min], linestyle='--', label="Processo adiabático", color='g')
plt.xlabel("Temperatura (T)")
plt.ylabel("Entropia (S)")
plt.title("Diagrama TS do Ciclo de Stirling")
plt.legend()
plt.grid()

# Ajustar o layout
plt.tight_layout()
plt.show()
