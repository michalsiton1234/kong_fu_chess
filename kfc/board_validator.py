"""
BoardValidator: checks a raw board (list of token rows) against a
PieceRegistry and raises a specific `BoardError` on the first problem found.

This class does not print anything and does not know about stdout - keeping
validation and I/O strictly separate is what lets it be unit tested by
simply asserting on raised exceptions, with no output capturing needed.
"""
from typing import List

from .exceptions import RowWidthMismatchError, UnknownTokenError
from .piece_registry import PieceRegistry


class BoardValidator:
    def __init__(self, piece_registry: PieceRegistry):
        self._piece_registry = piece_registry

    def validate(self, board_rows: List[List[str]]) -> None:
        if not board_rows:
            return
        self._validate_tokens(board_rows)
        self._validate_row_widths(board_rows)

    def _validate_tokens(self, board_rows: List[List[str]]) -> None:
        for row in board_rows:
            for token in row:
                if not self._piece_registry.is_valid_token(token):
                    raise UnknownTokenError(token)

    def _validate_row_widths(self, board_rows: List[List[str]]) -> None:
        expected_width = len(board_rows[0])
        for row in board_rows:
            if len(row) != expected_width:
                raise RowWidthMismatchError()
