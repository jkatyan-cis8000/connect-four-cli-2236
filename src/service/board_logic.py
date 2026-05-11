"""Board logic - operations on the game board."""

from typing import Tuple, Optional

from src.types.board import Board, Cell
from src.types.game import Player
from src.config.constants import ROWS, COLS, WIN_LENGTH


def create_empty_board() -> Board:
    """Create a new empty board."""
    return [[Cell.EMPTY for _ in range(COLS)] for _ in range(ROWS)]


def get_valid_row(board: Board, col: int) -> Optional[int]:
    """Find the lowest empty row in a column.
    
    Returns the row index (0-5) or None if column is full.
    """
    if col < 0 or col >= COLS:
        return None
    
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == Cell.EMPTY:
            return row
    return None


def drop_disc(board: Board, col: int, player: Player) -> Tuple[Board, Optional[int]]:
    """Drop a disc into the specified column.
    
    Args:
        board: Current board state
        col: Column index (0-6)
        player: Player making the move
    
    Returns:
        Tuple of (new board, row index where disc landed, or None if column full)
    """
    if col < 0 or col >= COLS:
        return board, None
    
    row = get_valid_row(board, col)
    if row is None:
        return board, None
    
    # Create a copy of the board
    new_board = [row[:] for row in board]
    if player == Player.RED:
        new_board[row][col] = Cell.RED
    else:
        new_board[row][col] = Cell.YELLOW
    return new_board, row


def _cell_for_player(player: Player) -> Cell:
    """Convert Player to Cell."""
    if player == Player.RED:
        return Cell.RED
    return Cell.YELLOW


def check_line(board: Board, row: int, col: int, player: Player, 
               delta_row: int, delta_col: int) -> bool:
    """Check for a line of WIN_LENGTH starting from (row, col) in given direction."""
    target_cell = _cell_for_player(player)
    count = 0
    for i in range(WIN_LENGTH):
        r = row + i * delta_row
        c = col + i * delta_col
        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == target_cell:
            count += 1
        else:
            break
    return count == WIN_LENGTH


def check_winner(board: Board, last_row: int, last_col: int, player: Player) -> bool:
    """Check if the last move resulted in a win.
    
    Checks all four directions: horizontal, vertical, and two diagonals.
    """
    # Check horizontal
    if check_line(board, last_row, last_col, player, 0, 1):
        return True
    if check_line(board, last_row, last_col, player, 0, -1):
        return True
    
    # Check vertical
    if check_line(board, last_row, last_col, player, 1, 0):
        return True
    if check_line(board, last_row, last_col, player, -1, 0):
        return True
    
    # Check diagonal (down-right and up-left)
    if check_line(board, last_row, last_col, player, 1, 1):
        return True
    if check_line(board, last_row, last_col, player, -1, -1):
        return True
    
    # Check diagonal (down-left and up-right)
    if check_line(board, last_row, last_col, player, 1, -1):
        return True
    if check_line(board, last_row, last_col, player, -1, 1):
        return True
    
    return False


def is_board_full(board: Board) -> bool:
    """Check if the board is completely full."""
    for row in board:
        for cell in row:
            if cell == Cell.EMPTY:
                return False
    return True
