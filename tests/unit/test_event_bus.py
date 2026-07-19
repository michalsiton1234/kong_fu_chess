"""Tests for pub/sub event bus integration with game events."""
from kungfu_chess.engine.event_bus import SynchronousEventBus
from kungfu_chess.engine.game_engine import GameEngine
from kungfu_chess.engine.game_events import MoveCompletedEvent


class BusRecorder:
    def __init__(self):
        self.events = []

    def handle(self, event) -> None:
        self.events.append(event)


class TestEventBus:
    def test_move_completed_published_to_bus_subscriber(self):
        board = BoardParser().parse("wR . .\n. . .\n. . .")
        white_rook = board.piece_at(Position(0, 0))
        engine = GameEngine()
        recorder = BusRecorder()
        engine.subscribe(MoveCompletedEvent, recorder)

        engine.request_move(board, white_rook, white_rook.cell, Position(0, 1))
        engine.advance_time(board, 1000)

        assert len(recorder.events) == 1
        assert recorder.events[0].destination == Position(0, 1)
