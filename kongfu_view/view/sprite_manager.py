import json
from pathlib import Path
from typing import Dict, Tuple

from paths import PIECES2_DIR

VISUAL_STATES = ("idle", "move", "jump", "long_rest", "short_rest")


class SpriteManager:
    def __init__(self) -> None:
        self._frame_counts: Dict[Tuple[str, str], int] = {}
        self._configs: Dict[Tuple[str, str], dict] = {}

    def sprite_path(
        self, code: str, visual_state: str, animation_time_ms: int
    ) -> Path:
        state = visual_state if visual_state in VISUAL_STATES else "idle"
        config = self._load_config(code, state)
        frame_count = self._frame_count(code, state)
        if frame_count <= 0:
            return self._fallback_path(code)

        fps = max(1, config.get("graphics", {}).get("frames_per_sec", 6))
        ms_per_frame = max(1, 1000 // fps)
        frame_index = animation_time_ms // ms_per_frame

        if not config.get("graphics", {}).get("is_loop", True):
            frame_index = min(frame_index, frame_count - 1)

        frame_number = (frame_index % frame_count) + 1
        return (
            PIECES2_DIR
            / code
            / "states"
            / state
            / "sprites"
            / f"{frame_number}.png"
        )

    def _fallback_path(self, code: str) -> Path:
        return PIECES2_DIR / code / "states" / "idle" / "sprites" / "1.png"

    def _load_config(self, code: str, state: str) -> dict:
        key = (code, state)
        if key not in self._configs:
            config_path = PIECES2_DIR / code / "states" / state / "config.json"
            if config_path.is_file():
                self._configs[key] = json.loads(config_path.read_text(encoding="utf-8"))
            else:
                self._configs[key] = {"graphics": {"frames_per_sec": 6, "is_loop": True}}
        return self._configs[key]

    def _frame_count(self, code: str, state: str) -> int:
        key = (code, state)
        if key not in self._frame_counts:
            sprites_dir = PIECES2_DIR / code / "states" / state / "sprites"
            if not sprites_dir.is_dir():
                self._frame_counts[key] = 0
            else:
                self._frame_counts[key] = len(list(sprites_dir.glob("*.png")))
        return self._frame_counts[key]
