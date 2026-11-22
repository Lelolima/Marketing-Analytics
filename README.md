# Marketing-Analytics

Pipeline ETL em Python (`marketing-pipeline-advanced.py`) para análise de leads de marketing: extrai, transforma,
segmenta, grava em SQLite e exporta um relatório JSON e gráficos.

> **Atenção: os dados são simulados.** `extract_data()` gera 100 leads aleatórios com `numpy` a cada execução
> (sem semente fixa). As chaves `data_source` e o parâmetro `source` existem na configuração/assinatura, mas **não são
> usados**: nenhum CSV ou API real é lido.

## Etapas implementadas

- **Extract**: 100 leads simulados (idade, perfil, recursos disponíveis, preferência de pagamento, valor de
  investimento, dias até a decisão).
- **Transform**:
  - código de categoria por perfil (`profile_mapping`: Transição de carreira→C1, Estudante→D1,
    Sem experiência→E1, Profissional→P1);
  - faixa etária: 18-25, 26-35, 36-45, 46-60;
  - `score_potencial` (0 a 1) = 0,4·recursos + 0,4·min(valor/5000, 1) + 0,2·(1 − dias/30);
  - segmento: Premium (≥ 0,8), Intermediário (≥ 0,5), Básico;
  - padronização (`StandardScaler`) de `valor_investimento` e `tempo_decisao_dias`.
- **Load**: tabela `leads_processed` no banco (`sqlite:///marketing_analytics.db` por padrão), relatório
  `output/analysis_report.json` e gráficos `output/score_distribution.png` e `output/age_value_relation.png`.

Não há identificação de "desafios" ou "objetivos" dos leads (citados em versões anteriores do README).

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt          # execução
pip install -r requirements-dev.txt      # + testes e lint
```

## Execução

```bash
python marketing-pipeline-advanced.py
```

Gera `marketing_pipeline.log`, `marketing_analytics.db` e a pasta `output/` no diretório atual.

### Configuração

Não há variáveis de ambiente nem segredos. É possível passar um JSON de configuração ao construtor
(`MarketingAnalyticsPipeline("config.json")`) para sobrescrever `database_url`, `export_path` ou `profile_mapping`.
Observação: `export_path` também não é usado hoje (a saída vai sempre para `output/`).

## Testes e lint

```bash
ruff check .
pytest -q tests
```

CI em `.github/workflows/ci.yml` (lint, compilação e testes).

## Relação com outros repositórios

`Advanced-Marketing-ML-Pipeline` trata do mesmo domínio (perfis de leads de cursos) com modelos de ML sobre dados
sintéticos. Os repositórios se sobrepõem, mas são independentes.
