"""Strategy interface for per-piece movement rules (architecture Rule 6)."""
from abc import ABC, abstractmethod

from ..model.board import Board
from ..model.piece import Piece
from ..model.position import Position


class PieceRule(ABC):
    @abstractmethod
    def can_move(
        self,
        board: Board,
        piece: Piece,
        source: Position,
        destination: Position,
    ) -> bool:
        """Returns True when the piece may move from source to destination."""
