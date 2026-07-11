"""
Position represents a board cell, not pixels.

It is a plain value object: two integers, equality, and a readable
representation. It deliberately knows nothing about board size, rendering,
movement rules, or pixel/input coordinates — those belong to Board,
BoardMapper, and the rule/rendering layers respectively (see architecture
Rule 3 — Separation of Concerns, and Rule 4 — Coordinate Adapter for
BoardMapper).

Bounds checking does NOT belong here — it belongs to Board, since only
Board knows its own width/height.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def __str__(self) -> str:
        return f"({self.row}, {self.col})"
