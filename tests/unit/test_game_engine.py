from kungfu_chess.engine.game_engine import GameEngine
from kungfu_chess.engine.jump import JUMP_DURATION_MS, Jump
from kungfu_chess.engine.motion import Motion
from kungfu_chess.io.board_parser import BoardParser
from kungfu_chess.model.position import Position


def make_board(text):
    return BoardParser().parse(text)


class TestGameEngine:
    def setup_method(self):
        self._engine = GameEngine()
        self._board = make_board("wR . bK\n. . .\n. . .")

    def test_request_move_rejected_when_game_over(self):
        self._engine._game_over = True
        rook = self._board.piece_at(Position(0, 0))
        assert not self._engine.request_move(
            self._board, rook, Position(0, 0), Position(0, 1)
        )

    def test_request_move_rejected_when_source_is_moving(self):
        rook = self._board.piece_at(Position(0, 0))
        self._engine.arbiter.schedule(
            Motion(1000, Position(0, 0), Position(0, 1), rook)
        )
        assert not self._engine.request_move(
            self._board, rook, Position(0, 0), Position(0, 1)
        )

    def test_request_move_rejected_when_piece_is_airborne(self):
        rook = self._board.piece_at(Position(0, 0))
        self._engine.arbiter.schedule_jump(
            Jump(0, JUMP_DURATION_MS, rook, Position(0, 0))
        )
        assert not self._engine.request_move(
            self._board, rook, Position(0, 0), Position(0, 1)
        )

    def test_request_move_rejected_on_destination_conflict(self):
        rook = self._board.piece_at(Position(0, 0))
        king = self._board.piece_at(Position(0, 2))
        self._engine.arbiter.schedule(
            Motion(1000, Position(0, 2), Position(0, 1), king)
        )
        assert not self._engine.request_move(
            self._board, rook, Position(0, 0), Position(0, 1)
        )

    def test_request_jump_rejected_when_game_over(self):
        rook = self._board.piece_at(Position(0, 0))
        self._engine._game_over = True
        assert not self._engine.request_jump(
            self._board, rook, Position(0, 0)
        )

    def test_request_jump_rejected_when_piece_not_on_cell(self):
        rook = self._board.piece_at(Position(0, 0))
        assert not self._engine.request_jump(
            self._board, rook, Position(1, 1)
        )

    def test_request_jump_rejected_when_cell_is_moving(self):
        rook = self._board.piece_at(Position(0, 0))
        self._engine.arbiter.schedule(
            Motion(1000, Position(0, 0), Position(0, 1), rook)
        )
        assert not self._engine.request_jump(
            self._board, rook, Position(0, 0)
        )

    def test_request_jump_rejected_when_piece_in_motion(self):
        rook = self._board.piece_at(Position(0, 0))
        self._engine.arbiter.schedule(
            Motion(1000, Position(0, 0), Position(0, 1), rook)
        )
        assert not self._engine.request_jump(
            self._board, rook, Position(0, 0)
        )

    def test_request_jump_rejected_when_piece_already_airborne(self):
        rook = self._board.piece_at(Position(0, 0))
        self._engine.arbiter.schedule_jump(
            Jump(0, JUMP_DURATION_MS, rook, Position(0, 0))
        )
        assert not self._engine.request_jump(
            self._board, rook, Position(0, 0)
        )

    def test_request_jump_rejected_when_piece_in_motion_from_other_cell(self):
        rook = self._board.piece_at(Position(0, 0))
        self._engine.arbiter.schedule(
            Motion(1000, Position(0, 1), Position(0, 2), rook)
        )
        assert not self._engine.request_jump(
            self._board, rook, Position(0, 0)
        )

    def test_reset_clears_game_over_and_arbiter(self):
        self._engine._game_over = True
        self._engine.reset()
        assert not self._engine.game_over
