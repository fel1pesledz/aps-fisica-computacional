import curses
import numpy as np
import random
import math
import time

def inicializar_particulas(numero_particulas):
    particulas = np.zeros(numero_particulas, dtype=[
        ('x', float), ('y', float),
        ('vx', float), ('vy', float),
        ('massa', float), ('cor', int)
    ])

    for particula in particulas:
        particula['x'] = random.uniform(1, 83)
        particula['y'] = random.uniform(1, 59)
        particula['vx'] = random.uniform(-1, 1) / 5
        particula['vy'] = random.uniform(-1, 1) / 5
        particula['massa'] = random.uniform(10, 20)
        particula['cor'] = random.randint(1, 15)

    return particulas

def desenhar_particulas(tela, particulas):
    for particula in particulas:
        x, y = int(particula['x']), int(particula['y'])
        raio = int(particula['massa'] // 10)
        caractere = 'O' if raio < 2 else '0'
        try:
            tela.addch(y, x, caractere, curses.color_pair(particula['cor']))
        except curses.error:
            pass

def simular(tela, numero_particulas):
    curses.curs_set(0)
    tela.nodelay(1)

    particulas = inicializar_particulas(numero_particulas)
    atraso = 0.05

    while True:
        tela.clear()
        desenhar_particulas(tela, particulas)
        tela.refresh()

        for particula in particulas:
            particula['x'] += particula['vx']
            particula['y'] += particula['vy']

            if particula['x'] <= 1 and particula['vx'] < 0:
                particula['vx'] = -particula['vx']
            if particula['y'] <= 1 and particula['vy'] < 0:
                particula['vy'] = -particula['vy']
            if particula['x'] >= 83 and particula['vx'] > 0:
                particula['vx'] = -particula['vx']
            if particula['y'] >= 59 and particula['vy'] > 0:
                particula['vy'] = -particula['vy']

        for i in range(numero_particulas):
            for j in range(i + 1, numero_particulas):
                distancia = math.hypot(
                    particulas[j]['x'] - particulas[i]['x'],
                    particulas[j]['y'] - particulas[i]['y']
                )

                if distancia < 2:
                    angulo = math.atan2(
                        particulas[j]['y'] - particulas[i]['y'],
                        particulas[j]['x'] - particulas[i]['x']
                    )

                    velocidade1 = math.hypot(particulas[i]['vx'], particulas[i]['vy'])
                    velocidade2 = math.hypot(particulas[j]['vx'], particulas[j]['vy'])

                    massa1 = particulas[i]['massa']
                    massa2 = particulas[j]['massa']

                    novo_vx1 = (velocidade1 * math.cos(angulo) * (massa1 - massa2) + 2 * massa2 * velocidade2 * math.cos(angulo)) / (massa1 + massa2)
                    novo_vy1 = (velocidade1 * math.sin(angulo) * (massa1 - massa2) + 2 * massa2 * velocidade2 * math.sin(angulo)) / (massa1 + massa2)
                    novo_vx2 = (velocidade2 * math.cos(angulo) * (massa2 - massa1) + 2 * massa1 * velocidade1 * math.cos(angulo)) / (massa1 + massa2)
                    novo_vy2 = (velocidade2 * math.sin(angulo) * (massa2 - massa1) + 2 * massa1 * velocidade1 * math.sin(angulo)) / (massa1 + massa2)

                    particulas[i]['vx'] = novo_vx1
                    particulas[i]['vy'] = novo_vy1
                    particulas[j]['vx'] = novo_vx2
                    particulas[j]['vy'] = novo_vy2

        time.sleep(atraso)

        if tela.getch() == ord(' '):
            break

def main():
    numero_particulas = int(input("DIGITE O NUMERO DE PARTICULAS: "))
    curses.wrapper(simular, numero_particulas)

if __name__ == "__main__":
    main()
