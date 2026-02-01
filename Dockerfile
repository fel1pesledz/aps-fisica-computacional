FROM python:3.10-slim

# Instala dependências de sistema (OpenCV e Interface de Terminal)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libncurses5-dev \
    libncursesw5-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala as bibliotecas Python necessárias para todos os projetos
RUN pip install --no-cache-dir numpy matplotlib scipy opencv-python

# Copia todos os seus projetos para dentro do container
COPY . .

# Por padrão, não faz nada (espera o comando do docker-compose)
CMD ["bash"]