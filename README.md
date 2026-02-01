
Este repositório está organizado em **módulos independentes**, cada um responsável por uma simulação ou análise específica:

## Módulos

### Colisões

Simulação estocástica de partículas em um ambiente fechado, com visualização interativa diretamente no terminal.

### Massa–Mola

Modelagem dinâmica de sistemas massa–mola, incluindo osciladores acoplados e entrada de parâmetros via teclado.

### Análise de Pêndulo

Análise experimental de um pêndulo físico utilizando:

-   Rastreamento do centro de massa com OpenCV
    
-   Processamento de dados
    
-   Ajuste de curva exponencial
    
-   Geração de gráficos
    

----------

# Como Executar (via Docker)

Para garantir que todas as dependências funcionem corretamente (como **OpenCV**, **curses** e **SciPy**), a execução deve ser feita via **Docker Compose**.

Certifique-se de ter o Docker e o Docker Compose instalados antes de prosseguir.

----------

## 1. Simulação de Colisões

Executa a simulação com interface interativa no terminal:

`docker-compose run colisoes` 

----------

## 2. Sistema Massa–Mola

Executa o simulador de oscilações.  
Durante a execução, será necessário inserir os parâmetros do sistema via teclado.

`docker-compose run massa-mola` 

----------

## 3. Análise Experimental do Pêndulo

Processa o vídeo experimental, realiza o ajuste matemático e gera os arquivos de dados e gráficos.

`docker-compose run pendulo` 

### Saída dos Resultados

Os gráficos e arquivos gerados pelo módulo do pêndulo serão salvos em:

`aps_pendulo/output/`
