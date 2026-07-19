"""Scale the game window so it fits on screen (avoids taskbar/title-bar clipping)."""
import ctypes


def fit_display_scale(image_width: int, image_height: int) -> float:
    user32 = ctypes.windll.user32
    screen_w = user32.GetSystemMetrics(0)
    screen_h = user32.GetSystemMetrics(1)

    margin_w = 40
    margin_h = 120
    max_w = max(1, screen_w - margin_w)
    max_h = max(1, screen_h - margin_h)

    scale_w = max_w / image_width
    scale_h = max_h / image_height
    return min(1.0, scale_w, scale_h)
