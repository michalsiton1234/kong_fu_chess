import sys
from typing import Callable, Optional, Tuple

import cv2

from kungfu_chess.graphics.view.board_layout import (
    BOARD_HEIGHT,
    BOARD_OFFSET_X,
    BOARD_WIDTH,
    pixel_to_cell,
    TOTAL_CANVAS_HEIGHT,
    TOTAL_CANVAS_WIDTH,
)

MouseEventCallback = Callable[
    [int, int, int, Optional[Tuple[int, int]]], None
]

if sys.platform == "win32":
    import ctypes

    class _POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

    _user32 = ctypes.windll.user32
else:
    _user32 = None


class MouseAdapter:
    def __init__(
        self,
        window_name: str,
        on_mouse_event: Optional[MouseEventCallback] = None,
    ):
        self._window_name = window_name
        self._on_mouse_event = on_mouse_event
        self._image_width = TOTAL_CANVAS_WIDTH
        self._image_height = TOTAL_CANVAS_HEIGHT
        self._hover_image_x = 0
        self._hover_image_y = 0
        self._hover_cell: Optional[Tuple[int, int]] = None
        self._pending_left_click = False
        self._pending_right_click = False
        self._click_image_x = 0
        self._click_image_y = 0
        cv2.setMouseCallback(window_name, self._on_mouse)

    def set_image_size(self, width: int, height: int) -> None:
        self._image_width = width
        self._image_height = height

    def _client_position(self, callback_x: int, callback_y: int) -> Tuple[int, int]:
        if _user32 is None:
            return callback_x, callback_y

        hwnd = _user32.FindWindowW(None, self._window_name)
        if not hwnd:
            return callback_x, callback_y

        screen_pt = _POINT()
        if not _user32.GetCursorPos(ctypes.byref(screen_pt)):
            return callback_x, callback_y

        client_pt = _POINT(screen_pt.x, screen_pt.y)
        if not _user32.ScreenToClient(hwnd, ctypes.byref(client_pt)):
            return callback_x, callback_y

        return client_pt.x, client_pt.y

    def _on_mouse(self, event, x, y, flags, param) -> None:
        client_x, client_y = self._client_position(x, y)
        image_x, image_y = self._window_to_image(client_x, client_y)
        self._hover_image_x = image_x
        self._hover_image_y = image_y
        self._hover_cell = self._cell_at_image(image_x, image_y)

        if event == cv2.EVENT_LBUTTONDOWN:
            self._pending_left_click = True
            self._click_image_x = image_x
            self._click_image_y = image_y
        elif event == cv2.EVENT_RBUTTONDOWN:
            self._pending_right_click = True
            self._click_image_x = image_x
            self._click_image_y = image_y

        if self._on_mouse_event is not None:
            self._on_mouse_event(event, image_x, image_y, self._hover_cell)

    def _window_to_image(self, client_x: int, client_y: int) -> Tuple[int, int]:
        if self._image_width <= 0 or self._image_height <= 0:
            return client_x, client_y

        try:
            offset_x, offset_y, window_w, window_h = cv2.getWindowImageRect(
                self._window_name
            )
        except cv2.error:
            offset_x, offset_y = 0, 0
            window_w, window_h = self._image_width, self._image_height

        if window_w <= 0 or window_h <= 0:
            offset_x, offset_y = 0, 0
            window_w, window_h = self._image_width, self._image_height

        local_x = client_x - offset_x
        local_y = client_y - offset_y
        image_x = int(local_x * self._image_width / window_w)
        image_y = int(local_y * self._image_height / window_h)
        image_x = max(0, min(self._image_width - 1, image_x))
        image_y = max(0, min(self._image_height - 1, image_y))
        return image_x, image_y

    def _cell_at_image(self, image_x: int, image_y: int) -> Optional[Tuple[int, int]]:
        board_x = image_x - BOARD_OFFSET_X
        board_y = image_y
        if board_x < 0 or board_y < 0:
            return None
        if board_x >= BOARD_WIDTH or board_y >= BOARD_HEIGHT:
            return None
        return pixel_to_cell(board_x, board_y)

    @property
    def hover_image_position(self) -> Tuple[int, int]:
        return self._hover_image_x, self._hover_image_y

    def hover_cell(self) -> Optional[Tuple[int, int]]:
        return self._hover_cell

    def consume_click(self) -> Optional[Tuple[int, int]]:
        if not self._pending_left_click:
            return None
        self._pending_left_click = False
        return self._click_image_x, self._click_image_y

    def consume_right_click(self) -> Optional[Tuple[int, int]]:
        if not self._pending_right_click:
            return None
        self._pending_right_click = False
        return self._click_image_x, self._click_image_y
