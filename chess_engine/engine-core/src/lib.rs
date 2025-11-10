/*
 * FEN Validator, Parser, and Zobrist Hashing Library
 * * This package is now both a library (rlib) AND a WASM module (cdylib).
 * * Many structs and functions are now `pub` to be used by `cli-demo`.
 */

use wasm_bindgen::prelude::*;
use serde::{Serialize, Deserialize};
use std::fmt;
use rand::{Rng, SeedableRng, rngs::StdRng};
use once_cell::sync::Lazy;

// --- 1. Crate Setup & Panic Hook ---

#[wasm_bindgen(start)]
pub fn main_js() {
    #[cfg(debug_assertions)]
    console_error_panic_hook::set_once();
}

// --- 2. Core Data Structures (Now public) ---

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
pub enum Color { // ADDED `pub`
    White,
    Black,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
pub enum PieceType { // ADDED `pub`
    Pawn,
    Knight,
    Bishop,
    Rook,
    Queen,
    King,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
pub struct Piece { // ADDED `pub`
    pub color: Color, // ADDED `pub`
    pub piece_type: PieceType, // ADDED `pub`
}

/// Represents the entire state of the chessboard.
#[derive(Debug, Clone, Serialize)]
pub struct BoardState { // ADDED `pub`
    // A 64-square representation, 0=a1, 7=h1, ..., 63=h8
    pub board: [Option<Piece>; 64], // ADDED `pub`
    pub side_to_move: Color, // ADDED `pub`
    // Bitflags for castling: 1=WK, 2=WQ, 4=BK, 8=BQ
    pub castling_rights: u8, // ADDED `pub`
    // The square index (0-63) of a potential en passant target.
    pub en_passant_target: Option<u8>, // ADDED `pub`
    pub halfmove_clock: u32, // ADDED `pub`
    pub fullmove_number: u32, // ADDED `pub`
}

// --- 3. Zobrist Hashing ---

const ZOBRIST_SEED: u64 = 0xDEADBEEFCAFEBABE;

/// Holds the precomputed random keys for Zobrist hashing.
struct ZobristKeys {
    // [piece_type][color][square]
    pieces: [[[u64; 64]; 2]; 6], // 6 piece types, 2 colors, 64 squares
    black_to_move: u64,
    // [castling_rights_mask] - 16 possible combinations
    castling: [u64; 16],
    // [file_index] - 8 possible files for en passant
    en_passant_file: [u64; 8],
}

/// Lazily initializes Zobrist keys using `once_cell`.
static KEYS: Lazy<ZobristKeys> = Lazy::new(generate_zobrist_keys);

/// Generates a full set of pseudo-random 64-bit keys.
fn generate_zobrist_keys() -> ZobristKeys {
    // ... (same code as before, no changes) ...
    let mut rng = StdRng::seed_from_u64(ZOBRIST_SEED);
    let mut keys = ZobristKeys {
        pieces: [[[0; 64]; 2]; 6],
        black_to_move: rng.gen(),
        castling: [0; 16],
        en_passant_file: [0; 8],
    };

    for pt_idx in 0..6 { // PieceType
        for c_idx in 0..2 { // Color
            for sq_idx in 0..64 { // Square
                keys.pieces[pt_idx][c_idx][sq_idx] = rng.gen();
            }
        }
    }

    for i in 0..16 {
        keys.castling[i] = rng.gen();
    }

    for i in 0..8 {
        keys.en_passant_file[i] = rng.gen();
    }

    keys
}

// BoardState methods are now public
impl BoardState {
    /// Calculates the Zobrist hash for the current board state.
    pub fn calculate_zobrist_hash(&self) -> u64 { // ADDED `pub`
        let mut hash: u64 = 0;

        // 1. Piece positions
        for (sq_idx, piece_opt) in self.board.iter().enumerate() {
            if let Some(piece) = piece_opt {
                let pt_idx = piece.piece_type as usize;
                let c_idx = piece.color as usize;
                hash ^= KEYS.pieces[pt_idx][c_idx][sq_idx];
            }
        }

        // 2. Side to move
        if self.side_to_move == Color::Black {
            hash ^= KEYS.black_to_move;
        }

        // 3. Castling rights
        hash ^= KEYS.castling[self.castling_rights as usize];

        // 4. En passant target
        if let Some(ep_square) = self.en_passant_target {
            let ep_file = (ep_square % 8) as usize;
            hash ^= KEYS.en_passant_file[ep_file];
        }

        hash
    }

    /// Helper to convert board to a simple ASCII representation for display.
    pub fn to_ascii(&self) -> String { // ADDED `pub`
        // ... (same code as before, no changes) ...
        let mut s = String::new();
        s.push_str("+---+---+---+---+---+---+---+---+\n");
        for r in (0..8).rev() { // From rank 8 down to 1
            s.push('|');
            for f in 0..8 { // From file a to h
                let sq_idx = (r * 8 + f) as usize;
                let piece_char = match self.board[sq_idx] {
                    Some(Piece { color: Color::White, piece_type: PieceType::Pawn }) => 'P',
                    Some(Piece { color: Color::White, piece_type: PieceType::Knight }) => 'N',
                    Some(Piece { color: Color::White, piece_type: PieceType::Bishop }) => 'B',
                    Some(Piece { color: Color::White, piece_type: PieceType::Rook }) => 'R',
                    Some(Piece { color: Color::White, piece_type: PieceType::Queen }) => 'Q',
                    Some(Piece { color: Color::White, piece_type: PieceType::King }) => 'K',
                    Some(Piece { color: Color::Black, piece_type: PieceType::Pawn }) => 'p',
                    Some(Piece { color: Color::Black, piece_type: PieceType::Knight }) => 'n',
                    Some(Piece { color: Color::Black, piece_type: PieceType::Bishop }) => 'b',
                    Some(Piece { color: Color::Black, piece_type: PieceType::Rook }) => 'r',
                    Some(Piece { color: Color::Black, piece_type: PieceType::Queen }) => 'q',
                    Some(Piece { color: Color::Black, piece_type: PieceType::King }) => 'k',
                    None => ' ',
                };
                s.push(' ');
                s.push(piece_char);
                s.push(' ');
                s.push('|');
            }
            s.push('\n');
            s.push_str("+---+---+---+---+---+---+---+---+\n");
        }
        s
    }
}

// --- 4. FEN Parsing and Error Handling ---

/// Custom error types for FEN validation.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum FenError { // Already `pub`
    InvalidFormat(String),
    InvalidPartCount(usize),
    InvalidRank(usize, String),
    InvalidRankLength(usize, usize),
    InvalidPiece(usize, char),
    InvalidSideToMove(String),
    InvalidCastling(String),
    InvalidEnPassant(String),
    InvalidHalfmoveClock(String),
    InvalidFullmoveNumber(String),
    ValidationKingCount(String),
    ValidationPawnPosition(String),
}

// Implement `Display` for `FenError` to get nice error messages.
impl fmt::Display for FenError {
    // ... (same code as before, no changes) ...
    fn fmt(&self, f: &mut fmtD::Formatter) -> fmt::Result {
        match self {
            FenError::InvalidFormat(s) => write!(f, "Invalid FEN format: {}", s),
            FenError::InvalidPartCount(n) => write!(f, "Invalid FEN: Expected 6 parts, found {}", n),
            FenError::InvalidRank(r, s) => write!(f, "Invalid FEN rank {}: {}", 8 - r, s),
            FenError::InvalidRankLength(r, l) => write!(f, "Invalid FEN rank {}: Expected length 8, got {}", 8 - r, l),
            FenError::InvalidPiece(r, c) => write!(f, "Invalid FEN rank {}: Invalid piece character '{}'", 8 - r, c),
            FenError::InvalidSideToMove(s) => write!(f, "Invalid side to move: '{}'. Expected 'w' or 'b'.", s),
            FenError::InvalidCastling(s) => write!(f, "Invalid castling string: '{}'. Expected '-' or 'KQkq'.", s),
            FenError::InvalidEnPassant(s) => write!(f, "Invalid en passant square: '{}'.", s),
            FenError::InvalidHalfmoveClock(s) => write!(f, "Invalid halfmove clock: '{}'. Not a number.", s),
            FenError::InvalidFullmoveNumber(s) => write!(f, "Invalid fullmove number: '{}'. Not a number.", s),
            FenError::ValidationKingCount(s) => write!(f, "Position validation failed: {}", s),
            FenError::ValidationPawnPosition(s) => write!(f, "Position validation failed: {}", s),
        }
    }
}

/// The main parsing logic, now public for `cli-demo`
pub fn parse_fen(fen: &str) -> Result<BoardState, FenError> { // ADDED `pub`
    let fen_trimmed = fen.trim();
    let parts: Vec<&str> = fen_trimmed.split_whitespace().collect();

    if parts.len() != 6 {
        return Err(FenError::InvalidPartCount(parts.len()));
    }
    
    // ... (same parsing code as before, no changes) ...
    let mut board: [Option<Piece>; 64] = [None; 64];
    let mut white_kings = 0;
    let mut black_kings = 0;

    // --- Part 1: Piece Placement ---
    let ranks: Vec<&str> = parts[0].split('/').collect();
    if ranks.len() != 8 {
        return Err(FenError::InvalidFormat("Expected 8 ranks separated by '/'.".into()));
    }

    for (r_idx, rank_str) in ranks.iter().enumerate() {
        let mut file: usize = 0;
        let rank = 7 - r_idx; // FEN starts from rank 8 (index 0) down to 1 (index 7)

        for c in rank_str.chars() {
            if file >= 8 {
                return Err(FenError::InvalidRankLength(r_idx, file));
            }

            let sq_idx = (rank * 8 + file) as usize;

            match c {
                'P' => {
                    if rank == 0 || rank == 7 { return Err(FenError::ValidationPawnPosition("White pawn on 1st or 8th rank.".into())); }
                    board[sq_idx] = Some(Piece { color: Color::White, piece_type: PieceType::Pawn });
                    file += 1;
                },
                'N' => { board[sq_idx] = Some(Piece { color: Color::White, piece_type: PieceType::Knight }); file += 1; },
                'B' => { board[sq_idx] = Some(Piece { color: Color::White, piece_type: PieceType::Bishop }); file += 1; },
                'R' => { board[sq_idx] = Some(Piece { color: Color::White, piece_type: PieceType::Rook }); file += 1; },
                'Q' => { board[sq_idx] = Some(Piece { color: Color::White, piece_type: PieceType::Queen }); file += 1; },
                'K' => {
                    board[sq_idx] = Some(Piece { color: Color::White, piece_type: PieceType::King });
                    white_kings += 1;
                    file += 1;
                },
                'p' => {
                    if rank == 0 || rank == 7 { return Err(FenError::ValidationPawnPosition("Black pawn on 1st or 8th rank.".into())); }
                    board[sq_idx] = Some(Piece { color: Color::Black, piece_type: PieceType::Pawn });
                    file += 1;
                },
                'n' => { board[sq_idx] = Some(Piece { color: Color::Black, piece_type: PieceType::Knight }); file += 1; },
                'b' => { board[sq_idx] = Some(Piece { color: Color::Black, piece_type: PieceType::Bishop }); file += 1; },
                'r' => { board[sq_idx] = Some(Piece { color: Color::Black, piece_type: PieceType::Rook }); file += 1; },
                'q' => { board[sq_idx] = Some(Piece { color: Color::Black, piece_type: PieceType::Queen }); file += 1; },
                'k' => {
                    board[sq_idx] = Some(Piece { color: Color::Black, piece_type: PieceType::King });
                    black_kings += 1;
                    file += 1;
                },
                '1'..='8' => {
                    let empty_count = c.to_digit(10).unwrap() as usize;
                    if file + empty_count > 8 {
                        return Err(FenError::InvalidRank(r_idx, format!("Rank skips past 8th file with '{}'", c)));
                    }
                    file += empty_count;
                },
                _ => return Err(FenError::InvalidPiece(r_idx, c)),
            }
        }
        if file != 8 {
            return Err(FenError::InvalidRankLength(r_idx, file));
        }
    }

    // Basic Validation
    if white_kings != 1 { return Err(FenError::ValidationKingCount(format!("Expected 1 white king, found {}", white_kings))); }
    if black_kings != 1 { return Err(FenError::ValidationKingCount(format!("Expected 1 black king, found {}", black_kings))); }
    
    // --- Part 2: Side to Move ---
    let side_to_move = match parts[1] {
        "w" => Color::White,
        "b" => Color::Black,
        _ => return Err(FenError::InvalidSideToMove(parts[1].into())),
    };

    // --- Part 3: Castling Rights ---
    let mut castling_rights: u8 = 0;
    if parts[2] != "-" {
        for c in parts[2].chars() {
            match c {
                'K' => castling_rights |= 1,
                'Q' => castling_rights |= 2,
                'k' => castling_rights |= 4,
                'q' => castling_rights |= 8,
                _ => return Err(FenError::InvalidCastling(parts[2].into())),
            }
        }
    }

    // --- Part 4: En Passant Target ---
    let en_passant_target = if parts[3] == "-" {
        None
    } else {
        let chars: Vec<char> = parts[3].chars().collect();
        if chars.len() != 2 {
            return Err(FenError::InvalidEnPassant(parts[3].into()));
        }
        let file = (chars[0] as u8).wrapping_sub(b'a');
        let rank = (chars[1] as u8).wrapping_sub(b'1');

        if file > 7 || rank > 7 {
            return Err(FenError::InvalidEnPassant(parts[3].into()));
        }

        // Basic validation: EP square must be on rank 3 or 6.
        if (side_to_move == Color::White && rank != 5) || (side_to_move == Color::Black && rank != 2) {
             return Err(FenError::InvalidEnPassant(format!("Square {} is not a valid en passant target for {} to move.", parts[3], parts[1])));
        }
        
        Some(rank * 8 + file)
    };

    // --- Part 5: Halfmove Clock ---
    let halfmove_clock = parts[4].parse::<u32>()
        .map_err(|_| FenError::InvalidHalfmoveClock(parts[4].into()))?;

    // --- Part 6: Fullmove Number ---
    let fullmove_number = parts[5].parse::<u32>()
        .map_err(|_| FenError::InvalidFullmoveNumber(parts[5].into()))?;
    if fullmove_number == 0 {
        return Err(FenError::InvalidFullmoveNumber("Fullmove number cannot be 0.".into()));
    }

    Ok(BoardState {
        board,
        side_to_move,
        castling_rights,
        en_passant_target,
        halfmove_clock,
        fullmove_number,
    })
}

// --- 5. WASM Interface (No changes, but now uses the public `parse_fen` function) ---

/// The data structure returned to JS on success.
#[derive(Serialize)]
struct SuccessResponse {
    fen: String,
    board_ascii: String,
    zobrist_hash: String, // As hex string
    state: BoardState,
}

/// The data structure returned to JS on failure.
#[derive(Serialize)]
struct ErrorResponse {
    fen: String,
    error_type: String,
    message: String,
}

/// The WASM entry point function.
/// Note: The Rust function is named `parse_fen_for_wasm` to avoid
/// confusion with the public `parse_fen`, but we keep the
/// JS name as `parse_fen_and_get_hash` for the web UI.
#[wasm_bindgen(js_name = parse_fen_and_get_hash)] // KEEPS the JS name `parse_fen_and_get_hash`
pub fn parse_fen_for_wasm(fen: &str) -> Result<JsValue, JsValue> {
    // Calls the main Rust function
    match parse_fen(fen) {
        Ok(board_state) => {
            let hash = board_state.calculate_zobrist_hash();
            let ascii = board_state.to_ascii();

            let response = SuccessResponse {
                fen: fen.to_string(),
                board_ascii: ascii,
                zobrist_hash: format!("{:016x}", hash), // Format as 16-char hex
                state: board_state,
            };
            
            Ok(JsValue::from_serde(&response).unwrap())
        },
        Err(e) => {
            let response = ErrorResponse {
                fen: fen.to_string(),
                error_type: format!("{:?}", e),
                message: e.to_string(),
            };
            
            Err(JsValue::from_serde(&response).unwrap())
        }
    }
}