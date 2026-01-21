Esta solução foi projetada para monitorar a performance e qualidade dos enriquecimentos de dados da plataforma HubDriva. Ela consiste em uma pipeline automatizada que transforma dados brutos em insights analíticos.

Ambiente Docker: 

Orquestra PostgreSQL, n8n, API e Frontend em containers isolados para garantir portabilidade.

Pipeline de Dados (n8n): 

Um fluxo orquestrador roda a cada 5 minutos , realizando a ingestão (API para Bronze) e o processamento (Bronze para Gold).

Data Warehouse Camadas:

Bronze: Armazena os registros brutos com carimbos de data de ingestão e atualização.

Gold: Contém dados limpos, traduzidos para o português e enriquecidos com cálculos de performance e sucesso.

API & Dashboard: 

Uma API centraliza o acesso aos dados da camada Gold , alimentando um dashboard frontend que exibe KPIs e métricas de processamento.




Para subir o ambiente, utilize o comando docker compose build seguido de docker compose up -d dentro da pasta que esta o Docker Compose




Para subir o frontend, utilize o comando python -m http.server 8000, e na guia pesquise por localhost:8000




Importação dos Workflows
Acesse a interface do n8n em http://localhost:5678.

No menu lateral, clique em Workflows.

Selecione a opção Import from File e escolha os arquivos JSON fornecidos no repositório.

Você deve importar os três workflows obrigatórios: Data Injestion, Processing e o Scheduler.

2. Configuração Inicial
Certifique-se de que as credenciais do PostgreSQL e as URLs da API (http://api:3000) estejam configuradas corretamente dentro dos nós de cada workflow.

Verifique se o header de autenticação contém a API Key: Bearer driva_test_key_abc123xyz789.

3. Execução

Execução Manual: Para testar imediatamente, abra o workflow desejado e clique no botão Execute Workflow no rodapé da página.

O fluxo seguirá a ordem: Ingestão de dados (API → Bronze) e, em seguida, Processamento (Bronze → Gold).




1. Endpoint de Fonte (Ingestão)
Simula a API de enriquecimentos que o n8n deve consumir para popular a camada Bronze.

curl -X GET "http://localhost:3000/people/v1/enrichments?page=1&limit=50" \
     -H "Authorization: Bearer driva_test_key_abc123xyz789"


2. Analytics Overview (KPIs)
Retorna o total de jobs, a taxa de sucesso e o tempo médio de processamento direto da camada Gold.
curl -X GET "http://localhost:3000/analytics/overview" \
     -H "Authorization: Bearer driva_test_key_abc123xyz789"

