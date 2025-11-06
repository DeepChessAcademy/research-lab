import chess.pgn
import logging
import apache_beam as beam

class ParsePgnFile(beam.DoFn):
    """
    Esta classe recebe um CAMINHO DE FICHEIRO como entrada (self, file_path)
    e emite (yield) um dicionário para CADA JOGO encontrado nesse ficheiro.
    """
    def process(self, file_path):
        logging.info(f"Iniciando processamento do ficheiro: {file_path}")
        game_count = 0
        failed_count = 0 # --- MELHORIA DE AUDITORIA ---
        
        try:
            # Usamos 'open' normal. O Beam gere isso.
            with open(file_path, encoding='utf-8') as f:
                
                # Este é o loop mágico da biblioteca python-chess
                while True:
                    # --- MELHORIA DE DEBUGAÇÃO (TRY INTERNO) ---
                    try:
                        game = chess.pgn.read_game(f)
                    except Exception as e:
                        logging.warning(f"Falha ao ler um jogo (jogo corrompido?). Erro: {e}")
                        failed_count += 1
                        continue # Pula para o próximo jogo
                    # --- FIM DA MELHORIA ---

                    # Se 'game' for None, o ficheiro acabou.
                    if game is None:
                        break
                    
                    # Processa os dados
                    info = {
                        'resultado': game.headers.get('Result'),
                        'rating_brancas': game.headers.get('WhiteElo'),
                        'rating_pretas': game.headers.get('BlackElo'),
                        
                        # --- CORREÇÃO DO BUG ---
                        # game.ply() não era fiável.
                        # Contamos explicitamente os lances da linha principal.
                        'total_lances': len(list(game.mainline_moves()))
                    }
                    
                    # 'yield' emite este jogo como um item 
                    # separado no pipeline
                    yield info
                    game_count += 1

        except Exception as e:
            # Este erro agora é mais sério (ex: ficheiro não encontrado)
            logging.error(f"Erro fatal ao processar {file_path}: {e}")
            
        # --- MELHORIA DE AUDITORIA (LOG DETALHADO) ---
        logging.info(f"Processamento concluído: {game_count} jogos parseados com sucesso.")
        if failed_count > 0:
            logging.warning(f"Auditoria: {failed_count} jogos falharam no parseamento (ver logs 'WARNING').")