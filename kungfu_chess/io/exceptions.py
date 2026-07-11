"""
Exceptions raised while parsing board *text*. Kept separate from
model/exceptions.py: these represent invalid input text, not invalid
operations on an already-built Board — two different reasons to change.

Each exception carries its own protocol `error_code`, so the printed error
text is defined exactly once (DRY) rather than duplicated between "the
place that detects the problem" and "the place that prints it".
"""


class BoardTextError(Exception):
    error_code = "ERROR UNKNOWN"

    def __init__(self, detail: str = ""):
        self.detail = detail
        super().__init__(f"{self.error_code} {detail}".strip())


class UnknownTokenError(BoardTextError):
    error_code = "ERROR UNKNOWN_TOKEN"


class RowWidthMismatchError(BoardTextError):
    error_code = "ERROR ROW_WIDTH_MISMATCH"
