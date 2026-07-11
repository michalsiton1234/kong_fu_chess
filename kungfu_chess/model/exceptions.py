"""Exceptions raised by the model layer (Board). Kept separate from io/exceptions.py
because these represent invalid *operations* on an already-built Board, not
invalid *text* being parsed into one — two different reasons to change."""


class BoardError(Exception):
    """Base class for all Board-level errors."""


class DuplicateOccupancyError(BoardError):
    """Raised when adding a piece to a cell that is already occupied."""


class PieceNotFoundError(BoardError):
    """Raised when an operation references a piece/cell that does not exist."""


class OutOfBoundsError(BoardError):
    """Raised when a position falls outside the board's width/height."""
