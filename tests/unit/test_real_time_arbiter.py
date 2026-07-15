from kungfu_chess.engine.jump import JUMP_DURATION_MS, Jump
from kungfu_chess.engine.motion import Motion
from kungfu_chess.engine.real_time_arbiter import RealTimeArbiter
from kungfu_chess.io.board_parser import BoardParser
from kungfu_chess.model.position import Position


def make_board(text):
    return BoardParser().parse(text)


class TestRealTimeArbiter:
    def setup_method(self):
        self._arbiter = RealTimeArbiter()
        self._game_over = False

    def _is_game_over(self):
        return self._game_over

    def _mark_game_over(self):
        self._game_over = True

    def _apply(self, board):
        self._arbiter.apply_completed_motions(
            board, self._is_game_over, self._mark_game_over
        )

    def test_skips_motions_after_game_over(self):
        board = make_board("wR . .")
        rook = board.piece_at(Position(0, 0))
        self._game_over = True
        self._arbiter.schedule(
            Motion(0, Position(0, 0), Position(0, 1), rook)
        )
        self._apply(board)
        assert board.piece_at(Position(0, 0)) == rook

    def test_skips_motion_when_source_piece_changed(self):
        board = make_board("wR . .")
        rook = board.piece_at(Position(0, 0))
        self._arbiter.schedule(
            Motion(0, Position(0, 0), Position(0, 1), rook)
        )
        board.remove_piece(Position(0, 0))
        self._apply(board)
        assert board.piece_at(Position(0, 1)) is None

    def test_cancels_friendly_landing_at_destination(self):
        board = make_board("wR wK .")
        rook = board.piece_at(Position(0, 0))
        self._arbiter.schedule(
            Motion(0, Position(0, 0), Position(0, 1), rook)
        )
        self._apply(board)
        assert board.piece_at(Position(0, 0)) == rook
        assert board.piece_at(Position(0, 1)).kind == "king"

    def test_airborne_counter_capture_removes_arriving_enemy(self):
        board = make_board("wR bR .")
        white_rook = board.piece_at(Position(0, 0))
        black_rook = board.piece_at(Position(0, 1))
        self._arbiter.schedule_jump(
            Jump(0, JUMP_DURATION_MS, white_rook, Position(0, 0))
        )
        self._arbiter.schedule(
            Motion(500, Position(0, 1), Position(0, 0), black_rook)
        )
        self._arbiter.advance_time(500)
        self._apply(board)
        assert board.piece_at(Position(0, 0)) == white_rook
        assert board.piece_at(Position(0, 1)) is None

    def test_airborne_counter_capture_ignores_friendly_arrival(self):
        board = make_board("wR wK .")
        rook = board.piece_at(Position(0, 0))
        king = board.piece_at(Position(0, 1))
        self._arbiter.schedule_jump(
            Jump(0, JUMP_DURATION_MS, rook, Position(0, 0))
        )
        self._arbiter.schedule(
            Motion(500, Position(0, 1), Position(0, 0), king)
        )
        self._arbiter.advance_time(500)
        self._apply(board)
        assert board.piece_at(Position(0, 0)) == rook

    def test_airborne_counter_capture_skips_when_enemy_source_empty(self):
        board = make_board("wR . bR")
        white_rook = board.piece_at(Position(0, 0))
        black_rook = board.piece_at(Position(0, 2))
        self._arbiter.schedule_jump(
            Jump(0, JUMP_DURATION_MS, white_rook, Position(0, 0))
        )
        self._arbiter.schedule(
            Motion(500, Position(0, 2), Position(0, 0), black_rook)
        )
        board.remove_piece(Position(0, 2))
        self._arbiter.advance_time(500)
        self._apply(board)
        assert board.piece_at(Position(0, 0)) == white_rook

    def test_airborne_counter_capture_on_king_ends_game(self):
        board = make_board("wR . bK")
        white_rook = board.piece_at(Position(0, 0))
        black_king = board.piece_at(Position(0, 2))
        self._arbiter.schedule_jump(
            Jump(0, JUMP_DURATION_MS, white_rook, Position(0, 0))
        )
        self._arbiter.schedule(
            Motion(500, Position(0, 2), Position(0, 0), black_king)
        )
        self._arbiter.advance_time(500)
        self._apply(board)
        assert self._game_over

    def test_active_jump_at_ignores_jumps_on_other_cells(self):
        board = make_board("wR . bR")
        white_rook = board.piece_at(Position(0, 0))
        black_rook = board.piece_at(Position(0, 2))
        self._arbiter.schedule_jump(
            Jump(0, JUMP_DURATION_MS, white_rook, Position(0, 0))
        )
        self._arbiter.schedule(
            Motion(500, Position(0, 2), Position(0, 1), black_rook)
        )
        self._arbiter.advance_time(500)
        self._apply(board)
        assert board.piece_at(Position(0, 1)) == black_rook

    def test_jump_expires_after_land_time(self):
        board = make_board("wR . .")
        rook = board.piece_at(Position(0, 0))
        self._arbiter.schedule_jump(
            Jump(0, JUMP_DURATION_MS, rook, Position(0, 0))
        )
        self._arbiter.advance_time(JUMP_DURATION_MS)
        self._apply(board)
        assert not self._arbiter.is_piece_airborne(rook)
