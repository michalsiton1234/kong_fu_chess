"""
BoardMapper converts pixel coordinates into logical board positions (Rule 4 — Coordinate Adapter).
Each board cell is defined as 100x100 pixels.

It respects Separation of Concerns (Rule 3) by querying the board's bounds,
ensuring that rendering-level coordinates (pixels) map cleanly into model positions.
"""
from typing import Optional
from ..model.board import Board
from ..model.position import Position

CELL_SIZE = 100

class BoardMapper:
    def to_position(self, board: Board, x: int, y: int) -> Optional[Position]:
        """
        Converts pixel coordinates (x, y) to a logical Position.
        Returns None if the coordinates are negative or outside the board bounds.
        """
        if x < 0 or y < 0:
            return None
            
        # x matches columns (horizontal), y matches rows (vertical)
        col = x // CELL_SIZE
        row = y // CELL_SIZE
        
        pos = Position(row=row, col=col)
        if board.in_bounds(pos):
            return pos
        return None