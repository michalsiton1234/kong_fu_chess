"""
PieceRegistry: the single source of truth for "which text tokens are legal
squares, and what piece do they represent".

`Piece` lives here too (rather than in its own file) because it has no
independent behaviour of its own - it is a tiny, passive value object that
only exists to be produced and interpreted by the registry. Splitting it
into a separate file would add an extra module without adding a real,
separate responsibility.

Why this is the extensibility point for future requirements:
- Section 3.2 of the design doc asks for pluggable piece types (e.g. a
  "Drone") without hard-coding rules elsewhere in the system. Because every
  other class only ever asks the registry "is this legal?" / "what piece is
  this?", adding a new piece type later is a matter of calling
  `registry.register(...)` (or loading definitions from a user-supplied
  config file) - nothing else in the codebase needs to change.
- It is also the natural place to introduce a compact numeric id per
  color/type combination (see `token_id`) once the board moves to a binary
  representation (see `board.py` for the storage-side half of that story).
"""
from dataclasses import dataclass
from typing import Dict, Iterable, Optional

EMPTY_SQUARE_TOKEN = "."

DEFAULT_COLORS = ("w", "b")
DEFAULT_PIECE_TYPES = ("K", "Q", "R", "B", "N", "P")


@dataclass(frozen=True)
class Piece:
    color: str            # canonical color id, e.g. "w" / "b"
    piece_type: str        # canonical piece-type id, e.g. "K", "Q", "N", ...
    original_token: str    # exact text as it appeared in the input

    def display_token(self) -> str:
        """The text that should be used when re-printing this square."""
        return self.original_token


class PieceRegistry:
    def __init__(
        self,
        colors: Iterable[str] = DEFAULT_COLORS,
        piece_types: Iterable[str] = DEFAULT_PIECE_TYPES,
    ):
        self._pieces_by_token: Dict[str, Piece] = {}
        self._next_token_id = 1
        self._token_id_by_key: Dict[str, int] = {}

        for color in colors:
            for piece_type in piece_types:
                self.register(color, piece_type)

    def register(self, color: str, piece_type: str) -> None:
        """Register a color/piece-type combination.

        Both accepted spelling conventions ("wK" and "Wk") are registered so
        that the board input stays backwards compatible, while still being
        driven entirely by data instead of a hard-coded literal set.
        """
        key = f"{color}{piece_type}"
        if key not in self._token_id_by_key:
            self._token_id_by_key[key] = self._next_token_id
            self._next_token_id += 1

        canonical_token = f"{color}{piece_type}"
        alternate_token = f"{color.upper()}{piece_type.lower()}"
        for token in (canonical_token, alternate_token):
            self._pieces_by_token[token] = Piece(
                color=color, piece_type=piece_type, original_token=token
            )

    def is_valid_token(self, token: str) -> bool:
        return token == EMPTY_SQUARE_TOKEN or token in self._pieces_by_token

    def parse_token(self, token: str) -> Optional[Piece]:
        """Return the Piece for a square token, or None for an empty square
        / unrecognized token (callers should check `is_valid_token` first)."""
        if token == EMPTY_SQUARE_TOKEN:
            return None
        template = self._pieces_by_token.get(token)
        if template is None:
            return None
        # Preserve the exact text seen on input, for faithful re-printing.
        return Piece(
            color=template.color,
            piece_type=template.piece_type,
            original_token=token,
        )

    def token_id(self, color: str, piece_type: str) -> Optional[int]:
        """A small, stable numeric id for a color/type combination.

        Not used yet - reserved for a future binary board representation,
        where each square could be stored as a fixed-width integer instead
        of a Python string.
        """
        return self._token_id_by_key.get(f"{color}{piece_type}")

    def all_valid_tokens(self):
        return set(self._pieces_by_token.keys()) | {EMPTY_SQUARE_TOKEN}
