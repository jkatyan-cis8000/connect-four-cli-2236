# ARCHITECTURE.md

Written by team-lead before spawning teammates. This is the shared blueprint —
teammates read it to understand what they are building and how their module fits.
Update it when the structure changes; do not let it drift from the actual code.

## Module Structure

- src/types/board.py: Board state (6x7 grid), Cell type (Empty, Red, Yellow)
- src/types/game.py: GameResult type (Win, Draw), Player type
- src/types/io.py: Input/Output types for user interaction
- src/config/constants.py: Game constants (rows=6, cols=7, win_length=4)
- src/service/board_logic.py: Board operations (drop disc, check win)
- src/service/game_manager.py: Game state, turn management, move validation
- src/ui/cli.py: CLI rendering, user input parsing, game loop
- src/runtime/__init__.py: App entry point, wires all layers together

## Interfaces

### types/board.py
- `Cell` enum: Empty, Red, Yellow
- `Board` class: 6x7 grid stored as list[list[Cell]]
- `Board.empty()` -> Board: Creates empty board

### types/game.py
- `Player` enum: Red, Yellow
- `GameResult` class: winner: Player | None, is_draw: bool

### types/io.py
- `ColumnChoice` type: int (1-indexed column number)

### service/board_logic.py
- `drop_disc(board: Board, col: int, player: Player) -> tuple[Board, int | None]`:
  Returns new board and row index where disc landed (None if column full)
- `check_winner(board: Board, last_row: int, last_col: int, player: Player) -> bool`:
  Checks for 4-in-a-row starting from last move

### service/game_manager.py
- `GameManager` class:
  - `__init__():` Creates new game state
  - `make_move(col: int) -> GameResult | None`: Returns result if game over
  - `current_player():` Returns Player whose turn it is
  - `is_valid_move(col: int) -> bool`: Checks if column has space
  - `get_board():` Returns current board state

### ui/cli.py
- `render_board(board: Board) -> str`: ASCII art board with column numbers
- `get_column_input() -> int`: Prompts user for column choice (1-7)
- `play_game():` Main game loop using GameManager

### runtime/__init__.py
- `main():` Entry point, calls ui.cli.play_game()

## Shared Data Structures

### Board
```python
Cell = Enum('Cell', ['Empty', 'Red', 'Yellow'])
Board = list[list[Cell]]  # 6 rows, 7 columns
# board[0] is top row, board[5] is bottom row
# board[row][col] where col is 0-6
```

### Game State
```python
Player = Enum('Player', ['Red', 'Yellow'])
# Red goes first

class GameResult:
    winner: Player | None  # None for draw
    is_draw: bool
```

### Input
```python
ColumnChoice = int  # 1-indexed: 1-7
```

## External Dependencies

- No external dependencies required. Uses only Python standard library.
