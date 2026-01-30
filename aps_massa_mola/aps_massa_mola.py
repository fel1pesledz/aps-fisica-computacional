import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle

def simulador_massa_mola():
    numero_massas = int(input("Número de massas (e molas): "))
    massas = np.array([float(input(f"Massa {i+1} (kg): ")) for i in range(numero_massas)])
    constante_mola = float(input("Constante das molas (N/m): "))
    posicoes_iniciais = np.array([float(input(f"Posição inicial da massa {i+1} (m): ")) for i in range(numero_massas)])
    velocidades_iniciais = np.array([float(input(f"Velocidade inicial da massa {i+1} (m/s): ")) for i in range(numero_massas)])
    delta_t = 0.01

    parede_esquerda = float(input("Posição da parede esquerda (m): "))
    parede_direita = float(input("Posição da parede direita (m): "))

    posicoes = posicoes_iniciais.copy()
    velocidades = velocidades_iniciais.copy()

    comprimentos_repouso = np.zeros(numero_massas + 1)
    comprimentos_repouso[0] = abs(posicoes[0] - parede_esquerda)

    for i in range(1, numero_massas):
        comprimentos_repouso[i] = abs(posicoes[i] - posicoes[i - 1])

    comprimentos_repouso[-1] = abs(parede_direita - posicoes[-1])

    def calcular_forcas(pos):
        forcas = np.zeros(numero_massas)
        for i in range(numero_massas):
            if i == 0:
                forcas[i] = (
                    -constante_mola * (pos[i] - parede_esquerda - comprimentos_repouso[0]) +
                    constante_mola * (pos[i + 1] - pos[i] - comprimentos_repouso[1])
                )
            elif i == numero_massas - 1:
                forcas[i] = (
                    -constante_mola * (pos[i] - pos[i - 1] - comprimentos_repouso[i]) -
                    constante_mola * (pos[i] - parede_direita + comprimentos_repouso[-1])
                )
            else:
                forcas[i] = (
                    -constante_mola * (pos[i] - pos[i - 1] - comprimentos_repouso[i]) +
                    constante_mola * (pos[i + 1] - pos[i] - comprimentos_repouso[i + 1])
                )
        return forcas

    def aplicar_limites(pos, vel):
        if pos[0] < parede_esquerda:
            pos[0] = parede_esquerda
            vel[0] = 0
        if pos[-1] > parede_direita:
            pos[-1] = parede_direita
            vel[-1] = 0

    def atualizar_dinamica():
        nonlocal posicoes, velocidades
        forcas = calcular_forcas(posicoes)
        aceleracoes = forcas / massas
        posicoes += velocidades * delta_t + 0.5 * aceleracoes * delta_t**2
        aplicar_limites(posicoes, velocidades)
        novas_forcas = calcular_forcas(posicoes)
        novas_aceleracoes = novas_forcas / massas
        velocidades += 0.5 * (aceleracoes + novas_aceleracoes) * delta_t

    figura, eixo = plt.subplots()
    eixo.set_xlim(parede_esquerda - 2, parede_direita + 2)
    eixo.set_ylim(-2, 2)

    blocos = [
        Rectangle((posicoes[i] - 0.2, -0.25), 0.4, 0.5, color='red')
        for i in range(numero_massas)
    ]

    for bloco in blocos:
        eixo.add_patch(bloco)

    molas, = eixo.plot([], [], '-', lw=2, color='blue')
    eixo.plot([parede_esquerda, parede_esquerda], [-0.5, 0.5], 'black', lw=2)
    eixo.plot([parede_direita, parede_direita], [-0.5, 0.5], 'black', lw=2)

    def inicializar():
        molas.set_data([], [])
        return blocos + [molas]

    def atualizar(_):
        atualizar_dinamica()
        posicoes_x = np.hstack(([parede_esquerda], posicoes, [parede_direita]))
        posicoes_y = np.zeros(numero_massas + 2)

        for i, bloco in enumerate(blocos):
            bloco.set_xy((posicoes[i] - 0.2, -0.25))

        molas.set_data(posicoes_x, posicoes_y)
        return blocos + [molas]

    animacao = FuncAnimation(
        figura,
        atualizar,
        frames=600,
        init_func=inicializar,
        blit=True,
        interval=30
    )

    plt.show()

simulador_massa_mola()
