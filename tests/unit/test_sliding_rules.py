from kungfu_chess.io.board_parser import BoardParser
from kungfu_chess.model.position import Position
from kungfu_chess.rules.bishop_rule import BishopRule
from kungfu_chess.rules.queen_rule import QueenRule
from kungfu_chess.rules.rook_rule import RookRule


def make_board(text):
    return BoardParser().parse(text)


class TestRookRule:
    def test_rejects_non_straight_move(self):
        board = make_board("wR . .\n. . .\n. . .")
        rook = board.piece_at(Position(0, 0))
        rule = RookRule()
        assert not rule.can_move(
            board, rook, Position(0, 0), Position(1, 1)
        )


class TestBishopRule:
    def test_rejects_non_diagonal_move(self):
        board = make_board("wB . .\n. . .\n. . .")
        bishop = board.piece_at(Position(0, 0))
        rule = BishopRule()
        assert not rule.can_move(
            board, bishop, Position(0, 0), Position(0, 2)
        )


class TestQueenRule:
    def test_rejects_invalid_geometry(self):
        board = make_board("wQ . .\n. . .\n. . .")
        queen = board.piece_at(Position(0, 0))
        rule = QueenRule()
        assert not rule.can_move(
            board, queen, Position(0, 0), Position(1, 2)
        )
