from ..model.board import Board
from ..model.piece import Piece
from ..model.position import Position
from .path_utils import is_path_clear
from .piece_rule import PieceRule


class BishopRule(PieceRule):
    def can_move(
        self,
        board: Board,
        piece: Piece,
        source: Position,
        destination: Position,
    ) -> bool:
        delta_row = abs(destination.row - source.row)
        delta_col = abs(destination.col - source.col)
        if delta_row != delta_col:
            return False
        return is_path_clear(board, source, destination)
