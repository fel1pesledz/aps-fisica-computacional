import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle

def massa_mola_simulador():
    # Entrada do usuário
    n = int(input("Número de massas (e molas): "))
    m = np.array([float(input(f"Massa {i+1} (kg): ")) for i in range(n)])
    k = float(input("Constante das molas (N/m): "))
    x0 = np.array([float(input(f"Posição inicial da massa {i+1} (m): ")) for i in range(n)])
    v0 = np.array([float(input(f"Velocidade inicial da massa {i+1} (m/s): ")) for i in range(n)])
    dt = 0.01  # Passo de tempo para integração

    # Paredes
    parede_esquerda = float(input("Posição da parede esquerda (m): "))
    parede_direita = float(input("Posição da parede direita (m): "))

    # Estado inicial
    posicoes = x0.copy()  # Renomeei para evitar conflito com `x` global
    velocidades = v0.copy()  # Renomeei para evitar conflito com `v` global

    # Calcular comprimentos de repouso iniciais
    d = np.zeros(n + 1)
    d[0] = abs(posicoes[0] - parede_esquerda)  # Distância parede esquerda e 1ª massa
    for i in range(1, n):
        d[i] = abs(posicoes[i] - posicoes[i - 1])  # Distâncias entre massas adjacentes
    d[-1] = abs(parede_direita - posicoes[-1])  # Distância última massa e parede direita

    # Função para calcular forças
    def calcular_forcas(pos):
        f = np.zeros(n)
        for i in range(n):
            if i == 0:  # Primeira massa (ligada à parede esquerda)
                f[i] = -k * (pos[i] - parede_esquerda - d[0]) + k * (pos[i + 1] - pos[i] - d[1])
            elif i == n - 1:  # Última massa (ligada à parede direita)
                f[i] = -k * (pos[i] - pos[i - 1] - d[i]) - k * (pos[i] - parede_direita + d[-1])
            else:  # Massas intermediárias
                f[i] = -k * (pos[i] - pos[i - 1] - d[i]) + k * (pos[i + 1] - pos[i] - d[i + 1])
        return f

    # Função para restringir a posição e velocidade das massas
    def aplicar_limites(pos, vel):
        if pos[0] < parede_esquerda:  # Massa esquerda ultrapassa limite
            pos[0] = parede_esquerda
            vel[0] = 0
        if pos[-1] > parede_direita:  # Massa direita ultrapassa limite
            pos[-1] = parede_direita
            vel[-1] = 0

    # Integração Verlet
    def atualizar_dinamica():
        nonlocal posicoes, velocidades
        f = calcular_forcas(posicoes)
        a = f / m
        posicoes += velocidades * dt + 0.5 * a * dt**2  # Atualiza posições
        aplicar_limites(posicoes, velocidades)  # Aplica restrições de parede
        f_new = calcular_forcas(posicoes)  # Recalcula forças com novas posições
        a_new = f_new / m
        velocidades += 0.5 * (a + a_new) * dt  # Atualiza velocidades

    # Configuração da animação
    fig, ax = plt.subplots()
    ax.set_xlim(parede_esquerda - 2, parede_direita + 2)
    ax.set_ylim(-2, 2)

    # Criar os "blocos" para as massas
    blocos = [Rectangle((posicoes[i] - 0.2, -0.25), 0.4, 0.5, color='red') for i in range(n)]
    for retangulo in blocos:
        ax.add_patch(retangulo)

    springs, = ax.plot([], [], '-', lw=2, color='blue')  # Linha para as molas
    ax.plot([parede_esquerda, parede_esquerda], [-0.5, 0.5], 'black', lw=2)
    ax.plot([parede_direita, parede_direita], [-0.5, 0.5], 'black', lw=2)

    def init():
        springs.set_data([], [])
        return blocos + [springs]

    def update(_):
        atualizar_dinamica()
        x_positions = np.hstack(([parede_esquerda], posicoes, [parede_direita]))
        y_positions = np.zeros(n + 2)

        # Atualizar posições dos blocos
        for i, retangulo in enumerate(blocos):
            retangulo.set_xy((posicoes[i] - 0.2, -0.25))

        # Atualizar mola
        springs.set_data(x_positions, y_positions)
        return blocos + [springs]

    anim = FuncAnimation(fig, update, frames=600, init_func=init, blit=True, interval=30)
    plt.show()


# Chamar o simulador
massa_mola_simulador()
