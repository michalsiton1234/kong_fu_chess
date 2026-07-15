"""
RuleEngine validates whether a piece may move to a target cell (Rule 7).

It delegates per-piece geometry to Strategy-pattern rules and applies
board-level constraints shared by all pieces.
"""
from typing import Dict, Optional

from ..model.board import Board
from ..model.piece import (
    BISHOP,
    KING,
    KNIGHT,
    PAWN,
    QUEEN,
    ROOK,
    Piece,
)
from ..model.position import Position
from .bishop_rule import BishopRule
from .king_rule import KingRule
from .knight_rule import KnightRule
from .pawn_rule import PawnRule
from .piece_rule import PieceRule
from .queen_rule import QueenRule
from .rook_rule import RookRule


class RuleEngine:
    def __init__(self, rules: Optional[Dict[str, PieceRule]] = None):
        self._rules = rules or self._default_rules()

    @staticmethod
    def _default_rules() -> Dict[str, PieceRule]:
        return {
            KING: KingRule(),
            QUEEN: QueenRule(),
            ROOK: RookRule(),
            BISHOP: BishopRule(),
            KNIGHT: KnightRule(),
            PAWN: PawnRule(),
        }

    def validate_move(
        self,
        board: Board,
        piece: Piece,
        source: Position,
        destination: Position,
    ) -> bool:
        if source == destination:
            return False

        dest_piece = board.piece_at(destination)
        if dest_piece is not None and dest_piece.color == piece.color:
            return False

        rule = self._rules.get(piece.kind)
        if rule is None:
            return False
        return rule.can_move(board, piece, source, destination)
