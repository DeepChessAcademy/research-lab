import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import logging
import sys

# --- IMPORTAÇÃO DA LÓGICA DE NEGÓCIO ---
# Importamos a nossa classe 'DoFn' refatorada do ficheiro parser.py
from parser import ParsePgnFile
# --------------------------------------

# 1. Crie uma pasta 'data/raw/' e coloque seu ficheiro PGN massivo nela
INPUT_FILE = 'data/raw/lichess_export.pgn'
OUTPUT_FILE = 'data/processed/pipeline_output'

# --- MELHORIA DE LOGGING (CONFIGURAÇÃO) ---
# A configuração do logging permanece no script principal (o orquestrador)
logging.basicConfig(
    level=logging.INFO,  # Nível mínimo para registar (INFO, WARNING, ERROR, etc.)
    format="%(asctime)s [%(levelname)s] %(message)s", # Formato: Data/Hora [NÍVEL] Mensagem
    handlers=[
        logging.FileHandler("pipeline.log"), # Para auditoria (grava em pipeline.log)
        logging.StreamHandler(sys.stdout)    # Para depuração (mostra na consola)
    ]
)
# --- FIM DA MELHORIA ---


def run_pipeline():
    """
    Define e corre o pipeline do Apache Beam.
    """
    # 3. Configurações do Pipeline (para correr localmente)
    options = PipelineOptions(
        runner='DirectRunner' # "Corra localmente"
    )

    # 4. O Pipeline
    logging.info("Iniciando o pipeline local (Beam DirectRunner)...")

    with beam.Pipeline(options=options) as p:
        (p
         # Início: Um PCollection com um único item: o nome do ficheiro
         | 'Start' >> beam.Create([INPUT_FILE])
         
         # Aplica nosso "operário" ParsePgnFile (importado do parser.py)
         | 'Parse Games' >> beam.FlatMap(ParsePgnFile())
         
         # Converte o dicionário para uma string CSV
         | 'Format to CSV' >> beam.Map(lambda x: f"{x['resultado']},{x['rating_brancas']},{x['rating_pretas']},{x['total_lances']}")
         
         # Escreve a saída em um ou mais ficheiros CSV
         | 'Write CSV' >> beam.io.WriteToText(OUTPUT_FILE, file_name_suffix='.csv', header='resultado,rating_brancas,rating_pretas,total_lances')
        )

    logging.info(f"Pipeline concluído. Saída salva em '{OUTPUT_FILE}-....csv'.")


# --- Ponto de Entrada do Script ---
if __name__ == '__main__':
    run_pipeline()