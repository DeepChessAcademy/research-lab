# ♟️ DeepChessAcademy (DCA) - Core

Este repositório contém o pipeline de dados MLOps (`dca-core`) para o projeto "DeepChessAcademy".

O objetivo deste projeto é servir como um **plano de estudos prático e unificado** para preparação e aprovação nas seguintes certificações:

1.  **CompTIA DataX (DYO-001)**
2.  **Google Cloud Professional Machine Learning Engineer**

## 🚀 Módulos do Projeto (Currículo)

* **Módulo 1: O Pipeline de Dados (ETL) & QA**
    * *Assunto:* Operações de Dados, Python, Apache Beam, Testes de Unidade (Pytest), Logging, Refatoração.
    * *Status:* **Concluído**
* **Módulo 2: O Valor das Peças (Estatística e EDA)**
    * *Assunto:* Estatística Descritiva, Teste de Hipóteses (t-Test), EDA, Visualização (Seaborn), Dashboards (Streamlit).
    * *Status:* **Em Andamento**
* **Módulo 3: Vendo o Futuro (ML Clássico)**
    * *Assunto:* Modelos Supervisionados (Regressão Logística), Métricas.
    * *Status:* Pendente
* **Módulo 4: O Tabuleiro "Quente" (Feature Engineering)**
    * *Assunto:* Engenharia de Features, ML Não Supervisionado.
    * *Status:* Pendente
* **Módulo 5: A Mente Profunda (Deep Learning)**
    * *Assunto:* Redes Neurais (CNNs, RNNs), TensorFlow/Keras.
    * *Status:* Pendente
* **Módulo 6: A Engine em Produção (MLOps)**
    * *Assunto:* CI/CD, Orquestração de Pipeline, Monitoramento, APIs.
    * *Status:* Pendente

## 🛠️ Como Executar o Projeto

Este projeto tem duas partes executáveis: O Pipeline (Módulo 1) e o Painel de Análise (Módulo 2).

### 1. Ambiente de Execução (Necessário para ambos)

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/DeepChessAcademy/dca-core.git](https://github.com/DeepChessAcademy/dca-core.git)
    cd dca-core
    ```

2.  **Crie e ative o ambiente virtual:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

### 2. Módulo 1: Executar o Pipeline de ETL

Isto só precisa de ser executado uma vez para processar os seus dados de xadrez.

1.  Coloque o seu ficheiro `.pgn` descompactado em `data/raw/`.
2.  Confirme que o `INPUT_FILE` em `pipeline.py` aponta para este ficheiro.
3.  Execute o pipeline:
    ```bash
    python pipeline.py
    ```
    * A saída CSV será salva em `data/processed/`.

### 3. Módulo 2: Executar o Painel de Análise (Dashboard)

Isto inicia o seu painel web interativo para testar as hipóteses.

1.  **Pré-requisito:** Certifique-se de que o Módulo 1 já foi executado e o ficheiro `.csv` existe em `data/processed/`.
2.  Confirme que o `CSV_PATH` em `dashboard.py` aponta para o seu ficheiro `.csv`.
3.  Execute o Streamlit:
    ```bash
    streamlit run dashboard.py
    ```
    * O seu navegador será aberto automaticamente com o painel interativo.

## 🧪 Como Executar os Testes (QA do Módulo 1)

Os testes de unidade validam a lógica de parsing do Módulo 1.

1.  **Execute todos os testes:**
    ```bash
    pytest
    ```
