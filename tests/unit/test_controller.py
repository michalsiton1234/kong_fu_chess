from kungfu_chess.controller.controller import Controller
from kungfu_chess.engine.game_engine import GameEngine
from kungfu_chess.engine.jump import JUMP_DURATION_MS, Jump
from kungfu_chess.io.board_parser import BoardParser
from kungfu_chess.model.position import Position


def make_board(board_text: str):
    return BoardParser().parse(board_text)


class TestController:
    def setup_method(self):
        self._engine = GameEngine()
        self._controller = Controller(self._engine)

    def test_selected_piece_property_returns_none_initially(self):
        assert self._controller.selected_piece is None

    def test_click_out_of_bounds_is_ignored(self):
        board = make_board("wR . .")
        self._controller.handle_click(board, 999, 999)
        assert self._controller.selected_piece is None

    def test_click_empty_cell_does_not_select(self):
        board = make_board("wR . .")
        self._controller.handle_click(board, 150, 50)
        assert self._controller.selected_piece is None

    def test_click_selects_friendly_piece(self):
        board = make_board("wR . .")
        self._controller.handle_click(board, 50, 50)
        assert self._controller.selected_piece is not None

    def test_click_ignored_when_game_over(self):
        board = make_board("wR . .")
        self._engine._game_over = True
        self._controller.handle_click(board, 50, 50)
        assert self._controller.selected_piece is None

    def test_click_stops_when_game_over_after_apply_pending_moves(self):
        board = make_board("wR . bK")
        self._controller.handle_click(board, 50, 50)
        self._controller.handle_click(board, 250, 50)
        self._engine.arbiter.advance_time(2000)
        self._controller.handle_click(board, 50, 50)
        assert self._controller.selected_piece is None

    def test_jump_stops_when_game_over_after_apply_pending_moves(self):
        board = make_board("wR . bK")
        self._controller.handle_click(board, 50, 50)
        self._controller.handle_click(board, 250, 50)
        self._engine.arbiter.advance_time(2000)
        self._controller.handle_jump(board, 50, 50)

    def test_move_attempt_clears_selection_when_source_is_moving(self):
        board = make_board("wR . . .")
        rook = board.piece_at(Position(0, 0))
        self._controller.handle_click(board, 50, 50)
        self._controller.handle_click(board, 250, 50)
        self._controller._selected_piece = rook
        self._controller.handle_click(board, 350, 50)
        assert self._controller.selected_piece is None

    def test_cannot_select_piece_while_it_is_moving(self):
        board = make_board("wR . . .")
        self._controller.handle_click(board, 50, 50)
        self._controller.handle_click(board, 350, 50)
        self._controller.handle_click(board, 50, 50)
        assert self._controller.selected_piece is None

    def test_cannot_select_airborne_piece(self):
        board = make_board("wR . .")
        self._controller.handle_jump(board, 50, 50)
        self._controller.handle_click(board, 50, 50)
        assert self._controller.selected_piece is None

    def test_cannot_change_selection_to_airborne_piece(self):
        board = make_board("wR wK .")
        king = board.piece_at(Position(0, 1))
        self._controller.handle_click(board, 50, 50)
        self._engine.arbiter.schedule_jump(
            Jump(
                start_time=0,
                land_time=JUMP_DURATION_MS,
                piece=king,
                cell=Position(0, 1),
            )
        )
        self._controller.handle_click(board, 150, 50)
        assert self._controller.selected_piece.kind == "rook"

    def test_cannot_change_selection_to_moving_piece(self):
        board = make_board("wR wK .")
        self._controller.handle_click(board, 50, 50)
        self._controller.handle_click(board, 150, 50)
        self._controller.handle_click(board, 250, 50)
        self._controller.handle_click(board, 50, 50)
        self._controller.handle_click(board, 150, 50)
        assert self._controller.selected_piece.kind == "rook"

    def test_move_attempt_clears_selection_when_source_is_moving(self):
        board = make_board("wR . . .")
        rook = board.piece_at(Position(0, 0))
        self._controller.handle_click(board, 50, 50)
        self._controller.handle_click(board, 250, 50)
        self._controller._selected_piece = rook
        self._controller.handle_click(board, 350, 50)
        assert self._controller.selected_piece is None

    def test_move_attempt_while_selected_piece_is_airborne_clears_selection(self):
        board = make_board("wR . .")
        self._controller.handle_click(board, 50, 50)
        self._engine.arbiter.schedule_jump(
            Jump(
                start_time=0,
                land_time=JUMP_DURATION_MS,
                piece=self._controller.selected_piece,
                cell=Position(0, 0),
            )
        )
        self._controller.handle_click(board, 150, 50)
        assert self._controller.selected_piece is None

    def test_jump_out_of_bounds_is_ignored(self):
        board = make_board("wR . .")
        self._controller.handle_jump(board, 999, 999)

    def test_jump_on_empty_cell_is_ignored(self):
        board = make_board("wR . .")
        self._controller.handle_jump(board, 150, 50)

    def test_jump_ignored_when_game_over(self):
        board = make_board("wR . .")
        self._engine._game_over = True
        self._controller.handle_jump(board, 50, 50)

    def test_jump_stops_when_game_over_after_apply_pending_moves(self):
        board = make_board("wR . bK")
        self._controller.handle_click(board, 50, 50)
        self._controller.handle_click(board, 250, 50)
        self._engine.arbiter.advance_time(2000)
        self._controller.handle_jump(board, 50, 50)

    def test_jump_clears_selection(self):
        board = make_board("wR . .")
        self._controller.handle_click(board, 50, 50)
        self._controller.handle_jump(board, 50, 50)
        assert self._controller.selected_piece is None

    def test_reset_clears_selection(self):
        board = make_board("wR . .")
        self._controller.handle_click(board, 50, 50)
        self._controller.reset()
        assert self._controller.selected_piece is None
