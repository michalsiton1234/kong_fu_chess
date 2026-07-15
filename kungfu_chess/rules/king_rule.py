from ..model.board import Board
from ..model.piece import Piece
from ..model.position import Position
from .piece_rule import PieceRule


class KingRule(PieceRule):
    def can_move(
        self,
        board: Board,
        piece: Piece,
        source: Position,
        destination: Position,
    ) -> bool:
        delta_row = abs(destination.row - source.row)
        delta_col = abs(destination.col - source.col)
        return delta_row <= 1 and delta_col <= 1
