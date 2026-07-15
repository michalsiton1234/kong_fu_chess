from ..model.board import Board
from ..model.piece import Piece
from ..model.position import Position
from .path_utils import is_path_clear
from .piece_rule import PieceRule


class QueenRule(PieceRule):
    def can_move(
        self,
        board: Board,
        piece: Piece,
        source: Position,
        destination: Position,
    ) -> bool:
        delta_row = abs(destination.row - source.row)
        delta_col = abs(destination.col - source.col)
        straight = delta_row == 0 or delta_col == 0
        diagonal = delta_row == delta_col
        if not straight and not diagonal:
            return False
        return is_path_clear(board, source, destination)
