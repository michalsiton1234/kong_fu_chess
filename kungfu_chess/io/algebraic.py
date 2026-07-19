"""Algebraic square names for move-log display (e2, c6, ...)."""
from ..model.position import Position


def square_name(position: Position) -> str:
    file_letter = chr(ord("a") + position.col)
    rank_number = 8 - position.row
    return f"{file_letter}{rank_number}"
