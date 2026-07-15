from kungfu_chess.io.board_parser import BoardParser
from kungfu_chess.model.position import Position
from kungfu_chess.rules.king_rule import KingRule


def make_board(board_text: str):
    return BoardParser().parse(board_text)


class TestKingRule:
    def setup_method(self):
        self._rule = KingRule()

    def test_king_moves_one_square_in_any_direction(self):
        board = make_board("wK . .\n. . .\n. . .")
        king = board.piece_at(Position(0, 0))
        assert self._rule.can_move(
            board, king, Position(0, 0), Position(1, 1)
        )

    def test_king_cannot_move_more_than_one_square(self):
        board = make_board("wK . .\n. . .\n. . .")
        king = board.piece_at(Position(0, 0))
        assert not self._rule.can_move(
            board, king, Position(0, 0), Position(0, 2)
        )

    def test_king_cannot_move_like_a_knight(self):
        board = make_board("wK . .\n. . .\n. . .")
        king = board.piece_at(Position(0, 0))
        assert not self._rule.can_move(
            board, king, Position(0, 0), Position(2, 1)
        )
