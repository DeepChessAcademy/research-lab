# Changelog

Todo o progresso notável neste projeto será documentado aqui.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] - Módulo 1 - 2025-11-06

O Módulo 1 está concluído. O pipeline de ETL está funcional, robusto e validado por testes de unidade.

### Adicionado
* Configuração do ambiente local com `Python 3.11` e `venv`.
* Estrutura de pastas profissional (`data/raw`, `data/processed`).
* Pipeline de ETL (`pipeline.py`) usando `Apache Beam` (`DirectRunner`) para processamento em lote.
* Lógica de parsing (`parser.py`) capaz de processar ficheiros PGN massivos do Lichess.
* Sistema de logging robusto para depuração (console) e auditoria (`pipeline.log`).
* Configuração de documentação do repositório (`LICENSE`, `README.md`, `CHANGELOG.md`).
* Configuração de controlo de versão (`.gitignore`) para ignorar caches, dados e ficheiros de ambiente.

### Alterado
* **Refatoração de QA:** A lógica de parsing foi movida de `pipeline.py` para `parser.py` para permitir testes de unidade (baixo acoplamento).
* `pipeline.py` agora serve como o orquestrador principal do pipeline.

### Corrigido (QA)
* **Teste de Unidade Adicionado:** Criado `test_parser.py` com `pytest` para validar a lógica de parsing.
* **Bug Encontrado:** O teste falhou, identificando um bug na contagem de lances (`game.ply()`).
* **Bug Corrigido:** Lógica de contagem de lances em `parser.py` corrigida para `len(list(game.mainline_moves()))`.
* **Teste Corrigido:** Dados de teste em `test_parser.py` atualizados para refletir os valores corretos.
* **Sucesso:** O teste de unidade (`pytest`) agora passa, validando a lógica de ETL.

### Pendente
* Início do **Módulo 2**, focando em Análise Exploratória de Dados (EDA) no dataset CSV gerado.