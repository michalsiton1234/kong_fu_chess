from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class PieceView:
    piece_id: str
    color: str
    kind: str
    row: int
    col: int
    pixel_x: int
    pixel_y: int
    visual_state: str = "idle"
    animation_time_ms: int = 0


@dataclass
class GameSnapshot:
    board_width: int
    board_height: int
    pieces: List[PieceView]
    selected_row: Optional[int] = None
    selected_col: Optional[int] = None
    hover_row: Optional[int] = None
    hover_col: Optional[int] = None
    reject_row: Optional[int] = None
    reject_col: Optional[int] = None
    legal_targets: List[Tuple[int, int]] = field(default_factory=list)
    game_over: bool = False
    score_white: int = 0
    score_black: int = 0
    white_player_name: str = "White"
    black_player_name: str = "Black"
    white_moves: List[str] = field(default_factory=list)
    black_moves: List[str] = field(default_factory=list)
    selected_label: Optional[str] = None
