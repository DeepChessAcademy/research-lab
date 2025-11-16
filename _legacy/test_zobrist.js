<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Zobrist Hash Teste & Analisador</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        pre { font-family: monospace; white-space: pre-wrap; }
        .test-log { border: 1px solid #ccc; padding: 10px; margin-top: 20px; }
        .pass { color: green; }
        .fail { color: red; font-weight: bold; }
        .log { color: #555; }
        
        /* --- Novas Styles para o Analisador Interativo --- */
        #interactive-tester {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #000;
        }
        #fenInput {
            width: 100%;
            padding: 8px;
            font-family: monospace;
            box-sizing: border-box; /* Para o padding não quebrar o layout */
        }
        #analyzeButton {
            padding: 10px 15px;
            margin: 10px 0;
            font-size: 16px;
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
        }
        #board-container {
            display: grid;
            grid-template-columns: repeat(8, 50px);
            grid-template-rows: repeat(8, 50px);
            width: 400px;
            height: 400px;
            border: 2px solid #333;
        }
        .square {
            width: 50px;
            height: 50px;
            font-size: 38px;
            display: flex;
            align-items: center;
            justify-content: center;
            user-select: none; /* Impede a seleção do texto das peças */
        }
        .square.light { background-color: #f0d9b5; }
        .square.dark  { background-color: #b58863; }
        .piece {
            /* Unicode de peças de xadrez tem alinhamentos diferentes, isto ajuda a centrar */
            transform: translateY(-2px); 
        }
        #validation-output {
            margin-top: 10px;
            font-weight: bold;
        }
        #zobrist-output {
            font-family: monospace;
            word-break: break-all;
            background: #eee;
            padding: 10px;
            margin-top: 10px;
        }

    </style>
</head>
<body>
    <h1>Zobrist Hash Teste & Analisador</h1>

    <div id="interactive-tester">
        <h2>Analisador de FEN</h2>
        <p>Insira um FEN string para validar, ver o tabuleiro e calcular o hash Zobrist.</p>
        
        <label for="fenInput">FEN String:</label>
        <input type="text" id="fenInput" value="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1">
        <button id="analyzeButton">Analisar</button>
        
        <div id="validation-output"></div>
        
        <div style="display: flex; gap: 20px; margin-top: 20px;">
            <div id="board-container">
                </div>
            <div>
                <h3>Hash Zobrist (BigInt)</h3>
                <pre id="zobrist-output"></pre>
            </div>
        </div>
    </div>


    <div class="test-log">
        <h2>Test Suite Automático</h2>
        <div id="log-container"></div>
    </div>

    <script type="module">
        import { initZobristKeys, generateZobristHash } from './zobrist.js';

        // --- Mapa de Peças Unicode ---
        const PIECE_UNICODE = {
            'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚',
            'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔'
        };

        // --- Novo: Validador de FEN ---
        // Este regex é um validador de FEN bastante robusto
        const FEN_REGEX = /^([rnbqkpRNBQKP1-8]{1,8}\/){7}[rnbqkpRNBQKP1-8]{1,8}\s[wb]\s(-|K?Q?k?q?)\s(-|[a-h][36])(\s\d+\s\d+)?$/;
        
        function validateFEN(fen) {
            // 1. Validação com Regex
            if (!FEN_REGEX.test(fen.trim())) {
                return { valid: false, error: "Formato FEN geral inválido." };
            }
            
            // 2. Validar a contagem de peças por rank
            const ranks = fen.split(' ')[0].split('/');
            for (let i = 0; i < ranks.length; i++) {
                let count = 0;
                for (const char of ranks[i]) {
                    if (/\d/.test(char)) {
                        count += parseInt(char, 10);
                    } else {
                        count++;
                    }
                }
                if (count !== 8) {
                    return { valid: false, error: `Rank ${8-i} (string: ${ranks[i]}) não soma 8 casas.` };
                }
            }
            
            return { valid: true };
        }
        
        // --- Novo: Renderizador de Tabuleiro ---
        function renderBoard(fen) {
            const boardContainer = document.getElementById('board-container');
            boardContainer.innerHTML = ''; // Limpa o tabuleiro anterior
            
            const boardStr = fen.split(' ')[0];
            let rank = 7;
            let file = 0;

            // Cria 64 casas (invisíveis por enquanto)
            const squares = [];
            for (let r = 0; r < 8; r++) {
                for (let f = 0; f < 8; f++) {
                    const square = document.createElement('div');
                    square.className = (r + f) % 2 === 0 ? 'square light' : 'square dark';
                    squares.push(square);
                }
            }

            // Preenche as casas com peças
            for (const char of boardStr) {
                if (char === '/') {
                    rank--;
                    file = 0;
                } else if (/\d/.test(char)) {
                    file += parseInt(char, 10);
                } else {
                    // É uma peça
                    const squareIndex = (7 - rank) * 8 + file;
                    if (squares[squareIndex]) {
                        squares[squareIndex].innerHTML = `<span class="piece">${PIECE_UNICODE[char] || '?'}</span>`;
                    }
                    file++;
                }
            }
            
            // Adiciona todas as 64 casas ao container
            squares.forEach(square => boardContainer.appendChild(square));
        }

        // --- Novo: Lógica do Botão "Analisar" ---
        function analyzeFenFromInput() {
            const fen = document.getElementById('fenInput').value.trim();
            const validationEl = document.getElementById('validation-output');
            const zobristEl = document.getElementById('zobrist-output');
            const boardContainer = document.getElementById('board-container');

            const validation = validateFEN(fen);
            
            if (!validation.valid) {
                validationEl.textContent = `FEN Inválido: ${validation.error}`;
                validationEl.className = 'fail';
                zobristEl.textContent = '';
                boardContainer.innerHTML = ''; // Limpa o tabuleiro
                return;
            }

            // Se for válido...
            validationEl.textContent = 'FEN Válido!';
            validationEl.className = 'pass';
            
            // 1. Renderiza o tabuleiro
            renderBoard(fen);
            
            // 2. Calcula e mostra o Zobrist
            try {
                const hash = generateZobristHash(fen);
                zobristEl.textContent = `${hash}n`; // 'n' indica que é um BigInt
            } catch (e) {
                validationEl.textContent = `Erro no cálculo: ${e.message}`;
                validationEl.className = 'fail';
                zobristEl.textContent = '';
            }
        }

        
        // --- Setup Inicial ---
        const logContainer = document.getElementById('log-container');

        function log(type, message) {
            const el = document.createElement('div');
            el.className = type; // 'pass', 'fail', ou 'log'
            el.textContent = message;
            logContainer.appendChild(el);
        }

        function assert(condition, message) {
            if (condition) {
                log('pass', `✅ PASS: ${message}`);
            } else {
                log('fail', '❌ FAIL: ' + message);
                console.error(`Assertion falhou: ${message}`);
            }
            return condition;
        }

        // --- Ponto de Entrada Principal ---
        
        // 1. Inicializa o Módulo Zobrist
        log('log', 'Inicializando chaves Zobrist...');
        initZobristKeys();
        log('log', 'Chaves inicializadas.');
        
        // 2. Liga o botão "Analisar"
        document.getElementById('analyzeButton').addEventListener('click', analyzeFenFromInput);
        
        // 3. Executa a análise inicial (para o FEN padrão)
        analyzeFenFromInput();
        
        // 4. Executa o Test Suite automático
        log('log', 'Executando testes automáticos...');
        try {
            // FENs de teste
            const fenStart = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
            const fenStartBlack = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1";
            const fenE4 = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1";
            const fenNoCastle = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w kq - 0 1";
            
            // Teste 1: Consistência
            const hash1 = generateZobristHash(fenStart);
            const hash2 = generateZobristHash(fenStart);
            assert(hash1 === hash2, "O mesmo FEN produz o mesmo hash");
            assert(hash1 !== 0n, "Hash inicial não é zero");

            // Teste 2: Lado a Mover
            const hash3 = generateZobristHash(fenStartBlack);
            assert(hash1 !== hash3, "Mudar o lado a mover altera o hash");

            // Teste 3: Movimento de Peça
            const hash4 = generateZobristHash(fenE4);
            assert(hash1 !== hash4, "Mover uma peça altera o hash");
            assert(hash3 !== hash4, "Hashes de E4 e de 'Black move' são diferentes");

            // Teste 4: Direitos de Roque
            const hash5 = generateZobristHash(fenNoCastle);
            assert(hash1 !== hash5, "Mudar os direitos de roque altera o hash");

            // Teste 5: En Passant
            const fenNoEnPassant = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1";
            const hash6 = generateZobristHash(fenE4); // com e.p. e3
            const hash7 = generateZobristHash(fenNoEnPassant); // sem e.p.
            assert(hash6 !== hash7, "Mudar a casa de en passant altera o hash");

            // Teste 6: Transposição (O teste MAIS IMPORTANTE)
            // 1. e4 e5 2. Nf3 Nc6 (Brancas a mover)
            const fenTranspoA = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3";
            // 1. Nf3 Nc6 2. e4 e5 (Brancas a mover)
            const fenTranspoB = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3";
            
            assert(
                generateZobristHash(fenTranspoA) === generateZobristHash(fenTranspoB),
                "[Transposição] Posições idênticas de diferentes ordens de lances têm o mesmo hash"
            );

            log('log', '\n🎉 Todos os testes automáticos passaram!');
        } catch (e) {
            log('fail', `ERRO CRÍTICO NO TEST SUITE: ${e.message}`);
        }
    </script>
</body>
</html>
