"""Scheduled in-flight move (Rule 9 — virtual time, Rule 10 — atomic arrival)."""
from dataclasses import dataclass

from ..model.piece import Piece
from ..model.position import Position


@dataclass
class Motion:
    arrival_time: int
    source: Position
    destination: Position
    piece: Piece
