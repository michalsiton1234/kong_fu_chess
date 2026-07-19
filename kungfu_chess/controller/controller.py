"""
Controller handles click input and piece selection (Rule 4–5).

It maps pixels to board cells via BoardMapper and delegates move requests
to GameEngine without performing rule validation itself.
"""
from typing import Optional

from ..engine.game_engine import GameEngine
from ..io.board_mapper import BoardMapper
from ..model.board import Board
from ..model.piece import Piece
from ..model.position import Position


class Controller:
    def __init__(
        self,
        game_engine: GameEngine,
        board_mapper: Optional[BoardMapper] = None,
    ):
        self._game_engine = game_engine
        self._board_mapper = board_mapper or BoardMapper()
        self._selected_piece: Optional[Piece] = None
        self._last_failed_destination: Optional[Position] = None

    def reset(self) -> None:
        self._selected_piece = None
        self._last_failed_destination = None

    @property
    def selected_piece(self) -> Optional[Piece]:
        return self._selected_piece

    @property
    def last_failed_destination(self) -> Optional[Position]:
        return self._last_failed_destination

    def clear_failed_destination(self) -> None:
        self._last_failed_destination = None

    def handle_click(self, board: Board, x: int, y: int) -> None:
        if self._game_engine.game_over:
            return

        position = self._board_mapper.to_position(board, x, y)
        if position is None:
            return

        self._game_engine.apply_pending_moves(board)
        if self._game_engine.game_over:
            return

        clicked_piece = board.piece_at(position)
        if self._selected_piece is None:
            self._select_piece(board, position, clicked_piece)
            return

        if (
            clicked_piece is not None
            and clicked_piece.color == self._selected_piece.color
        ):
            self._change_selection(board, position, clicked_piece)
            return

        self._attempt_move(board, position, clicked_piece)

    def handle_jump(self, board: Board, x: int, y: int) -> None:
        if self._game_engine.game_over:
            return

        position = self._board_mapper.to_position(board, x, y)
        if position is None:
            return

        self._game_engine.apply_pending_moves(board)
        if self._game_engine.game_over:
            return

        piece = board.piece_at(position)
        if piece is None:
            return

        self._game_engine.request_jump(board, piece, position)
        self._selected_piece = None

    def _select_piece(
        self,
        board: Board,
        position: Position,
        clicked_piece: Optional[Piece],
    ) -> None:
        if clicked_piece is None:
            return
        if self._game_engine.arbiter.is_piece_moving(position):
            return
        if self._game_engine.arbiter.is_piece_airborne(clicked_piece):
            return
        if self._game_engine.arbiter.is_piece_resting(clicked_piece):
            return
        self._selected_piece = clicked_piece

    def _change_selection(
        self,
        board: Board,
        position: Position,
        clicked_piece: Piece,
    ) -> None:
        if self._game_engine.arbiter.is_piece_moving(position):
            return
        if self._game_engine.arbiter.is_piece_airborne(clicked_piece):
            return
        if self._game_engine.arbiter.is_piece_resting(clicked_piece):
            return
        self._selected_piece = clicked_piece

    def _attempt_move(
        self,
        board: Board,
        destination: Position,
        clicked_piece: Optional[Piece],
    ) -> None:
        source = self._selected_piece.cell
        if self._game_engine.arbiter.is_piece_moving(source):
            self._selected_piece = None
            return
        if self._game_engine.arbiter.is_piece_airborne(self._selected_piece):
            self._selected_piece = None
            return
        if self._game_engine.arbiter.is_piece_resting(self._selected_piece):
            self._selected_piece = None
            return

        allow_premove = (
            not self._game_engine.validate_move(
                board, self._selected_piece, source, destination
            )
            and clicked_piece is not None
            and clicked_piece.color == self._selected_piece.color
        )

        self._last_failed_destination = None
        accepted = self._game_engine.request_move(
            board,
            self._selected_piece,
            source,
            destination,
            allow_premove=allow_premove,
        )
        if not accepted:
            self._last_failed_destination = destination
        self._selected_piece = None
