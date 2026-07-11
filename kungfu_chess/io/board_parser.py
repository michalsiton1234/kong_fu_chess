"""
BoardParser creates a Board from text, following the Board Notation rules
(see notation.py). It assigns each parsed piece a stable id at creation
time (architecture doc, "Piece IDs are assigned at creation time by
BoardParser or PieceFactory").

BoardParser only knows about board notation — it does not know about the
wider script structure ("Board:" / "Commands:" sections, that's
ScriptParser's job) and it never touches stdin/stdout directly.
"""
from itertools import count
from typing import List

from ..model.board import Board
from ..model.piece import Piece
from ..model.position import Position
from .exceptions import RowWidthMismatchError
from .notation import parse_token


class BoardParser:
    def __init__(self):
        self._next_id = count(1)

    def parse(self, board_text: str) -> Board:
        rows = self._split_rows(board_text)
        if not rows:
            return Board(width=0, height=0)

        self._validate_row_widths(rows)
        board = Board(width=len(rows[0]), height=len(rows))

        for row_index, row in enumerate(rows):
            for col_index, token in enumerate(row):
                parsed = parse_token(token)  # raises UnknownTokenError
                if parsed is None:
                    continue
                color, kind = parsed
                board.add_piece(
                    Piece(
                        id=f"p{next(self._next_id)}",
                        color=color,
                        kind=kind,
                        cell=Position(row_index, col_index),
                    )
                )
        return board

    @staticmethod
    def _split_rows(board_text: str) -> List[List[str]]:
        lines = [line.strip() for line in board_text.strip().split("\n") if line.strip()]
        return [line.split() for line in lines]

    @staticmethod
    def _validate_row_widths(rows: List[List[str]]) -> None:
        expected_width = len(rows[0])
        for row in rows:
            if len(row) != expected_width:
                raise RowWidthMismatchError()
