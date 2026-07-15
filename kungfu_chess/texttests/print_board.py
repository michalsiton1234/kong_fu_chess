"""PrintBoard renders the current logical board state (Rule 2)."""
from typing import TextIO

from ..engine.game_engine import GameEngine
from ..io.board_printer import BoardPrinter
from ..model.board import Board


class PrintBoard:
    def __init__(
        self,
        game_engine: GameEngine,
        board_printer: BoardPrinter,
        output_stream: TextIO,
    ):
        self._game_engine = game_engine
        self._board_printer = board_printer
        self._output_stream = output_stream

    def execute(self, board: Board) -> None:
        self._game_engine.apply_pending_moves(board)
        print(
            self._board_printer.render(board),
            file=self._output_stream,
        )
