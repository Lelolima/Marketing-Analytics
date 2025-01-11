# Marketing-Analytics

Este projeto implementa uma pipeline ETL (Extract, Transform, Load) em Python para análise de dados de leads em um contexto de marketing. Ele simula as etapas de extração, transformação e carregamento de dados, com foco em categorizar perfis, identificar padrões e fornecer insights relevantes para decisões estratégicas.

📜 Descrição do Projeto
A análise de leads é uma parte crucial para otimizar campanhas de marketing e personalizar abordagens. Este projeto automatiza o processamento desses dados usando um fluxo ETL que abrange:

Extração: Simulação de coleta de dados sobre perfis, idades e preferências de pagamento.
Transformação:
Categorização de perfis em grupos: Transição de carreira, Estudantes, e Sem experiência.
Segmentação etária em faixas: 18-25, 25-35, 35-55.
Identificação de desafios, como insegurança profissional e falta de experiência.
Classificação de objetivos, como melhoria salarial e mudança de área.
Carregamento: Persistência dos dados processados em um banco de dados SQLite para análises posteriores.
📊 Análises Realizadas
Categorização de Leads: Identifica os principais grupos para personalização de campanhas.
Segmentação Etária: Analisa a distribuição de idades e concentrações demográficas.
Aspectos Financeiros: Mapeia recursos disponíveis e preferências de pagamento.
Identificação de Desafios e Objetivos: Reconhece barreiras e metas dos leads.
🚀 Como Executar
Clone o repositório:

bash
Copiar código
git clone https://github.com/Lelolima/marketing-analytics.git
cd marketing-analytics
Instale os pacotes necessários:

bash
Copiar código
pip install pandas sqlalchemy
Execute o script:

bash
Copiar código
python etl_pipeline_code.py
🛠️ Tecnologias Utilizadas
Python: Linguagem de programação.
Pandas: Manipulação e análise de dados.
SQLAlchemy: Conexão e persistência de dados em banco de dados.
SQLite: Banco de dados relacional leve.
📈 Resultados Esperados
Após a execução do pipeline, os dados transformados estarão disponíveis em um banco de dados, prontos para análises e geração de relatórios.

📚 Próximos Passos
Integração com um dashboard em Power BI para visualização de insights.
Conexão com APIs externas para dados reais.
Automação de tarefas com agendadores (ex.: Apache Airflow).
