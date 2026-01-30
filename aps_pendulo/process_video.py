import cv2 as cv
import numpy as np
import os

PIXEL_PARA_CM = 12 / 261
ARQUIVO_VIDEO = "video.mp4"
DIRETORIO_SAIDA = "./output/"
PASSO_TEMPO = 1 / 30  # 30 FPS

os.makedirs(DIRETORIO_SAIDA, exist_ok=True)

def binarizar(imagem):
    cinza = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
    desfocada = cv.GaussianBlur(cinza, (5, 5), 0)
    _, binaria = cv.threshold(desfocada, 100, 255, cv.THRESH_BINARY_INV)
    return binaria

def centro_de_massa(imagem):
    momentos = cv.moments(imagem)

    if momentos["m00"] == 0:
        raise ValueError("Centro de massa não encontrado")

    return momentos["m10"] / momentos["m00"]

def processar_frame(frame, tempo, lista_tempos, lista_posicoes):
    try:
        frame_binario = binarizar(frame)
        centro_x = centro_de_massa(frame_binario)
        lista_tempos.append(f"{tempo}\n")
        lista_posicoes.append(f"{centro_x * PIXEL_PARA_CM}\n")
    except ValueError as erro:
        print(f"Erro no tempo {tempo}s: {erro}")

def main():
    captura = cv.VideoCapture(ARQUIVO_VIDEO)

    if not captura.isOpened():
        print(f"Erro ao abrir o vídeo {ARQUIVO_VIDEO}")
        return

    tempo = 0
    contador_frames = 0
    intervalo_frames = int(captura.get(cv.CAP_PROP_FPS) * PASSO_TEMPO)

    tempos = []
    posicoes = []

    sucesso = True

    while sucesso:
        sucesso, frame = captura.read()

        if sucesso and contador_frames % intervalo_frames == 0:
            processar_frame(frame, tempo, tempos, posicoes)
            tempo = round(tempo + PASSO_TEMPO, 2)

        contador_frames += 1

    captura.release()

    with open(os.path.join(DIRETORIO_SAIDA, "tempos.txt"), "w") as arquivo_tempo:
        arquivo_tempo.writelines(tempos)

    with open(os.path.join(DIRETORIO_SAIDA, "espacos.txt"), "w") as arquivo_espaco:
        arquivo_espaco.writelines(posicoes)

if __name__ == "__main__":
    main()
