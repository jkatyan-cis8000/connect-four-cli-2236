"""Game manager - handles game state and move validation."""

from src.types.board import Board, Cell
from src.types.game import Player, GameResult
from src.types.io import ColumnChoice
from src.service.board_logic import (
    create_empty_board, drop_disc, check_winner, is_board_full
)


class GameManager:
    """Manages the state of a Connect Four game."""
    
    def __init__(self):
        """Initialize a new game."""
        self._board: Board = create_empty_board()
        self._current_player: Player = Player.RED
        self._game_over: bool = False
        self._winner: Player | None = None
    
    def get_board(self) -> Board:
        """Return the current board state."""
        return self._board
    
    def current_player(self) -> Player:
        """Return the player whose turn it is."""
        return self._current_player
    
    def is_valid_move(self, col: ColumnChoice) -> bool:
        """Check if a move is valid (column has space)."""
        from src.config.constants import MIN_COLUMN, MAX_COLUMN
        
        if col < MIN_COLUMN or col > MAX_COLUMN:
            return False
        
        # Convert to 0-indexed column
        col_idx = col - 1
        from src.service.board_logic import get_valid_row
        return get_valid_row(self._board, col_idx) is not None
    
    def make_move(self, col: ColumnChoice) -> GameResult | None:
        """Execute a move and return the game result if game is over.
        
        Args:
            col: Column choice (1-indexed)
        
        Returns:
            GameResult if game ended, None otherwise
        """
        if self._game_over:
            return GameResult(self._winner, self._winner is None)
        
        # Convert to 0-indexed column
        col_idx = col - 1
        
        # Drop the disc
        new_board, row = drop_disc(self._board, col_idx, self._current_player)
        
        if row is None:
            # Column is full - invalid move
            return None
        
        self._board = new_board
        
        # Check for win
        if check_winner(self._board, row, col_idx, self._current_player):
            self._game_over = True
            self._winner = self._current_player
            return GameResult(self._current_player, False)
        
        # Check for draw
        if is_board_full(self._board):
            self._game_over = True
            return GameResult(None, True)
        
        # Switch turns
        self._current_player = (
            Player.YELLOW if self._current_player == Player.RED 
            else Player.RED
        )
        
        return None
