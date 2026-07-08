"""
Board: encapsulates the 2D grid of square tokens, and knows how to render
itself back to text.

Storage is deliberately hidden behind this class (Encapsulation). Today it
is a simple list-of-lists of strings. If/when the project switches to a
binary board representation for memory efficiency (a change explicitly
flagged as coming in the future), only the internals of this class need to
change - every other module reads the board exclusively through
`get_row()` / `rows()` / `width` / `height` / `to_text()`, never through the
raw storage, so swapping the storage strategy will not ripple through the
codebase.

Rendering (`to_text`) is kept on Board itself rather than in a separate
"printer" class: it is a one-line, purely-derived view of the same data
Board already owns, not a distinct responsibility worth its own module.
"""
from typing import List


class Board:
    def __init__(self, rows: List[List[str]]):
        self._rows: List[List[str]] = [list(row) for row in rows]

    @property
    def height(self) -> int:
        return len(self._rows)

    @property
    def width(self) -> int:
        return len(self._rows[0]) if self._rows else 0

    def get_row(self, index: int) -> List[str]:
        """Returns a defensive copy - callers can never mutate our internal state."""
        return list(self._rows[index])

    def rows(self):
        for index in range(self.height):
            yield self.get_row(index)

    def to_text(self) -> str:
        return "\n".join(" ".join(row) for row in self.rows())
