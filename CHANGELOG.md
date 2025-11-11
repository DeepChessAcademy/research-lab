```markdown
# Changelog

Todo o progresso notável neste projeto será documentado aqui, alinhado com os módulos do currículo definidos no `README.md`.

## [Em Andamento] - Módulo 5 (Engine de Inferência)

### Adicionado - 2025-11-11
* **`DCA-Zobrist-JS`**: Migração da prova de conceito em Rust para Vanilla JavaScript.
* `zobrist.js`: Módulo ES6 para geração de hash Zobrist de 64 bits (com `BigInt` e `crypto.getRandomValues`).
* `test_zobrist.html`: Suite de testes automáticos e ferramenta de análise interativa.
* **Validação FEN**: Adicionada função de validação de FEN (com Regex) e renderizador de tabuleiro (com Unicode) à ferramenta de análise.
* **Mapeamento de Syllabus**: Este módulo estabelece a base para o **GCP-MLE (Software Engineering)** e o futuro Módulo 6 (Servir Modelos).

---

## [1.2.0] - Módulo 3 (ML Clássico) - 2025-11-10

### Adicionado
* `train.py`: Script para treinar, avaliar (Acurácia, Precisão, Recall, F1) e serializar (salvar) o primeiro modelo de ML (Regressão Logística).
* **`model_v1.joblib`**: Artefato do modelo treinado (ignorado pelo `.gitignore`).
* **Reutilização de Código**: `train.py` importa com sucesso a função `carregar_e_limpar_dados` do `eda.py`.
* **Mapeamento de Syllabus**: Conclui os objetivos do **CompTIA 3.2 (Modeling)** e **CompTIA 3.3 (Model Evaluation)**.

---

## [1.1.0] - Módulo 2 (EDA & Dashboard) - 2025-11-09

### Adicionado
* `dashboard.py`: Painel de Análise Exploratória de Dados (EDA) com `Streamlit`.
* `eda.py`: Módulo contendo 8 funções de análise de hipóteses (H1-H8).
* **Engenharia de Features (v1)**: `Rating_Diferencial` e `Resultado_Binario` provaram ser preditores viáveis.
* **Mapeamento de Syllabus**: Conclui os objetivos do **CompTIA 3.0 (Data Analysis & Visualization)**.

---

## [1.0.0] - Módulo 1 (Pipeline ETL & QA) - 2025-11-06

### Adicionado
* `pipeline.py`: Pipeline de ETL com `Apache Beam` para processar PGNs.
* `parser.py`: Lógica de parsing de PGN para extrair metadados e contagem de lances.
```
* `test_parser.py`: Testes de unidade com `pytest` para garantir a Qualidade dos Dados (QA).
* **Logging**: Sistema de logging robusto em `pipeline.log`.
* **Mapeamento de Syllabus**: Conclui os objetivos do **CompTIA 2.0 (Data Pipelines)** e **CompTIA 4.1 (QA)**.
