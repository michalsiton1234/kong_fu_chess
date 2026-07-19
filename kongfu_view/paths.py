from pathlib import Path

KONGFU_VIEW_DIR = Path(__file__).resolve().parent
REPO_ROOT = KONGFU_VIEW_DIR.parent
LOGIC_DIR = REPO_ROOT
CTD26_DIR = REPO_ROOT.parent / "kung_fu_chess_gra" / "CTD26"

BOARD_PNG = CTD26_DIR / "board.png"
PIECES2_DIR = CTD26_DIR / "pieces2"


def idle_sprite_path(code: str) -> Path:
    return PIECES2_DIR / code / "states" / "idle" / "sprites" / "1.png"


def ensure_working_directory() -> None:
    import os

    os.chdir(KONGFU_VIEW_DIR)
