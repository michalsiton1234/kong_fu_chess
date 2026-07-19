"""Maps GUI image pixels to logical board cells (accounts for side panels)."""
from typing import Optional

from kungfu_chess.model.board import Board
from kungfu_chess.model.position import Position

from .board_layout import BOARD_HEIGHT, BOARD_OFFSET_X, BOARD_WIDTH, pixel_to_cell


class GraphicsBoardMapper:
    def to_position(self, board: Board, x: int, y: int) -> Optional[Position]:
        board_x = x - BOARD_OFFSET_X
        cell = pixel_to_cell(board_x, y)
        if cell is None:
            return None

        row, col = cell
        position = Position(row=row, col=col)
        if board.in_bounds(position):
            return position
        return None
