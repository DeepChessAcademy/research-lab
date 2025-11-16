import pytest
from parser import ParsePgnFile
import os

# 1. Crie um PGN de teste falso
PGN_TESTE = """
[Event "Jogo de Teste 1"]
[Result "1-0"]
[WhiteElo "1500"]
[BlackElo "1400"]

1. e4 e5 2. f4 1-0

[Event "Jogo de Teste 2"]
[Result "0-1"]
[WhiteElo "1600"]
[BlackElo "1700"]

1. d4 d5 0-1
"""

def test_parse_pgn_file():
    """
    Testa se o ParsePgnFile processa corretamente um ficheiro PGN
    com múltiplos jogos.
    """
    # 2. Configuração (Setup): Crie um ficheiro PGN de teste temporário
    test_filename = "test_data.pgn"
    with open(test_filename, "w") as f:
        f.write(PGN_TESTE)

    # 3. Defina a saída esperada - CORRIGIDO
    expected_output = [
        {'resultado': '1-0', 'rating_brancas': '1500', 'rating_pretas': '1400', 'total_lances': 3}, # Era 4
        {'resultado': '0-1', 'rating_brancas': '1600', 'rating_pretas': '1700', 'total_lances': 2}  # Era 4
    ]

    # 4. Execução (Act): Chame o *processador* do DoFn
    parser_dofn = ParsePgnFile()
    # beam.DoFn.process retorna um 'generator', então convertemos para lista
    results = list(parser_dofn.process(test_filename))

    # 5. Verificação (Assert): Verifique se a saída é a esperada
    assert len(results) == 2
    assert results == expected_output

    # 6. Limpeza (Teardown): Remova o ficheiro de teste
    os.remove(test_filename)
