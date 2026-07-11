"""
Piece represents a chess piece.

Piece.state is only a lifecycle flag: "idle", "moving", or "captured". It
does NOT store path, destination, elapsed time, speed, interpolation, or
arrival logic — those details belong to Motion and RealTimeArbiter, which
will be introduced in later iterations (see architecture Rule 9 — virtual
time, and Rule 10 — atomic state transitions).

A Piece never knows about the renderer, mouse clicks, pixels, or text-test
syntax (Separation of Concerns, Rule 3).

Piece IDs are assigned consistently at creation time by BoardParser (or a
future dedicated PieceFactory). If stable identity is later relied upon
for motion tracking or snapshots, duplicate piece IDs would be invalid —
Board itself does not currently enforce ID uniqueness, since in this
iteration position-based occupancy is the only invariant that matters.
"""
from dataclasses import dataclass

from .position import Position

IDLE = "idle"
MOVING = "moving"
CAPTURED = "captured"

WHITE = "white"
BLACK = "black"

KING = "king"
QUEEN = "queen"
ROOK = "rook"
BISHOP = "bishop"
KNIGHT = "knight"
PAWN = "pawn"


@dataclass
class Piece:
    id: str
    color: str
    kind: str
    cell: Position
    state: str = IDLE
