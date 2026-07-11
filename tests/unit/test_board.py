import pytest

from kungfu_chess.model.board import Board
from kungfu_chess.model.exceptions import DuplicateOccupancyError, PieceNotFoundError
from kungfu_chess.model.piece import KING, ROOK, WHITE, BLACK, Piece
from kungfu_chess.model.position import Position


def make_piece(piece_id, color, kind, cell):
    return Piece(id=piece_id, color=color, kind=kind, cell=cell)


def test_board_stores_width_and_height():
    board = Board(width=4, height=3)
    assert board.width == 4
    assert board.height == 3


def test_empty_cell_returns_no_piece():
    board = Board(width=3, height=3)
    assert board.piece_at(Position(1, 1)) is None


def test_occupied_cell_returns_the_correct_piece():
    board = Board(width=3, height=3)
    piece = make_piece("p1", WHITE, KING, Position(1, 1))
    board.add_piece(piece)
    assert board.piece_at(Position(1, 1)) is piece


def test_adding_two_pieces_to_the_same_cell_fails():
    board = Board(width=3, height=3)
    board.add_piece(make_piece("p1", WHITE, KING, Position(1, 1)))
    with pytest.raises(DuplicateOccupancyError):
        board.add_piece(make_piece("p2", BLACK, ROOK, Position(1, 1)))


def test_moving_a_piece_updates_source_and_destination():
    board = Board(width=3, height=3)
    piece = make_piece("p1", WHITE, KING, Position(0, 0))
    board.add_piece(piece)

    board.move_piece(Position(0, 0), Position(2, 2))

    assert board.piece_at(Position(0, 0)) is None
    assert board.piece_at(Position(2, 2)) is piece
    assert piece.cell == Position(2, 2)


def test_moving_a_nonexistent_piece_raises():
    board = Board(width=3, height=3)
    with pytest.raises(PieceNotFoundError):
        board.move_piece(Position(0, 0), Position(1, 1))


def test_removing_a_captured_piece_clears_its_cell():
    board = Board(width=3, height=3)
    board.add_piece(make_piece("p1", WHITE, KING, Position(1, 1)))

    board.remove_piece(Position(1, 1))

    assert board.piece_at(Position(1, 1)) is None


def test_removing_from_an_empty_cell_raises():
    board = Board(width=3, height=3)
    with pytest.raises(PieceNotFoundError):
        board.remove_piece(Position(1, 1))


def test_in_bounds_true_for_cell_inside_board():
    board = Board(width=3, height=3)
    assert board.in_bounds(Position(0, 0)) is True
    assert board.in_bounds(Position(2, 2)) is True


def test_in_bounds_false_for_cell_outside_board():
    board = Board(width=3, height=3)
    assert board.in_bounds(Position(3, 0)) is False
    assert board.in_bounds(Position(0, -1)) is False
