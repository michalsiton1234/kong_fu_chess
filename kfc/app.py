"""
KongFuChessApp: wires the parsing / validation / command pipeline together.

Input and output streams are passed into `run()` (dependency injection)
instead of this class reaching for `sys.stdin` / `print()` directly. That
means unit tests can exercise the full pipeline with plain `io.StringIO`
objects, with no need to monkey-patch `sys.stdin` or capture stdout.
"""
from typing import Optional, TextIO

from .board import Board
from .board_validator import BoardValidator
from .exceptions import BoardError
from .input_parser import InputParser
from .piece_registry import PieceRegistry


class KongFuChessApp:
    def __init__(
        self,
        parser: Optional[InputParser] = None,
        validator: Optional[BoardValidator] = None,
    ):
        self._parser = parser or InputParser()
        self._validator = validator or BoardValidator(PieceRegistry())

    def run(self, input_stream: TextIO, output_stream: TextIO) -> None:
        raw_text = input_stream.read().strip()
        if not raw_text:
            return

        board_rows, commands = self._parser.parse(raw_text)
        if not board_rows:
            return

        try:
            self._validator.validate(board_rows)
        except BoardError as error:
            print(error.error_code, file=output_stream)
            return

        if "print_board" in commands:
            board = Board(board_rows)
            print(board.to_text(), file=output_stream)
