"""
GameEngine is the application-service gateway for all game actions (Rule 8).

It separates validation from action (Rule 5) by consulting RuleEngine and
delegating time-based execution to RealTimeArbiter.
"""
from typing import Optional

from ..model.board import Board
from ..model.piece import KNIGHT, Piece
from ..model.position import Position
from ..rules.rule_engine import RuleEngine
from .game_events import GameObserver
from .jump import JUMP_DURATION_MS, Jump
from .motion import Motion
from .real_time_arbiter import RealTimeArbiter


class GameEngine:
    def __init__(
        self,
        rule_engine: Optional[RuleEngine] = None,
        arbiter: Optional[RealTimeArbiter] = None,
    ):
        self._rule_engine = rule_engine or RuleEngine()
        self._arbiter = arbiter or RealTimeArbiter()
        self._game_over = False

    @property
    def arbiter(self) -> RealTimeArbiter:
        return self._arbiter

    @property
    def game_over(self) -> bool:
        return self._game_over

    def add_observer(self, observer: GameObserver) -> None:
        self._arbiter.add_observer(observer)

    def reset(self) -> None:
        self._game_over = False
        self._arbiter.reset()

    def apply_pending_moves(self, board: Board) -> None:
        self._arbiter.apply_completed_motions(
            board,
            is_game_over=lambda: self._game_over,
            mark_game_over=self._mark_game_over,
        )

    def advance_time(self, board: Board, milliseconds: int) -> None:
        self._arbiter.advance_time(milliseconds)
        self.apply_pending_moves(board)

    def validate_move(
        self,
        board: Board,
        piece: Piece,
        source: Position,
        destination: Position,
    ) -> bool:
        return self._rule_engine.validate_move(
            board, piece, source, destination
        )

    def request_move(
        self,
        board: Board,
        piece: Piece,
        source: Position,
        destination: Position,
        *,
        allow_premove: bool = False,
    ) -> bool:
        if self._game_over:
            return False

        if self._arbiter.is_piece_moving(source):
            return False

        if self._arbiter.is_piece_airborne(piece):
            return False

        if self._arbiter.is_piece_resting(piece):
            return False

        is_valid = self._rule_engine.validate_move(
            board, piece, source, destination
        )
        if not is_valid and not allow_premove:
            return False

        if self._arbiter.has_destination_conflict(destination):
            return False

        travel_time = self._travel_time(piece, source, destination)
        arrival_time = self._arbiter.current_time + travel_time
        self._arbiter.schedule(
            Motion(
                arrival_time=arrival_time,
                source=source,
                destination=destination,
                piece=piece,
            )
        )
        return True

    def request_jump(
        self,
        board: Board,
        piece: Piece,
        cell: Position,
    ) -> bool:
        if self._game_over:
            return False

        if board.piece_at(cell) != piece:
            return False

        if self._arbiter.is_piece_moving(cell):
            return False

        if self._arbiter.is_piece_in_motion(piece):
            return False

        if self._arbiter.is_piece_airborne(piece):
            return False

        if self._arbiter.is_piece_resting(piece):
            return False

        start_time = self._arbiter.current_time
        self._arbiter.schedule_jump(
            Jump(
                start_time=start_time,
                land_time=start_time + JUMP_DURATION_MS,
                piece=piece,
                cell=cell,
            )
        )
        return True

    def _mark_game_over(self) -> None:
        self._game_over = True

    @staticmethod
    def _travel_time(piece: Piece, source: Position, destination: Position) -> int:
        delta_row = abs(destination.row - source.row)
        delta_col = abs(destination.col - source.col)
        distance = max(delta_row, delta_col)
        if piece.kind == KNIGHT:
            distance = 1
        return distance * 1000
