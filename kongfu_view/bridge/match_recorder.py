"""Observer that records score and per-player move lists for the HUD."""
from typing import List

from kungfu_chess.engine.game_events import (
    CounterCaptureEvent,
    GameObserver,
    MoveCompletedEvent,
)
from kungfu_chess.io.algebraic import square_name
from kungfu_chess.model.piece import BLACK, WHITE

PIECE_VALUES = {
    "pawn": 1,
    "knight": 3,
    "bishop": 3,
    "rook": 5,
    "queen": 9,
    "king": 0,
}

KIND_LABELS = {
    "pawn": "Pawn",
    "knight": "Knight",
    "bishop": "Bishop",
    "rook": "Rook",
    "queen": "Queen",
    "king": "King",
}

PROMOTION_POINTS = 9


class MatchRecorder:
    def __init__(self) -> None:
        self.score_white = 0
        self.score_black = 0
        self.white_moves: List[str] = []
        self.black_moves: List[str] = []

    def on_move_completed(self, event: MoveCompletedEvent) -> None:
        captured = event.captured_piece
        if captured is not None:
            self._add_capture_points(event.piece.color, captured.kind)

        if event.promoted_to_queen:
            self._add_capture_points(event.piece.color, "queen")

        line = self._format_move(event)
        self._append_line(event.piece.color, line)

    def on_counter_capture(self, event: CounterCaptureEvent) -> None:
        self._add_capture_points(event.defender.color, event.captured_piece.kind)
        time_s = event.timestamp_ms / 1000.0
        defender = KIND_LABELS[event.defender.kind]
        cell = square_name(event.cell)
        captured = KIND_LABELS[event.captured_piece.kind]
        line = f"{time_s:.1f}s {defender}: jump x{cell} ({captured})"
        self._append_line(event.defender.color, line)

    def log_jump(self, timestamp_ms: int, piece) -> None:
        time_s = timestamp_ms / 1000.0
        label = KIND_LABELS[piece.kind]
        cell = square_name(piece.cell)
        line = f"{time_s:.1f}s {label}: jump @{cell}"
        self._append_line(piece.color, line)

    def _add_capture_points(self, color: str, kind: str) -> None:
        points = PIECE_VALUES.get(kind, 0)
        if color == WHITE:
            self.score_white += points
        else:
            self.score_black += points

    def _append_line(self, color: str, line: str) -> None:
        if color == WHITE:
            self.white_moves.append(line)
        else:
            self.black_moves.append(line)

    @staticmethod
    def _format_move(event: MoveCompletedEvent) -> str:
        time_s = event.timestamp_ms / 1000.0
        label = KIND_LABELS[event.piece.kind]
        source = square_name(event.source)
        destination = square_name(event.destination)
        if event.captured_piece is not None:
            move_text = f"{source}x{destination}"
        else:
            move_text = f"{source}->{destination}"
        return f"{time_s:.1f}s {label}: {move_text}"
