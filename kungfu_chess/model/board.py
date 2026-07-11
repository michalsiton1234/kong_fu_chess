"""
Board owns the logical arrangement of pieces.

Responsibilities (architecture doc, "Model Design — Board"):
  - Store width and height.
  - Add a piece.
  - Remove a piece.
  - Query a piece at a cell.
  - Check whether a cell is inside bounds.
  - Move a piece after a move has been validated.
  - Reject duplicate occupancy.

Board does NOT contain chess movement rules. The board knows what exists;
it does not decide which chess moves are legal (Separation of Concerns,
Rule 3; Strategy Pattern for piece rules, Rule 6). Board.move_piece assumes
validation has already happened — Board never calls a future RuleEngine,
and a future RuleEngine will never mutate Board directly (Rule 5, Rule 7).
"""
from typing import Dict, Optional

from .exceptions import DuplicateOccupancyError, PieceNotFoundError
from .piece import Piece
from .position import Position


class Board:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._pieces_by_cell: Dict[Position, Piece] = {}

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def in_bounds(self, position: Position) -> bool:
        return 0 <= position.row < self._height and 0 <= position.col < self._width

    def piece_at(self, position: Position) -> Optional[Piece]:
        return self._pieces_by_cell.get(position)

    def add_piece(self, piece: Piece) -> None:
        if piece.cell in self._pieces_by_cell:
            raise DuplicateOccupancyError(
                f"Cell {piece.cell} is already occupied"
            )
        self._pieces_by_cell[piece.cell] = piece

    def remove_piece(self, position: Position) -> None:
        if position not in self._pieces_by_cell:
            raise PieceNotFoundError(f"No piece at {position}")
        del self._pieces_by_cell[position]

    def move_piece(self, source: Position, destination: Position) -> None:
        """Moves a piece that has already been validated elsewhere.

        Any piece currently occupying `destination` is silently replaced —
        Board has no opinion on whether that represents a legal capture;
        that decision belongs entirely to the future RuleEngine, which is
        expected to have already approved this move before Board is asked
        to perform it.
        """
        piece = self._pieces_by_cell.pop(source, None)
        if piece is None:
            raise PieceNotFoundError(f"No piece at {source}")
        piece.cell = destination
        self._pieces_by_cell[destination] = piece
