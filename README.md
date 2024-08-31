# Chess AI

This project is a Python-based Chess AI with a graphical user interface built using Pygame. The AI leverages a Minimax algorithm with Alpha-Beta pruning and various heuristics to evaluate moves and simulate a challenging opponent. The system supports all standard chess rules and provides real-time move validation and game state detection.

## Features

- **Human vs. AI Gameplay: Play against an AI that adapts its strategy based on your moves.
- **Minimax Algorithm: Utilizes Minimax with Alpha-Beta pruning for optimal move decision-making.
- **Heuristic Evaluation: Incorporates material count, piece positioning, mobility, and more to evaluate board states.
- **Full Chess Rule Support: Implements castling, en passant, and pawn promotion.
- **Real-Time Validation: Ensures all moves are legal and detects check, checkmate, and stalemate conditions.

## Installation

To set up and run the system, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/jgottlieb11/chess-ai.git
    cd chess-ai
    ```

2. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the system**:
    ```bash
    python gui/gui.py
    ```

## Gameplay

- **Use your mouse to select and move pieces.
- **The AI will automatically make its move after you complete yours.
- **The game will detect and notify you of check, checkmate, or stalemate.
