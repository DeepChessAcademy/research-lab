# Changelog

Todo o progresso notável neste projeto será documentado aqui.
O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Em Andamento] - Módulo 3 (Treino de ML)

### Adicionado
* Script `train.py` que executa o primeiro ciclo de MLOps (treino, avaliação, serialização).
* Reutilização da função `carregar_e_limpar_dados()` do `eda.py` (boas práticas).
* Avaliação de métricas de classificação (Acurácia, Precisão, Recall, F1) (CompTIA 3.3).
* Serialização (gravação) do modelo treinado (`model_v1.joblib`) usando `joblib`.
* Adicionada pasta `models/` e ficheiros `*.joblib` ao `.gitignore`.

## [1.1.0] - Módulo 2 (EDA & Dashboard) - 2025-11-09

### Adicionado
* Painel de Análise (`dashboard.py`) com `Streamlit`.
* Módulo de Análise (`eda.py`) com 8 funções de hipótese (H1-H8).
* Novas Dependências: `streamlit`, `seaborn`, `scipy`, `scikit-learn`.
* Engenharia de Features: `Rating_Diferencial`, `Resultado_Binario`, etc.

## [1.0.0] - Módulo 1 (Pipeline ETL Estável) - 2025-11-06

### Adicionado
* Pipeline de ETL (`pipeline.py`) com `Apache Beam`.
* Lógica de parsing (`parser.py`) e testes de unidade (`test_parser.py`).
* Sistema de logging robusto (`pipeline.log`).

### Corrigido (Estabilidade do Pipeline)
* **(QA) Bug Lógico:** Corrigida a contagem de lances em `parser.py`.
* **(Pipeline) `TypeError`:** Substituído `beam.FlatMap` por `beam.ParDo`.
* **(Pipeline) `DEADLINE_EXCEEDED`:** Aumentado o timeout do `DirectRunner` para `600s`.
