/*
 * FEN Parser CLI Demo
 * * This is a command-line executable that uses the `engine-core` library.
 * * How to use (from the `chess_engine` directory):
 * cargo run -p cli-demo -- "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
 * * The '--' is important to separate Cargo's arguments from our program's arguments.
 */

use engine_core::{parse_fen, BoardState, FenError}; // Import public items from our 'engine-core'
use std::env; // To read command-line arguments

fn main() {
    // Collect command-line arguments
    let args: Vec<String> = env::args().collect();

    // Check if a FEN was provided.
    // args[0] is the program name, args[1] is the first argument.
    if args.len() < 2 {
        eprintln!("Error: No FEN string provided.");
        eprintln!("Usage: cargo run -p cli-demo -- \"<FEN_STRING>\"");
        std::process.exit(1);
    }

    let fen_str = &args[1];

    println!("Attempting to parse FEN: \"{}\"", fen_str);
    println!("-------------------------------------------------");

    // Call the parse function from our library
    match parse_fen(fen_str) {
        Ok(board_state) => {
            // Success!
            let hash = board_state.calculate_zobrist_hash();
            let ascii = board_state.to_ascii();

            println!("Parse Succeeded!");
            println!("\n{}", ascii); // Print the ASCII board
            
            println!("Zobrist Hash: {:016x}", hash); // Print the hash in hex
            println!("Side to Move: {:?}", board_state.side_to_move);
            println!("Castling:     {}", format_castling(board_state.castling_rights));
            println!("En Passant:   {}", format_en_passant(board_state.en_passant_target));
            println!("Halfmove:     {}", board_state.halfmove_clock);
            println!("Fullmove:     {}", board_state.fullmove_number);
        }
        Err(e) => {
            // Error!
            eprintln!("Error parsing FEN: {}", e);
            std::process.exit(1_i32);
        }
    }
}

// Helper functions for formatting
fn format_castling(rights: u8) -> String {
    let mut s = String::new();
    if (rights & 1) != 0 { s.push('K'); }
    if (rights & 2) != 0 { s.push('Q'); }
    if (rights & 4) != 0 { s.push('k'); }
    if (rights & 8) != 0 { s.push('q'); }
    if s.is_empty() { "-".to_string() } else { s }
}

fn format_en_passant(target: Option<u8>) -> String {
    match target {
        Some(sq) => {
            let rank = (sq / 8) + 1;
            let file = (sq % 8) as u8 + b'a';
            format!("{}{}", file as char, rank)
        }
        None => "-".to_string(),
    }
}