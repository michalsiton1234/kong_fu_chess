"""
PromotionService handles pawn promotion on the last rank (Phase 8 / Iteration 10).

Architecture Rule 6: promotion is a dedicated sub-service, not embedded in
Board or piece-movement geometry rules.
"""
from ..model.board import Board
from ..model.piece import PAWN, QUEEN, WHITE, Piece


class PromotionService:
    def apply_if_needed(self, piece: Piece, board: Board) -> None:
        if piece.kind != PAWN:
            return
        if not self._reached_last_row(piece, board.height):
            return
        piece.kind = QUEEN

    @staticmethod
    def _reached_last_row(piece: Piece, board_height: int) -> bool:
        if piece.color == WHITE:
            return piece.cell.row == 0
        return piece.cell.row == board_height - 1
