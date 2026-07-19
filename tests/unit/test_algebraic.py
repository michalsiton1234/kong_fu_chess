from kungfu_chess.io.algebraic import square_name
from kungfu_chess.model.position import Position


class TestAlgebraic:
    def test_white_back_rank_square(self):
        assert square_name(Position(7, 4)) == "e1"

    def test_black_back_rank_square(self):
        assert square_name(Position(0, 4)) == "e8"

    def test_middle_board_square(self):
        assert square_name(Position(4, 3)) == "d4"
