import numpy as np
import matplotlib.pyplot as plt

volume_min = 1
volume_max = 3
pressao_min = 1
pressao_max = 3
temperatura_min = 300
temperatura_max = 600

volumes = np.linspace(volume_min, volume_max, 100)

# Processos isotérmicos (P·V = constante)
pressao_expansao = pressao_min * (volume_max / volumes)
pressao_compressao = pressao_max * (volume_min / volumes)

# Processos adiabáticos (aproximação visual)
pressao_adiabatica_1 = pressao_max * (volume_min / volumes) ** 1.4
pressao_adiabatica_2 = pressao_min * (volume_max / volumes) ** 1.4

plt.figure(figsize=(14, 6))

# Diagrama PV do ciclo de Stirling
plt.subplot(1, 2, 1)
plt.plot(volumes, pressao_expansao, label="Expansão isotérmica")
plt.plot(volumes, pressao_compressao, label="Compressão isotérmica")
plt.plot(volumes, pressao_adiabatica_1, linestyle="--", label="Processo adiabático")
plt.plot(volumes, pressao_adiabatica_2, linestyle="--")
plt.xlabel("Volume (V)")
plt.ylabel("Pressão (P)")
plt.title("Diagrama PV – Ciclo de Stirling")
plt.legend()
plt.grid()

entropia_min = 1
entropia_max = 3

temperatura_expansao = np.linspace(temperatura_min, temperatura_max, 100)
temperatura_compressao = np.linspace(temperatura_max, temperatura_min, 100)

# Curvas aproximadas no diagrama TS
entropia_expansao = entropia_min + 0.5 * np.sqrt(temperatura_expansao)
entropia_compressao = entropia_max - 0.5 * np.sqrt(temperatura_compressao)

plt.subplot(1, 2, 2)
plt.plot(temperatura_expansao, entropia_expansao, label="Expansão isotérmica")
plt.plot(temperatura_compressao, entropia_compressao, label="Compressão isotérmica")
plt.plot([temperatura_min, temperatura_max], [entropia_min, entropia_max], linestyle="--", label="Processo adiabático")
plt.plot([temperatura_max, temperatura_min], [entropia_max, entropia_min], linestyle="--")
plt.xlabel("Temperatura (T)")
plt.ylabel("Entropia (S)")
plt.title("Diagrama TS – Ciclo de Stirling")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
