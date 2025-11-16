# ext_parser.py
"""
Módulo extensor para parsing de PGNs anotados (v2).

Este parser agora extrai:
1. Metadados do Jogo (Headers: WhiteElo, Opening, etc.)
2. Dados por Lance (Eval, CLK, FEN)
3. Anotações do Lichess (Blunder, Mistake, Best Move, etc.)
"""

import chess.pgn
import io
import re
import pandas as pd
from typing import Iterator, Dict, Any, Optional

def _convert_eval_to_cp(eval_str: str) -> Optional[int]:
    """Converte uma string de avaliação (ex: "+0.45", "#-3") para centipawns."""
    if not isinstance(eval_str, str):
        return None
        
    if eval_str.startswith('#'):
        try:
            mate_in = int(eval_str[1:])
            # Valor de mate: 100000 - (N lances * 100)
            if mate_in > 0:
                return 100000 - (mate_in * 100) # Mate a favor
            else:
                return -100000 + (abs(mate_in) * 100) # Mate contra
        except ValueError:
            return None # Ex: "#" sem número
    try:
        # Avaliação normal (ex: "-1.23")
        return int(float(eval_str) * 100)
    except (ValueError, TypeError):
        return None

def _extract_comment_data(comment: str) -> Dict[str, Any]:
    """
    Extrai dados de [%eval], [%clk] e anotações de texto (Blunder, etc.)
    """
    data = {
        'eval_str': None,
        'clk_time': None,
        'classification': None,
        'eval_change_str': None,
        'suggested_best_move': None,
        'annotation_text': None
    }
    
    if not comment:
        return data

    # 1. Extrair [%eval ...]
    eval_match = re.search(r'\[%eval\s+([#\+\-0-9\.]+)]', comment)
    if eval_match:
        data['eval_str'] = eval_match.group(1)

    # 2. Extrair [%clk ...]
    clk_match = re.search(r'\[%clk\s+([\d:\.]+)]', comment)
    if clk_match:
        data['clk_time'] = clk_match.group(1)
        
    # 3. Extrair anotações das "entrelinhas" (ex: Blunder, Mistake)
    # Ex: { (-0.25 → -5.12) Blunder. Ne2 was best. }
    
    # Remove as tags de colchetes para facilitar a busca do texto
    plain_comment = re.sub(r'\[%.*?\]', '', comment).strip()
    data['annotation_text'] = plain_comment if plain_comment else None
    
    # 3a. Classificação (Blunder, Mistake, Inaccuracy)
    class_match = re.search(r'\)\s*([A-Za-z]+)\.', plain_comment)
    if class_match:
        data['classification'] = class_match.group(1)
        
    # 3b. Mudança de Eval (ex: "-0.25 → -5.12" ou "Mate in 3 → -1.48")
    change_match = re.search(r'\(\s*([^→]+)\s*→\s*([^\)]+)\s*\)', plain_comment)
    if change_match:
        data['eval_change_str'] = f"{change_match.group(1).strip()} → {change_match.group(2).strip()}"

    # 3c. Melhor Lance
    best_match = re.search(r'\.\s*([A-Za-z\d\+\#\=]+)\s+was best', plain_comment)
    if best_match:
        data['suggested_best_move'] = best_match.group(1)
        
    return data

def parse_annotated_pgn(pgn_content: str) -> Iterator[Dict[str, Any]]:
    """
    Analisa o conteúdo de um PGN anotado e gera um dicionário por lance,
    incluindo os metadados do jogo em cada linha.
    
    Args:
        pgn_content: O conteúdo textual completo do arquivo PGN.

    Yields:
        Um dicionário contendo dados do lance E dados do header do jogo.
    """
    pgn_file = io.StringIO(pgn_content)
    game = chess.pgn.read_game(pgn_file)
    
    if not game:
        return

    # 1. Extrair Metadados (Headers)
    # Adicionamos todos os headers a cada linha de lance
    game_headers = dict(game.headers)
    
    # Garante que campos comuns existam, mesmo que vazios
    common_headers = [
        "GameId", "Event", "Site", "Date", "White", "Black", "Result", 
        "WhiteElo", "BlackElo", "Variant", "TimeControl", "ECO", "Opening", 
        "Termination", "Annotator"
    ]
    base_data = {h: game_headers.get(h, None) for h in common_headers}
    base_data["GameId"] = game_headers.get("GameId", game_headers.get("Site", "Unknown_ID").split('/')[-1])


    board = game.board()
    
    # Avaliação da posição inicial
    root_comment_data = _extract_comment_data(game.comment)
    last_eval_cp = _convert_eval_to_cp(root_comment_data.get('eval_str')) or 0

    for i, node in enumerate(game.mainline()):
        move = node.move
        move_san = board.san(move)
        player_turn = "White" if board.turn == chess.WHITE else "Black"
        
        # 1. Obter dados do comentário (avaliação APÓS este lance)
        comment_data = _extract_comment_data(node.comment)
        eval_after_move_cp = _convert_eval_to_cp(comment_data.get('eval_str'))
        
        cp_loss = 0
        
        if eval_after_move_cp is not None:
            # Lógica de CP Loss (Assume que eval é sempre POV das Brancas)
            if player_turn == "White":
                # CP Loss (Brancas) = (eval anterior) - (eval atual)
                cp_loss = last_eval_cp - eval_after_move_cp
            else: # Player é "Black"
                # CP Loss (Pretas) = (eval atual) - (eval anterior)
                cp_loss = eval_after_move_cp - last_eval_cp
                
            # Atualiza a avaliação para o próximo loop
            last_eval_cp = eval_after_move_cp
        else:
            # Se a eval estiver faltando, não podemos calcular o CP Loss
            # Apenas resetamos a 'last_eval' para a eval do lance anterior
            # (ou mantemos, pois não há nova info)
            pass 
        
        # 3. Preparar dados específicos do lance
        move_specific_data = {
            "move_number": board.fullmove_number,
            "ply": i + 1,
            "player": player_turn,
            "move_san": move_san,
            "eval_cp_pov_white": eval_after_move_cp,
            "centipawn_loss": max(0, cp_loss), # CP Loss não pode ser negativo
            "time_on_clock": comment_data.get('clk_time'),
            "fen_before_move": board.fen(),
            "classification": comment_data.get('classification'),
            "eval_change_str": comment_data.get('eval_change_str'),
            "suggested_best_move": comment_data.get('suggested_best_move'),
            "raw_annotation": comment_data.get('annotation_text')
        }
        
        # Combina metadados do jogo com dados do lance
        yield {**base_data, **move_specific_data}
        
        # Executa o lance no tabuleiro interno para o próximo loop
        board.push(move)
