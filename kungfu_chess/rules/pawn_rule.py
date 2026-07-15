from ..model.board import Board
from ..model.piece import WHITE, Piece
from ..model.position import Position
from .path_utils import is_path_clear
from .piece_rule import PieceRule


class PawnRule(PieceRule):
    def can_move(
        self,
        board: Board,
        piece: Piece,
        source: Position,
        destination: Position,
    ) -> bool:
        dest_piece = board.piece_at(destination)
        direction = -1 if piece.color == WHITE else 1
        row_diff = destination.row - source.row
        col_diff = abs(destination.col - source.col)

        if col_diff == 0:
            if row_diff == direction:
                return dest_piece is None
            if row_diff == 2 * direction and source.row == self._start_row(
                piece, board.height
            ):
                return (
                    dest_piece is None
                    and is_path_clear(board, source, destination)
                )
        elif col_diff == 1:
            if row_diff == direction:
                return (
                    dest_piece is not None and dest_piece.color != piece.color
                )
        return False

    @staticmethod
    def _start_row(piece: Piece, board_height: int) -> int:
        # Standard pawn ranks: white on height-2, black on row 1.
        if piece.color == WHITE:
            return board_height - 2
        return 1
