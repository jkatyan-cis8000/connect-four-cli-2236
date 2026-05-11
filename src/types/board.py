"""Board types - Cell enum and Board data structure."""

from enum import Enum
from typing import List


class Cell(Enum):
    """Represents a cell state on the Connect Four board."""
    EMPTY = ' '
    RED = 'R'
    YELLOW = 'Y'


# Board is a 6x7 grid where board[0] is the top row and board[5] is the bottom row
Board = List[List[Cell]]
