import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import logging
import sys

# --- IMPORTAÇÃO DA LÓGICA DE NEGÓCIO ---
# Importamos a nossa classe 'DoFn' refatorada do ficheiro parser.py
from parser import ParsePgnFile
# --------------------------------------

# 1. Crie uma pasta 'data/raw/' e coloque seu ficheiro PGN massivo nela
# NOME DO ARQUIVO GRANDE HARDCODED:
INPUT_FILE = 'data/raw/lichess_db_standard_rated_2013-01.pgn'
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
        runner='DirectRunner', # "Corra localmente"
        # CORREÇÃO A2.2: Aumenta o timeout para 600 segundos (10 minutos) 
        # para evitar o DEADLINE_EXCEEDED no DirectRunner.
        direct_runner_service_checkout_timeout_seconds=600 
    )

    # 4. O Pipeline
    logging.info("Iniciando o pipeline local (Beam DirectRunner)...")

    with beam.Pipeline(options=options) as p:
        (p
         # Início: Um PCollection com um único item: o nome do ficheiro
         | 'Start' >> beam.Create([INPUT_FILE])
         
         # Aplica nosso "operário" ParsePgnFile (importado do parser.py)
         # CORREÇÃO A1: beam.FlatMap alterado para beam.ParDo (o transformador correto para DoFn)
         | 'Parse Games' >> beam.ParDo(ParsePgnFile())
         
         # Converte o dicionário para uma string CSV
         | 'Format to CSV' >> beam.Map(lambda x: f"{x['resultado']},{x['rating_brancas']},{x['rating_pretas']},{x['total_lances']}")
         
         # Escreve a saída em um ou mais ficheiros CSV
         # O 'header' força a primeira linha a ter os nomes das colunas
         | 'Write CSV' >> beam.io.WriteToText(
             OUTPUT_FILE, 
             file_name_suffix='.csv',
             header='resultado,rating_brancas,rating_pretas,total_lances'
           )
        )
    logging.info("pipeline done!")


if __name__ == '__main__':
    run_pipeline()
