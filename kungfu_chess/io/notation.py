"""
Shared board-notation tables (Board Notation rules from the architecture doc):
  - Each row is written on a separate line.
  - Cells are separated by spaces.
  - "." means an empty cell.
  - White pieces use prefix "w"; black pieces use prefix "b".
  - Piece letters use chess notation: K, Q, R, B, N, P.

This module is the single source of truth for the token <-> (color, kind)
mapping, used by BOTH BoardParser and BoardPrinter (DRY, Rule 1) — if the
notation ever changes, it changes here once, not in two places that could
drift apart.
"""
from typing import Optional, Tuple

from ..model.piece import BISHOP, BLACK, KING, KNIGHT, PAWN, QUEEN, ROOK, WHITE
from .exceptions import UnknownTokenError

EMPTY_TOKEN = "."

_COLOR_PREFIX = {WHITE: "w", BLACK: "b"}
_PREFIX_TO_COLOR = {prefix: color for color, prefix in _COLOR_PREFIX.items()}

_KIND_LETTER = {
    KING: "K",
    QUEEN: "Q",
    ROOK: "R",
    BISHOP: "B",
    KNIGHT: "N",
    PAWN: "P",
}
_LETTER_TO_KIND = {letter: kind for kind, letter in _KIND_LETTER.items()}


def token_for(color: str, kind: str) -> str:
    return f"{_COLOR_PREFIX[color]}{_KIND_LETTER[kind]}"


def parse_token(token: str) -> Optional[Tuple[str, str]]:
    """Returns (color, kind), or None for the empty-cell token.

    Raises UnknownTokenError for anything that isn't the empty token or a
    well-formed "<w|b><K|Q|R|B|N|P>" pair.
    """
    if token == EMPTY_TOKEN:
        return None
    if len(token) == 2 and token[0] in _PREFIX_TO_COLOR and token[1] in _LETTER_TO_KIND:
        return _PREFIX_TO_COLOR[token[0]], _LETTER_TO_KIND[token[1]]
    raise UnknownTokenError(token)
