import importlib.util
import json
import pathlib

import matplotlib
import pytest

matplotlib.use("Agg")
ROOT = pathlib.Path(__file__).resolve().parents[1]


def _load():
    spec = importlib.util.spec_from_file_location("mp", ROOT / "marketing-pipeline-advanced.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def pipeline(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return _load().MarketingAnalyticsPipeline()


def test_score_potencial_fica_entre_0_e_1(pipeline):
    # pesos 0.4 + 0.4 + 0.2: o score nunca deve passar de 1
    df = pipeline.transform_data(pipeline.extract_data())
    assert df["score_potencial"].between(0, 1).all()


def test_score_valores_conhecidos(pipeline):
    import pandas as pd

    df = pd.DataFrame({
        "id": [1, 2], "idade": [20, 50], "perfil": ["Estudante", "Profissional"],
        "recursos_disponiveis": [True, False], "preferencia_pagamento": ["PIX", "Boleto"],
        "valor_investimento": [5000.0, 0.0], "tempo_decisao_dias": [0, 30],
    })
    out = pipeline.transform_data(df)
    assert out["score_potencial"].tolist() == pytest.approx([1.0, 0.0])
    assert out["segmento"].tolist() == ["Premium", "Básico"]


def test_pipeline_completa_gera_saidas(pipeline, tmp_path):
    pipeline.run_pipeline()
    rel = json.loads((tmp_path / "output" / "analysis_report.json").read_text(encoding="utf-8"))
    assert rel["total_leads"] == 100
    assert sum(rel["distribuicao_segmentos"].values()) == 100
    assert (tmp_path / "output" / "score_distribution.png").exists()
    assert (tmp_path / "marketing_analytics.db").exists()


def test_config_externa_sobrescreve_padrao(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    cfg = tmp_path / "cfg.json"
    cfg.write_text(json.dumps({"database_url": "sqlite:///outro.db"}), encoding="utf-8")
    p = _load().MarketingAnalyticsPipeline(str(cfg))
    assert p.config["database_url"] == "sqlite:///outro.db"
