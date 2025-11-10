Rust/WASM FEN Parser Project (Workspace)

This project is a Rust "workspace" containing two packages, located within the chess_engine directory.

engine-core: The main library that handles FEN parsing and Zobrist hashing.

cli-demo: A command-line executable that uses engine-core.

New File Structure

The entire engine workspace is now contained within the chess_engine/ subdirectory:

DeepChessAcademy/
├── README.md (Your main project README)
│
└── chess_engine/       <-- (NEW PROJECT ROOT)
    ├── Cargo.toml          <-- (Defines the workspace)
    ├── index.html          <-- (Web demo UI)
    ├── BUILDING.md         <-- (These build instructions)
    │
    ├── cli-demo/
    │   ├── Cargo.toml
    │   └── src/
    │       └── main.rs
    │
    └── engine-core/
        ├── Cargo.toml
        └── src/
            └── lib.rs


Prerequisites

Rust: https://www.rust-lang.org/tools/install

wasm-pack: cargo install wasm-pack

Local Web Server (e.g., Python)

How to Run the CLI Demo (Command-Line)

IMPORTANT: All commands must now be run from the chess_engine/ directory.

Open your terminal and navigate into the project folder:

cd DeepChessAcademy/chess_engine


Use cargo run specifying the package (-p) cli-demo.

Use -- to separate Cargo's arguments from your program's arguments.

Example with starting FEN:

# Make sure you are inside the 'chess_engine' directory!
cargo run -p cli-demo -- "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


Example with an error FEN:

# Make sure you are inside the 'chess_engine' directory!
cargo run -p cli-demo -- "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq"


How to Run the Web Demo (WASM)

IMPORTANT: All commands must now be run from the chess_engine/ directory.

Navigate to the Directory:

cd DeepChessAcademy/chess_engine


Build the WASM:
From the chess_engine/ folder, run wasm-pack pointing to the engine-core directory:

# Make sure you are inside the 'chess_engine' directory!
wasm-pack build ./engine-core --target web


This will create engine-core/pkg/. The index.html file (which is in the same directory) is already configured to look there.

Serve the Project:
Start your web server from the chess_engine/ folder:

# Make sure you are inside the 'chess_engine' directory!
python -m http.server 8000


View in Browser:
Open http://localhost:8000.