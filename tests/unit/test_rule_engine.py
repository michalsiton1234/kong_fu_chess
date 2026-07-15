from kungfu_chess.io.board_parser import BoardParser
from kungfu_chess.model.piece import Piece
from kungfu_chess.model.position import Position
from kungfu_chess.rules.rule_engine import RuleEngine


def make_board(text):
    return BoardParser().parse(text)


class TestRuleEngine:
    def setup_method(self):
        self._engine = RuleEngine()

    def test_rejects_move_to_same_cell(self):
        board = make_board("wR . .")
        rook = board.piece_at(Position(0, 0))
        assert not self._engine.validate_move(
            board, rook, Position(0, 0), Position(0, 0)
        )

    def test_rejects_move_onto_friendly_piece(self):
        board = make_board("wR wK .")
        rook = board.piece_at(Position(0, 0))
        assert not self._engine.validate_move(
            board, rook, Position(0, 0), Position(0, 1)
        )

    def test_rejects_unknown_piece_kind(self):
        board = make_board(". . .")
        unknown = Piece(
            id="x1",
            color="white",
            kind="dragon",
            cell=Position(0, 0),
        )
        board.add_piece(unknown)
        assert not self._engine.validate_move(
            board, unknown, Position(0, 0), Position(0, 1)
        )
