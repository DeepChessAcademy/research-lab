# ♟️ DeepChessAcademy (DCA)

Este repositório contém o código-fonte do projeto "DeepChessAcademy", uma iniciativa para construir um motor de análise de xadrez do zero, usando-o como uma ferramenta de aprendizado para dominar conceitos de Engenharia de Dados, Estatística, Machine Learning e MLOps.

## 🎯 Objetivo Principal

O objetivo deste projeto não é apenas construir uma IA de xadrez, mas servir como um **plano de estudos prático e unificado** para preparação e aprovação nas seguintes certificações:

1.  **CompTIA DataX (DYO-001)**
2.  **Google Cloud Professional Machine Learning Engineer**

Cada módulo do projeto é mapeado para domínios de conhecimento específicos desses exames.

## 🚀 Módulos do Projeto (Currículo)

O projeto é dividido em 6 módulos que seguem a Taxonomia de Bloom, do mais simples ao mais complexo:

* **Módulo 1: O Pipeline de Dados (ETL) & QA**
    * *Assunto:* Operações de Dados, Programação (Python, Apache Beam), Testes de Unidade (Pytest), Logging, Refatoração.
    * *Status:* **Concluído**
* **Módulo 2: O Valor das Peças (Estatística e EDA)**
    * *Assunto:* Estatística Descritiva, Teste de Hipóteses, EDA, BigQuery ML.
    * *Status:* Pendente
* **Módulo 3: Vendo o Futuro (ML Clássico)**
    * *Assunto:* Modelos Supervisionados (Regressão Logística, Árvores, XGBoost), Métricas de Classificação.
    * *Status:* Pendente
* **Módulo 4: O Tabuleiro "Quente" (Feature Engineering)**
    * *Assunto:* Engenharia de Features, ML Não Supervisionado (Clustering, PCA), Vertex AI Feature Store.
    * *Status:* Pendente
* **Módulo 5: A Mente Profunda (Deep Learning)**
    * *Assunto:* Cálculo, Redes Neurais (CNNs, RNNs), TensorFlow/Keras, Vertex AI Training (GPUs/TPUs).
    * *Status:* Pendente
* **Módulo 6: A Engine em Produção (MLOps)**
    * *Assunto:* CI/CD, Orquestração de Pipeline (Vertex AI Pipelines), Monitoramento de Drift, APIs (Cloud Run).
    * *Status:* Pendente

## 🛠️ Como Executar o Projeto (Módulo 1)

Este projeto usa **Python 3.11** e **Apache Beam**.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/DeepChessAcademy.git](https://github.com/seu-usuario/DeepChessAcademy.git)
    cd DeepChessAcademy
    ```

2.  **Crie e ative o ambiente virtual:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

4.  **Execute o pipeline de dados principal:**
    * *Pré-requisito:* Baixe um ficheiro `.pgn` (ex: do Lichess, e **descomprima-o**).
    * Coloque o ficheiro em `data/raw/` (ex: `data/raw/lichess_export.pgn`).
    * Confirme que o `INPUT_FILE` em `pipeline.py` aponta para este ficheiro.
    * Execute o pipeline:
    ```bash
    python pipeline.py
    ```
    * A saída CSV estruturada será salva em `data/processed/`.
    * Os logs de auditoria serão salvos em `pipeline.log`.

## 🧪 Como Executar os Testes (QA)

O projeto está configurado com testes de unidade para garantir a qualidade do código.

1.  **Execute todos os testes:**
    (Certifique-se de que o seu `venv` está ativado e as dependências de teste estão instaladas via `requirements.txt`)
    ```bash
    pytest
    ```

2.  **Gere o Relatório de Cobertura (Opcional):**
    Para ver um relatório HTML de quais linhas de código os testes cobriram:
    ```bash
    pytest --cov=parser
    ```
    * Abra o ficheiro `htmlcov/index.html` no seu navegador para ver o relatório.