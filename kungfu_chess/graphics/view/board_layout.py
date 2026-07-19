from typing import Optional, Tuple

BOARD_WIDTH = 822
BOARD_HEIGHT = 828
BOARD_COLS = 8
BOARD_ROWS = 8

CELL_WIDTH = BOARD_WIDTH // BOARD_COLS
CELL_HEIGHT = BOARD_HEIGHT // BOARD_ROWS

PANEL_WIDTH = 280
BOARD_OFFSET_X = PANEL_WIDTH
TOTAL_CANVAS_WIDTH = PANEL_WIDTH + BOARD_WIDTH + PANEL_WIDTH
TOTAL_CANVAS_HEIGHT = BOARD_HEIGHT


def to_pixel(row: int, col: int) -> Tuple[int, int]:
    x0, y0, _, _ = cell_bounds(row, col)
    return x0, y0


def to_board_pixel(row: int, col: int) -> Tuple[int, int]:
    x, y = to_pixel(row, col)
    return x + BOARD_OFFSET_X, y


def cell_bounds(row: int, col: int) -> Tuple[int, int, int, int]:
    x0 = (col * BOARD_WIDTH) // BOARD_COLS
    y0 = (row * BOARD_HEIGHT) // BOARD_ROWS
    x1 = ((col + 1) * BOARD_WIDTH) // BOARD_COLS
    y1 = ((row + 1) * BOARD_HEIGHT) // BOARD_ROWS
    return x0, y0, x1, y1


def pixel_to_cell(board_x: int, board_y: int) -> Optional[Tuple[int, int]]:
    if board_x < 0 or board_y < 0:
        return None
    if board_x >= BOARD_WIDTH or board_y >= BOARD_HEIGHT:
        return None

    col = min(BOARD_COLS - 1, (board_x * BOARD_COLS) // BOARD_WIDTH)
    row = min(BOARD_ROWS - 1, (board_y * BOARD_ROWS) // BOARD_HEIGHT)
    return row, col


def interpolate_pixel(
    source_row: int,
    source_col: int,
    dest_row: int,
    dest_col: int,
    progress: float,
) -> Tuple[int, int]:
    source_x, source_y = to_pixel(source_row, source_col)
    dest_x, dest_y = to_pixel(dest_row, dest_col)
    clamped = max(0.0, min(1.0, progress))
    x = int(source_x + (dest_x - source_x) * clamped)
    y = int(source_y + (dest_y - source_y) * clamped)
    return x, y
