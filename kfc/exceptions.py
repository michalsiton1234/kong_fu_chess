"""
Domain-specific exceptions for board parsing/validation.

Each exception carries its own protocol `error_code`, so the text of every
error message is defined exactly once (DRY) instead of being duplicated
between "the place that detects the problem" and "the place that prints it".
"""


class BoardError(Exception):
    """Base class for all board-related errors that map to a protocol code."""

    error_code: str = "ERROR UNKNOWN"

    def __init__(self, detail: str = ""):
        self.detail = detail
        super().__init__(f"{self.error_code} {detail}".strip())


class UnknownTokenError(BoardError):
    """Raised when a square in the board section contains an unrecognized token."""

    error_code = "ERROR UNKNOWN_TOKEN"


class RowWidthMismatchError(BoardError):
    """Raised when board rows don't all share the same number of columns."""

    error_code = "ERROR ROW_WIDTH_MISMATCH"
