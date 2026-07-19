"""Tests for game observer events fired on move completion."""
from kungfu_chess.engine.game_engine import GameEngine
from kungfu_chess.io.board_parser import BoardParser
from kungfu_chess.model.position import Position


class RecordingObserver:
    def __init__(self):
        self.move_events = []
        self.counter_events = []

    def on_move_completed(self, event):
        self.move_events.append(event)

    def on_counter_capture(self, event):
        self.counter_events.append(event)


class TestGameObserverEvents:
    def test_move_completed_event_includes_capture(self):
        board = BoardParser().parse(
            "wR bR .\n"
            ". . .\n"
            ". . ."
        )
        white_rook = board.piece_at(Position(0, 0))
        engine = GameEngine()
        observer = RecordingObserver()
        engine.add_observer(observer)

        engine.request_move(
            board, white_rook, white_rook.cell, Position(0, 1)
        )
        engine.advance_time(board, 1000)

        assert len(observer.move_events) == 1
        event = observer.move_events[0]
        assert event.captured_piece is not None
        assert event.captured_piece.kind == "rook"
        assert event.timestamp_ms == 1000

    def test_move_completed_event_without_capture(self):
        board = BoardParser().parse("wR . .\n. . .\n. . .")
        white_rook = board.piece_at(Position(0, 0))
        engine = GameEngine()
        observer = RecordingObserver()
        engine.add_observer(observer)

        engine.request_move(board, white_rook, white_rook.cell, Position(0, 1))
        engine.advance_time(board, 1000)

        assert len(observer.move_events) == 1
        assert observer.move_events[0].captured_piece is None
