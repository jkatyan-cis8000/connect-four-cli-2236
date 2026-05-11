"""Game types - Player enum and GameResult class."""

from enum import Enum
from typing import Optional


class Player(Enum):
    """Represents a player in the game."""
    RED = 'Red'
    YELLOW = 'Yellow'


class GameResult:
    """Represents the result of a game."""
    winner: Optional['Player']
    is_draw: bool

    def __init__(self, winner: Optional[Player] = None, is_draw: bool = False):
        self.winner = winner
        self.is_draw = is_draw

    def __eq__(self, other):
        if not isinstance(other, GameResult):
            return False
        return self.winner == other.winner and self.is_draw == other.is_draw

    def __repr__(self):
        if self.is_draw:
            return "GameResult(draw)"
        elif self.winner:
            return f"GameResult(winner={self.winner.value})"
        return "GameResult(ongoing)"
