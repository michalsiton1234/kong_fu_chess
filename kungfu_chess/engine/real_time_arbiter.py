"""
RealTimeArbiter manages virtual time and parallel in-flight motions (Rule 9).

Pieces reach their destination only after travel duration elapses. State
changes are applied atomically at arrival — no in-between board positions
(Rule 10).
"""
from typing import Callable, List, Optional

from ..model.board import Board
from ..model.piece import KING, Piece
from ..model.position import Position
from ..rules.promotion_service import PromotionService
from .motion import Motion


class RealTimeArbiter:
    def __init__(
        self, promotion_service: Optional[PromotionService] = None
    ) -> None:
        self._current_time: int = 0
        self._pending_motions: List[Motion] = []
        self._promotion_service = promotion_service or PromotionService()

    @property
    def current_time(self) -> int:
        return self._current_time

    def reset(self) -> None:
        self._current_time = 0
        self._pending_motions = []

    def advance_time(self, milliseconds: int) -> None:
        self._current_time += milliseconds

    def schedule(self, motion: Motion) -> None:
        self._pending_motions.append(motion)

    def is_piece_moving(self, source: Position) -> bool:
        return any(
            motion.source == source for motion in self._pending_motions
        )

    def has_destination_conflict(self, destination: Position) -> bool:
        return any(
            motion.destination == destination
            for motion in self._pending_motions
        )

    def apply_completed_motions(
        self,
        board: Board,
        is_game_over: Callable[[], bool],
        mark_game_over: Callable[[], None],
    ) -> None:
        self._pending_motions.sort(key=lambda motion: motion.arrival_time)

        remaining: List[Motion] = []
        for motion in self._pending_motions:
            if self._current_time < motion.arrival_time:
                remaining.append(motion)
                continue

            if is_game_over():
                continue

            if board.piece_at(motion.source) != motion.piece:
                continue

            target_piece = board.piece_at(motion.destination)
            if (
                target_piece is not None
                and target_piece.color == motion.piece.color
            ):
                continue

            if target_piece is not None and target_piece.kind == KING:
                mark_game_over()

            board.move_piece(motion.source, motion.destination)
            self._promotion_service.apply_if_needed(motion.piece, board)

        self._pending_motions = remaining
