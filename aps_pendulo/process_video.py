from functools import partial
import cv2 as cv
import numpy as np
import os

# Relação pixel para cm (ajuste com base nos experimentos)
PIXEL_TO_CM = 12 / 261  # cm/pixel
VIDEO_FILE = "video.mp4"  # Nome do vídeo
OUTPUT_DIR = "./output/"
FRAME_RATE = 1 / 30  # 30 FPS

# Cria a pasta de saída, se não existir
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Função para binarizar um frame
def binarize(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)  # Converte para escala de cinza
    blurred = cv.GaussianBlur(gray, (5, 5), 0)  # Aplica blur para remover ruído
    _, binary = cv.threshold(blurred, 100, 255, cv.THRESH_BINARY_INV)  # Binarização
    return binary

def centro_de_massa(image):
    # Calcula os momentos da imagem binarizada
    moments = cv.moments(image)

    # Evita divisão por zero (caso a imagem esteja completamente preta ou branca)
    if moments["m00"] == 0:
        raise ValueError("Centro de massa não encontrado - momentos inválidos.")

    # Calcula a posição horizontal (cX) do centro de massa
    cX = moments["m10"] / moments["m00"]

    return cX

# Função para processar um frame e extrair informações de tempo e posição
def process_frame(frame, sec, time_list, position_list):
    try:
        binary_frame = binarize(frame)
        cX = centro_de_massa(binary_frame)
        time_list.append(f"{sec}\n")
        position_list.append(f"{cX * PIXEL_TO_CM}\n")
    except ValueError as e:
        print(f"Erro ao processar frame no tempo {sec}s: {e}")

# Função principal para processar o vídeo inteiro
def main():
    vidcap = cv.VideoCapture(VIDEO_FILE)  # Abre o vídeo
    if not vidcap.isOpened():
        print(f"Erro: Não foi possível abrir o vídeo {VIDEO_FILE}")
        return

    sec = 0  # Inicializa o tempo
    frame_contador = 0  # Contador de frames
    frame_intervalo = int(vidcap.get(cv.CAP_PROP_FPS) * FRAME_RATE)  # Intervalo entre frames a serem processados

    time_list = []  # Lista para armazenar os tempos
    position_list = []  # Lista para armazenar as posições

    ret = True  # Variável de controle do laço

    while ret:  # Continua enquanto o frame for lido corretamente
        # Tenta ler o próximo frame
        ret, frame = vidcap.read()

        # Processa o frame a cada intervalo de tempo definido
        if ret and frame_contador % frame_intervalo == 0:
            process_frame(frame, sec, time_list, position_list)
            sec = round(sec + FRAME_RATE, 2)  # Atualiza o tempo

        frame_contador += 1  # Incrementa o contador de frames

    vidcap.release()  # Libera o vídeo

    # Salva os dados de tempos e posições em arquivos
    with open(os.path.join(OUTPUT_DIR, "tempos.txt"), "w") as f_time:
        f_time.writelines(time_list)

    with open(os.path.join(OUTPUT_DIR, "espacos.txt"), "w") as f_space:
        f_space.writelines(position_list)


if __name__ == "__main__":
    main()
