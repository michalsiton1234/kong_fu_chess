"""Shared path-clearance checks for sliding pieces (Rule 6 — Strategy support)."""
from ..model.board import Board
from ..model.position import Position


def is_path_clear(board: Board, source: Position, dest: Position) -> bool:
    """Returns True when every cell between source and dest is empty."""
    row_dir = 0
    if dest.row > source.row:
        row_dir = 1
    elif dest.row < source.row:
        row_dir = -1

    col_dir = 0
    if dest.col > source.col:
        col_dir = 1
    elif dest.col < source.col:
        col_dir = -1

    curr_row = source.row + row_dir
    curr_col = source.col + col_dir

    while (curr_row, curr_col) != (dest.row, dest.col):
        if board.piece_at(Position(row=curr_row, col=curr_col)) is not None:
            return False
        curr_row += row_dir
        curr_col += col_dir

    return True
