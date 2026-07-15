"""In-place jump action (Iteration 11 — special action, 1000 ms airborne window)."""
from dataclasses import dataclass

from ..model.piece import Piece
from ..model.position import Position

JUMP_DURATION_MS = 1000


@dataclass
class Jump:
    start_time: int
    land_time: int
    piece: Piece
    cell: Position
