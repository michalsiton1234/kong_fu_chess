"""Game events for Observer pattern (move log, score, UI adapters)."""
from dataclasses import dataclass
from typing import Optional, Protocol

from ..model.piece import Piece
from ..model.position import Position


@dataclass(frozen=True)
class MoveCompletedEvent:
    timestamp_ms: int
    piece: Piece
    source: Position
    destination: Position
    captured_piece: Optional[Piece]
    promoted_to_queen: bool


@dataclass(frozen=True)
class CounterCaptureEvent:
    timestamp_ms: int
    defender: Piece
    captured_piece: Piece
    cell: Position


class GameObserver(Protocol):
    def on_move_completed(self, event: MoveCompletedEvent) -> None:
        ...

    def on_counter_capture(self, event: CounterCaptureEvent) -> None:
        ...
