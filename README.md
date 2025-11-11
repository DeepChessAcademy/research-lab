# ♟️ DeepChessAcademy (DCA) - MLOps & Chess AI

Este repositório serve como um portfólio prático de ponta a ponta, documentando a jornada de construção de um ecossistema de Machine Learning para análise de xadrez.

O objetivo principal é aplicar os conceitos das certificações **CompTIA DataX (DYO-001)** e **Google Cloud ML Engineer (GCP-MLE)** num problema do mundo real.

## 🚀 A Arquitetura do Ecossistema

O projeto é dividido em dois sistemas complementares que imitam uma arquitetura MLOps moderna:

### 1. Sistema de "Batch": O Pipeline MLOps (`dca-core`)
* **Propósito:** Processamento em lote de *dados históricos* (milhões de jogos).
* **Função:** Treinar e avaliar modelos de ML que aprendem padrões a partir de dados em repouso.
* **Foco (Exames):** Mapeia diretamente para **CompTIA DataX (Pipelines, ETL, Análise)** e **GCP-MLE (MLOps, Data Pipelines)**.

### 2. Sistema de "Real-Time": A Engine de Inferência (`dca-chess-engine`)
* **Propósito:** Análise interativa de *dados em tempo real* (uma posição de tabuleiro).
* **Função:** Servir os modelos treinados (do Sistema 1) e aplicar algoritmos de xadrez (como Zobrist Hashing) para avaliação imediata.
* **Foco (Exames):** Mapeia para **GCP-MLE (Software Engineering, Model Serving)** e os fundamentos de CS necessários para construir sistemas de ML complexos.

---

## 🧭 O Currículo (Módulos do Projeto)

Cada módulo abaixo representa um passo no currículo, ligando uma necessidade do projeto a um domínio do exame.

### Sistema 1: O Pipeline MLOps (Batch)

#### Módulo 1: O Pipeline de Dados (ETL) & QA
* **Propósito:** Ingerir, analisar (parse), limpar e estruturar dados de PGN.
* **Syllabus:** **CompTIA 2.0 (Data Pipelines)**, **CompTIA 4.1 (QA)**.
* **Entregável:** `pipeline.py` (com Apache Beam) e `test_parser.py` (com `pytest`).
* **Status:** ✅ Concluído

#### Módulo 2: O Valor das Peças (EDA & Dashboard)
* **Propósito:** Análise Exploratória de Dados (EDA) para validar hipóteses e descobrir *features* (preditores).
* **Syllabus:** **CompTIA 3.0 (Data Analysis & Visualization)**.
* **Entregável:** `dashboard.py` (com Streamlit) e `eda.py`.
* **Status:** ✅ Concluído

#### Módulo 3: Vendo o Futuro (ML Clássico)
* **Propósito:** Treinar um primeiro modelo (Regressão Logística) para provar o conceito. Inclui treino, avaliação e serialização.
* **Syllabus:** **CompTIA 3.2 (Modeling)**, **CompTIA 3.3 (Model Evaluation)**.
* **Entregável:** `train.py` e o artefato `model_v1.joblib`.
* **Status:** ✅ Concluído

#### Módulo 4: O Tabuleiro "Quente" (Feature Engineering)
* **Propósito:** Ir além da simples "diferença de rating" e criar *features* complexas (ex: "contagem de peças", "estrutura de peões").
* **Syllabus:** **CompTIA 3.1 (Feature Engineering)**.
* **Entregável:** (Pendente) Versão v2 do pipeline de treino.
* **Status:** ⏳ Pendente

---

### Sistema 2: A Engine de Inferência (Real-time)

#### Módulo 5: A Engine (Algoritmos & Parsing FEN)
* **Propósito:** Construir as fundações de uma engine de xadrez, incluindo um parser FEN e Zobrist Hashing para deteção de transposição.
* **Syllabus:** **GCP-MLE (Software Engineering Best Practices)**, **Fundamentos de Algoritmos** (necessários para pesquisa de árvores).
* **Entregável:** Módulo `zobrist.js` e a ferramenta de análise `test_zobrist.html`.
* **Status:** ✅ Concluído

#### Módulo 6: O Oráculo (Deep Learning & Transformers)
* **Propósito:** Substituir o modelo de ML Clássico (M3) por um modelo de Deep Learning (Transformer) que possa ser alimentado por uma interface UCI.
* **Syllabus:** **GCP-MLE (Build & Use ML Models)**, **GCP-MLE (ML Model Serving)**.
* **Entregável:** (Pendente) Interface UCI e o modelo Transformer treinado.
* **Status:** ⏳ Pendente

---

## 🛠️ Como Executar os Componentes

### 1. Pipeline MLOps (Módulos 1-3)

(Requer Python, `venv`, e `requirements.txt`)

```bash
# Módulo 1: Executar o Pipeline de ETL
python pipeline.py

# Módulo 2: Executar o Painel de Análise
streamlit run dashboard.py

# Módulo 3: Treinar o Modelo
python train.py

# 1. Inicie um servidor local no diretório
python -m http.server

# 2. Abra o browser e navegue para:
# http://localhost:8000/test_zobrist.html
```
