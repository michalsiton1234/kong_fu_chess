import sys
from pathlib import Path

import cv2
import numpy as np

_view_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_view_root))
from paths import CTD26_DIR

sys.path.insert(0, str(CTD26_DIR / "py"))
from img import Img

from .board_layout import (
    BOARD_OFFSET_X,
    CELL_HEIGHT,
    CELL_WIDTH,
    PANEL_WIDTH,
    cell_bounds,
)
from .game_snapshot import GameSnapshot
from .piece_assets import piece_code
from .sprite_manager import SpriteManager
from . import hud_layout


class Renderer:
    PANEL_COLOR = (45, 45, 45)

    def __init__(self, board_path: Path):
        self._board_path = board_path
        self._sprites = SpriteManager()

    def render(self, snapshot: GameSnapshot) -> Img:
        board_img = Img().read(str(self._board_path))
        canvas = self._create_canvas(board_img)
        board_img.draw_on(canvas, BOARD_OFFSET_X, 0)

        self._draw_legal_moves(canvas, snapshot.legal_targets)
        self._draw_rest_overlays(canvas, snapshot.pieces)

        self._draw_cell_highlight(
            canvas,
            snapshot.hover_row,
            snapshot.hover_col,
            hud_layout.HOVER_BORDER_COLOR,
            2,
        )
        self._draw_cell_highlight(
            canvas,
            snapshot.selected_row,
            snapshot.selected_col,
            hud_layout.SELECTED_BORDER_COLOR,
            4,
        )
        self._draw_cell_highlight(
            canvas, snapshot.reject_row, snapshot.reject_col, (0, 0, 255), 3
        )

        for piece in snapshot.pieces:
            code = piece_code(piece.color, piece.kind)
            path = self._sprites.sprite_path(
                code, piece.visual_state, piece.animation_time_ms
            )
            sprite = Img().read(
                str(path),
                size=(CELL_WIDTH, CELL_HEIGHT),
                keep_aspect=True,
            )
            sprite.draw_on(canvas, BOARD_OFFSET_X + piece.pixel_x, piece.pixel_y)

        self._draw_side_panels(canvas, snapshot)
        self._draw_top_hud(canvas, snapshot)

        return canvas

    def _create_canvas(self, board_img: Img) -> Img:
        canvas = Img()
        board_h, board_w = board_img.img.shape[:2]
        channels = board_img.img.shape[2]
        total_w = PANEL_WIDTH + board_w + PANEL_WIDTH
        fill_color = (45, 45, 45, 255) if channels == 4 else (45, 45, 45)
        canvas.img = np.full(
            (board_h, total_w, channels),
            fill_color,
            dtype=np.uint8,
        )
        return canvas

    def _draw_rest_overlays(self, canvas: Img, pieces) -> None:
        for piece in pieces:
            if piece.visual_state != "long_rest":
                continue
            progress = min(1.0, piece.animation_time_ms / hud_layout.LONG_REST_MS)
            if progress >= 1.0:
                continue
            self._draw_rest_drain(canvas, piece.row, piece.col, progress)

    def _draw_legal_moves(self, canvas: Img, targets) -> None:
        for row, col in targets:
            self._fill_cell(
                canvas,
                row,
                col,
                hud_layout.LEGAL_FILL_COLOR,
                hud_layout.LEGAL_FILL_ALPHA,
            )

    @staticmethod
    def _draw_rest_drain(canvas, row, col, progress) -> None:
        if canvas.img is None:
            return
        x0, y0, x1, y1 = cell_bounds(row, col)
        x = BOARD_OFFSET_X + x0
        y = y0
        w = x1 - x0
        h = y1 - y0
        drain_top = int(progress * h)
        if drain_top >= h:
            return

        region = canvas.img[y + drain_top : y + h, x : x + w]
        overlay = region.copy()
        region_h = h - drain_top
        cv2.rectangle(
            overlay, (0, 0), (w - 1, region_h - 1), hud_layout.REST_FILL_COLOR, -1
        )
        cv2.addWeighted(
            overlay,
            hud_layout.REST_FILL_ALPHA,
            region,
            1.0 - hud_layout.REST_FILL_ALPHA,
            0,
            region,
        )

    @staticmethod
    def _fill_cell(canvas, row, col, color, alpha) -> None:
        if row is None or col is None or canvas.img is None:
            return
        x0, y0, x1, y1 = cell_bounds(row, col)
        x = BOARD_OFFSET_X + x0
        y = y0
        w = x1 - x0
        h = y1 - y0
        region = canvas.img[y : y + h, x : x + w]
        overlay = region.copy()
        cv2.rectangle(overlay, (0, 0), (w - 1, h - 1), color, -1)
        cv2.addWeighted(overlay, alpha, region, 1.0 - alpha, 0, region)

    @staticmethod
    def _draw_cell_highlight(canvas, row, col, color, thickness) -> None:
        if row is None or col is None or canvas.img is None:
            return
        x0, y0, x1, y1 = cell_bounds(row, col)
        x = BOARD_OFFSET_X + x0
        y = y0
        w = x1 - x0
        h = y1 - y0
        cv2.rectangle(
            canvas.img,
            (x + 2, y + 2),
            (x + w - 3, y + h - 3),
            color,
            thickness,
        )

    @staticmethod
    def _trim_line(text: str) -> str:
        if len(text) <= hud_layout.MAX_MOVE_CHARS:
            return text
        return text[: hud_layout.MAX_MOVE_CHARS - 3] + "..."

    def _draw_player_panel(
        self,
        canvas: Img,
        x: int,
        title: str,
        score: int,
        moves,
    ) -> None:
        canvas.put_text(
            title,
            x,
            hud_layout.PANEL_TITLE_Y,
            hud_layout.PANEL_TITLE_SIZE,
            color=hud_layout.PANEL_TEXT,
            thickness=hud_layout.TEXT_THICKNESS,
        )
        canvas.put_text(
            f"Score: {score}",
            x,
            hud_layout.PANEL_SCORE_VALUE_Y,
            hud_layout.SCORE_VALUE_SIZE,
            color=hud_layout.SCORE_COLOR,
            thickness=hud_layout.TEXT_THICKNESS,
        )
        canvas.put_text(
            "Moves",
            x,
            hud_layout.PANEL_MOVES_HEADER_Y,
            hud_layout.MOVE_FONT_SIZE * 0.75,
            color=hud_layout.PANEL_MUTED,
            thickness=1,
        )

        visible = moves[-hud_layout.MAX_VISIBLE_MOVES :]
        for index, line in enumerate(visible):
            canvas.put_text(
                self._trim_line(line),
                x,
                hud_layout.PANEL_MOVES_START_Y
                + index * hud_layout.MOVE_LINE_HEIGHT,
                hud_layout.MOVE_FONT_SIZE,
                color=hud_layout.PANEL_TEXT,
                thickness=hud_layout.MOVE_TEXT_THICKNESS,
            )

    def _draw_side_panels(self, canvas: Img, snapshot: GameSnapshot) -> None:
        self._draw_player_panel(
            canvas,
            hud_layout.LEFT_PANEL_X,
            snapshot.white_player_name,
            snapshot.score_white,
            snapshot.white_moves,
        )
        self._draw_player_panel(
            canvas,
            hud_layout.RIGHT_PANEL_X,
            snapshot.black_player_name,
            snapshot.score_black,
            snapshot.black_moves,
        )

    def _draw_top_hud(self, canvas: Img, snapshot: GameSnapshot) -> None:
        if snapshot.selected_label:
            canvas.put_text(
                snapshot.selected_label,
                hud_layout.SELECTED_X,
                hud_layout.SELECTED_Y,
                hud_layout.SELECTED_SIZE,
                color=(255, 255, 0, 255),
                thickness=2,
            )

        if snapshot.game_over:
            canvas.put_text(
                "GAME OVER",
                hud_layout.GAME_OVER_X,
                hud_layout.GAME_OVER_Y,
                1.2,
                color=(0, 0, 255, 255),
                thickness=2,
            )
