"""
RealTimeArbiter manages virtual time and parallel in-flight motions (Rule 9).

Pieces reach their destination only after travel duration elapses. State
changes are applied atomically at arrival — no in-between board positions
(Rule 10).
"""
from typing import Callable, Dict, List, Optional

from ..model.board import Board
from ..model.piece import KING, PAWN, QUEEN, Piece
from ..model.position import Position
from ..rules.promotion_service import PromotionService
from .game_events import CounterCaptureEvent, GameObserver, MoveCompletedEvent
from .jump import Jump
from .motion import Motion
from .rest import LONG_REST_MS, SHORT_REST_MS


class RealTimeArbiter:
    def __init__(
        self,
        promotion_service: Optional[PromotionService] = None,
        observers: Optional[List[GameObserver]] = None,
    ) -> None:
        self._current_time: int = 0
        self._pending_motions: List[Motion] = []
        self._pending_jumps: List[Jump] = []
        self._rest_until_by_piece_id: Dict[str, int] = {}
        self._promotion_service = promotion_service or PromotionService()
        self._observers: List[GameObserver] = list(observers or [])

    def add_observer(self, observer: GameObserver) -> None:
        self._observers.append(observer)

    @property
    def current_time(self) -> int:
        return self._current_time

    def reset(self) -> None:
        self._current_time = 0
        self._pending_motions = []
        self._pending_jumps = []
        self._rest_until_by_piece_id = {}

    def advance_time(self, milliseconds: int) -> None:
        self._current_time += milliseconds

    def schedule(self, motion: Motion) -> None:
        self._pending_motions.append(motion)

    def schedule_jump(self, jump: Jump) -> None:
        self._pending_jumps.append(jump)

    def is_piece_moving(self, source: Position) -> bool:
        return any(
            motion.source == source for motion in self._pending_motions
        )

    def is_piece_in_motion(self, piece: Piece) -> bool:
        return any(motion.piece is piece for motion in self._pending_motions)

    def is_piece_airborne(self, piece: Piece) -> bool:
        return any(
            jump.piece is piece and self._current_time < jump.land_time
            for jump in self._pending_jumps
        )

    def is_piece_resting(self, piece: Piece) -> bool:
        rest_until = self._rest_until_by_piece_id.get(piece.id)
        if rest_until is None:
            return False
        return self._current_time < rest_until

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

            if self._try_airborne_counter_capture(
                board, motion, is_game_over, mark_game_over
            ):
                continue

            if board.piece_at(motion.source) != motion.piece:
                continue

            target_piece = board.piece_at(motion.destination)
            if (
                target_piece is not None
                and target_piece.color == motion.piece.color
            ):
                continue

            captured_piece = None
            if (
                target_piece is not None
                and target_piece.color != motion.piece.color
            ):
                captured_piece = target_piece

            if captured_piece is not None and captured_piece.kind == KING:
                mark_game_over()

            was_pawn = motion.piece.kind == PAWN
            board.move_piece(motion.source, motion.destination)
            self._promotion_service.apply_if_needed(motion.piece, board)
            promoted_to_queen = was_pawn and motion.piece.kind == QUEEN
            self._notify_move_completed(
                MoveCompletedEvent(
                    timestamp_ms=motion.arrival_time,
                    piece=motion.piece,
                    source=motion.source,
                    destination=motion.destination,
                    captured_piece=captured_piece,
                    promoted_to_queen=promoted_to_queen,
                )
            )
            self._start_long_rest(motion.piece)

        self._pending_motions = remaining
        self._apply_landed_jumps()

    def _active_jump_at(
        self, cell: Position, event_time: int
    ) -> Optional[Jump]:
        for jump in self._pending_jumps:
            if jump.cell != cell:
                continue
            if jump.start_time <= event_time <= jump.land_time:
                return jump
        return None

    def _try_airborne_counter_capture(
        self,
        board: Board,
        motion: Motion,
        is_game_over: Callable[[], bool],
        mark_game_over: Callable[[], None],
    ) -> bool:
        jump = self._active_jump_at(motion.destination, motion.arrival_time)
        if jump is None:
            return False
        if motion.piece.color == jump.piece.color:
            return False

        if board.piece_at(motion.source) != motion.piece:
            return False

        if motion.piece.kind == KING:
            mark_game_over()

        self._notify_counter_capture(
            CounterCaptureEvent(
                timestamp_ms=motion.arrival_time,
                defender=jump.piece,
                captured_piece=motion.piece,
                cell=motion.destination,
            )
        )
        board.remove_piece(motion.source)
        return True

    def _apply_landed_jumps(self) -> None:
        remaining: List[Jump] = []
        for jump in self._pending_jumps:
            if jump.land_time <= self._current_time:
                self._start_short_rest(jump.piece)
                continue
            remaining.append(jump)
        self._pending_jumps = remaining

    def _start_long_rest(self, piece: Piece) -> None:
        self._rest_until_by_piece_id[piece.id] = (
            self._current_time + LONG_REST_MS
        )

    def _start_short_rest(self, piece: Piece) -> None:
        self._rest_until_by_piece_id[piece.id] = (
            self._current_time + SHORT_REST_MS
        )

    def _notify_move_completed(self, event: MoveCompletedEvent) -> None:
        for observer in self._observers:
            observer.on_move_completed(event)

    def _notify_counter_capture(self, event: CounterCaptureEvent) -> None:
        for observer in self._observers:
            observer.on_counter_capture(event)
