from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PACKAGE_ROOT / "assets"
BOARD_PNG = ASSETS_DIR / "board.png"
PIECES_DIR = ASSETS_DIR / "pieces"
PIECES2_DIR = PIECES_DIR


def idle_sprite_path(code: str) -> Path:
    return PIECES_DIR / code / "states" / "idle" / "sprites" / "1.png"
