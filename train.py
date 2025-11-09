# train.py
import pandas as pd
import logging
import joblib # Biblioteca para salvar/carregar modelos
from eda import carregar_e_limpar_dados # REUTILIZAMOS o nosso módulo de EDA!
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# --- Configuração ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Constantes
CSV_PATH = 'data/processed/pipeline_output-00000-of-00001.csv' # CONFIRME O NOME
MODEL_PATH = 'models/model_v1.joblib' # Onde vamos salvar o nosso primeiro modelo

def treinar_modelo():
    """
    Função principal para carregar dados, treinar o modelo e salvá-lo.
    """
    
    # 1. Carregar Dados (Reutilizando o Módulo 2)
    logging.info("Carregando e limpando dados...")
    df = carregar_e_limpar_dados(CSV_PATH)
    
    if df is None:
        logging.error("Carga de dados falhou. Abortando treino.")
        return

    # 2. Preparar Features (X) e Alvo (y)
    # (CompTIA 3.1 - Modelagem)
    logging.info("Preparando features e alvo...")
    
    # Usamos as features que provamos serem úteis no Módulo 2
    X = df[['Rating_Diferencial']]
    y = df['Resultado_Binario']

    # 3. Dividir Dados (Treino e Teste)
    # (CompTIA 3.3 - Avaliação)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    logging.info(f"Dados divididos: {len(X_train)} para treino, {len(X_test)} para teste.")

    # 4. Treinar o Modelo
    # (CompTIA 3.2 - Regressão Logística)
    logging.info("Treinando o modelo de Regressão Logística...")
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    logging.info("Treino concluído.")

    # 5. Avaliar o Modelo
    # (CompTIA 3.3 - Métricas de Classificação)
    logging.info("Avaliando o modelo...")
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print("\n--- Métricas de Avaliação (Módulo 3) ---")
    print(f"  Acurácia (Accuracy): {accuracy:.4f}")
    print(f"  Precisão (Precision): {precision:.4f}")
    print(f"  Recall: {recall:.4f}")
    print(f"  F1-Score: {f1:.4f}")
    print("----------------------------------------\n")

    # 6. Salvar (Serializar) o Modelo
    # (Base do MLOps)
    logging.info(f"Salvando o modelo treinado em {MODEL_PATH}...")
    joblib.dump(model, MODEL_PATH)
    logging.info("Modelo salvo com sucesso!")

if __name__ == "__main__":
    treinar_modelo()