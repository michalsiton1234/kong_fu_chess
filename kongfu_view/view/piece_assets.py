from pathlib import Path

from paths import BOARD_PNG, idle_sprite_path

_KIND = {"king": "K", "queen": "Q", "rook": "R", "bishop": "B", "knight": "N", "pawn": "P"}


def piece_code(color: str, kind: str) -> str:
    return f"{_KIND[kind]}{'W' if color == 'white' else 'B'}"


def idle_frame_path(code: str) -> Path:
    return idle_sprite_path(code)
