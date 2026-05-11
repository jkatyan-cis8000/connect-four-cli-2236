"""CLI UI - rendering and user input."""

from src.types.board import Board, Cell
from src.types.game import Player
from src.types.io import ColumnChoice
from src.service.game_manager import GameManager


def render_board(board: Board) -> str:
    """Render the board as an ASCII string.
    
    Includes column numbers at the bottom.
    """
    lines = []
    
    # Render each row
    for row in board:
        row_str = '|' + '|'.join(cell.value for cell in row) + '|'
        lines.append(row_str)
    
    # Add separator
    lines.append('-' * (len(board[0]) * 2 + 1))
    
    # Add column numbers
    col_numbers = ' ' + ' '.join(str(i) for i in range(1, len(board[0]) + 1))
    lines.append(col_numbers)
    
    return '\n'.join(lines)


def get_column_input() -> ColumnChoice:
    """Prompt user for a column choice (1-7)."""
    while True:
        try:
            choice = input("Enter column (1-7): ").strip()
            col = int(choice)
            if 1 <= col <= 7:
                return col
            print("Please enter a number between 1 and 7.")
        except ValueError:
            print("Please enter a valid number.")


def play_game():
    """Main game loop."""
    from src.types.game import GameResult
    
    game = GameManager()
    
    print("Welcome to Connect Four!")
    print("Player RED goes first. Enter column numbers 1-7 to drop discs.")
    print()
    
    while True:
        print(render_board(game.get_board()))
        print(f"\nPlayer {game.current_player().value}'s turn")
        
        col = get_column_input()
        
        if not game.is_valid_move(col):
            print("Column is full! Choose another.")
            continue
        
        result = game.make_move(col)
        
        if result:
            print(render_board(game.get_board()))
            if result.is_draw:
                print("\nGame ended in a draw!")
            else:
                print(f"\nPlayer {result.winner.value} wins!")
            break
    
    print("\nThanks for playing!")
