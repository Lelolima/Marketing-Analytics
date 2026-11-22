# Auditoria — Marketing-Analytics — 2026-11-22

## Estado anterior
- 1 script (`marketing-pipeline-advanced.py`) e README. Sem testes, sem CI (`gh run list` vazio), sem requirements.
- README mandava executar `etl_pipeline_code.py` (arquivo inexistente) e instalar só `pandas sqlalchemy`.
- Dados 100% simulados (`np.random`), sem aviso no README.

## Problemas encontrados

| # | Sev. | Problema | Evidência |
|---|---|---|---|
| 1 | P0 | Script não completa: `plt.style.use('seaborn')` lança `OSError` (estilo removido no matplotlib ≥ 3.6) | execução real com matplotlib 3.11.2: `OSError: 'seaborn' is not a valid package style` |
| 2 | P1 | Fórmula de `score_potencial` com precedência errada: `1 - (dias/30)*0.2` em vez de `(1 - dias/30)*0.2`. Score ia até 1,8 e nunca ficava abaixo de 0,8 → **todo lead caía em "Premium"** | teste `test_score_valores_conhecidos` antes da correção: `[1.8, 0.8]` em vez de `[1.0, 0.0]` |
| 3 | P2 | Figuras do matplotlib nunca fechadas; `open()` sem encoding (acentos no JSON/config no Windows) | leitura do código |
| 4 | P2 | Sem testes, sem CI, sem requirements; README infiel | — |
| 5 | Info | `data_source`, `export_path` e o parâmetro `source` não são usados | leitura do código; documentado no README |

Segredos: nenhum encontrado (busca por padrões de chave/token/senha em todo o histórico, `git log -p --all`).
Gitleaks não está instalado nesta máquina; a busca foi manual por regex.
Vulnerabilidades: `pip-audit -r requirements.txt` → "No known vulnerabilities found".

## Mudanças
- Estilo `seaborn-v0_8`, `plt.close()` após salvar, `encoding='utf-8'` em leitura/escrita.
- Correção da precedência do `score_potencial` (pesos 0,4/0,4/0,2 somam 1, coerente com os limiares 0,8/0,5).
- `json.dump` com conversor de tipos numpy (defensivo; com pandas 3.1 as contagens já saem como `int`, então
  não reproduzi falha nesse ponto).
- `requirements.txt` (versões fixadas e testadas), `requirements-dev.txt`, `ruff.toml` (E9 + pyflakes), `.gitignore`.
- 4 testes (`tests/test_pipeline.py`) e CI (`ruff`, `compileall`, `pytest`; `permissions: contents: read`; actions fixadas por SHA).
- README reescrito conforme a implementação.

## Testes executados (Windows, Python 3.12)
- Antes da correção: `pytest -q tests` → 3 failed, 1 passed (OSError do estilo; score 1,8).
- Depois: `pytest -q tests` → **4 passed**; `ruff check .` → All checks passed.
- Execução real `python marketing-pipeline-advanced.py` (via teste ponta a ponta) gera DB, JSON e 2 PNG.

## Riscos residuais / decisões do dono
- A correção do score muda a distribuição dos segmentos (antes todos "Premium"). É o comportamento coerente com os
  pesos, mas confirme a regra de negócio.
- Extração continua simulada; ligar `data_source` a um CSV real é decisão do dono.
- Sobreposição de domínio com `Advanced-Marketing-ML-Pipeline` (não unificado).
- Não há arquivo LICENSE.
