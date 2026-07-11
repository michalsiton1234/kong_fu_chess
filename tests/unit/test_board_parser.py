import pytest

from kungfu_chess.io.board_parser import BoardParser
from kungfu_chess.io.exceptions import RowWidthMismatchError, UnknownTokenError
from kungfu_chess.model.piece import BLACK, KING, ROOK, WHITE
from kungfu_chess.model.position import Position


def test_board_dimensions_are_inferred_from_text():
    board = BoardParser().parse("wK . bR\n. . .\n. wN bK")
    assert board.width == 3
    assert board.height == 3


def test_board_parser_accepts_a_rectangular_board():
    board = BoardParser().parse("wK . . bK\n. . . .\nwR . . bR")
    assert board.width == 4
    assert board.height == 3


def test_pieces_are_stored_by_position():
    board = BoardParser().parse("wK . bR\n. . .\n. wN bK")
    piece = board.piece_at(Position(0, 0))
    assert piece.color == WHITE
    assert piece.kind == KING


def test_empty_cells_are_represented_by_dot():
    board = BoardParser().parse("wK . bR")
    assert board.piece_at(Position(0, 1)) is None


def test_board_parser_rejects_inconsistent_row_length():
    with pytest.raises(RowWidthMismatchError):
        BoardParser().parse("wK . .\n. bK")


def test_board_parser_rejects_illegal_piece_token():
    with pytest.raises(UnknownTokenError):
        BoardParser().parse("wK xZ\n. .")


def test_duplicate_occupancy_is_impossible_via_parsing():
    # Every parsed piece gets a distinct cell by construction (one token per
    # cell), so there is no way for BoardParser to produce two pieces on the
    # same cell - this documents that guarantee explicitly.
    board = BoardParser().parse("wK bR\n. .")
    assert board.piece_at(Position(0, 0)).kind == KING
    assert board.piece_at(Position(0, 1)).color == BLACK


def test_piece_ids_are_unique_across_a_parse():
    board = BoardParser().parse("wK bR\nwR bK")
    ids = {
        board.piece_at(Position(0, 0)).id,
        board.piece_at(Position(0, 1)).id,
        board.piece_at(Position(1, 0)).id,
        board.piece_at(Position(1, 1)).id,
    }
    assert len(ids) == 4


def test_empty_text_yields_zero_sized_board():
    board = BoardParser().parse("")
    assert board.width == 0
    assert board.height == 0
