import pytest

from kungfu_chess.io.board_parser import BoardParser
from kungfu_chess.model.board import Board
from kungfu_chess.model.piece import BLACK, PAWN, QUEEN, WHITE, Piece
from kungfu_chess.model.position import Position
from kungfu_chess.rules.pawn_rule import PawnRule
from kungfu_chess.rules.promotion_service import PromotionService


def make_board(board_text: str) -> Board:
    return BoardParser().parse(board_text)


class TestPawnRule:
    def setup_method(self):
        self._rule = PawnRule()

    def test_single_step_forward_on_empty_square(self):
        board = make_board(". . .\n. wP .\n. . .")
        piece = board.piece_at(Position(1, 1))
        assert self._rule.can_move(
            board, piece, Position(1, 1), Position(0, 1)
        )

    def test_double_step_from_start_row_when_path_clear(self):
        board = make_board(
            ". . .\n. . .\n. . .\n. wP .\n. . ."
        )
        piece = board.piece_at(Position(3, 1))
        assert self._rule.can_move(
            board, piece, Position(3, 1), Position(1, 1)
        )

    def test_double_step_rejected_when_intermediate_square_blocked(self):
        board = make_board(
            ". . .\n. . .\n. wR .\n. wP .\n. . ."
        )
        piece = board.piece_at(Position(3, 1))
        assert not self._rule.can_move(
            board, piece, Position(3, 1), Position(1, 1)
        )

    def test_double_step_rejected_when_not_on_start_row(self):
        board = make_board(". . .\n. . .\n. . .\n. wP .")
        piece = board.piece_at(Position(3, 1))
        assert not self._rule.can_move(
            board, piece, Position(3, 1), Position(1, 1)
        )

    def test_double_step_rejected_when_destination_occupied(self):
        board = make_board(
            ". . .\n. wP .\n. . .\n. wP .\n. . ."
        )
        piece = board.piece_at(Position(3, 1))
        assert not self._rule.can_move(
            board, piece, Position(3, 1), Position(1, 1)
        )


class TestPromotionService:
    def setup_method(self):
        self._service = PromotionService()

    def test_white_pawn_on_last_row_becomes_queen(self):
        board = Board(width=3, height=3)
        pawn = Piece(
            id="p1",
            color=WHITE,
            kind=PAWN,
            cell=Position(0, 1),
        )
        board.add_piece(pawn)
        self._service.apply_if_needed(pawn, board)
        assert pawn.kind == QUEEN

    def test_black_pawn_on_last_row_becomes_queen(self):
        board = Board(width=3, height=3)
        pawn = Piece(
            id="p1",
            color=BLACK,
            kind=PAWN,
            cell=Position(2, 1),
        )
        board.add_piece(pawn)
        self._service.apply_if_needed(pawn, board)
        assert pawn.kind == QUEEN

    def test_pawn_not_on_last_row_stays_pawn(self):
        board = Board(width=3, height=3)
        pawn = Piece(
            id="p1",
            color=WHITE,
            kind=PAWN,
            cell=Position(1, 1),
        )
        board.add_piece(pawn)
        self._service.apply_if_needed(pawn, board)
        assert pawn.kind == PAWN
