from kungfu_chess.model.piece import CAPTURED, IDLE, KING, MOVING, WHITE, Piece
from kungfu_chess.model.position import Position


def make_piece(**overrides):
    defaults = dict(id="p1", color=WHITE, kind=KING, cell=Position(0, 0))
    defaults.update(overrides)
    return Piece(**defaults)


def test_piece_defaults_to_idle_state():
    piece = make_piece()
    assert piece.state == IDLE


def test_piece_state_can_become_moving():
    piece = make_piece()
    piece.state = MOVING
    assert piece.state == MOVING


def test_piece_state_can_become_captured():
    piece = make_piece()
    piece.state = CAPTURED
    assert piece.state == CAPTURED


def test_piece_stores_color_kind_and_cell():
    cell = Position(4, 5)
    piece = make_piece(color=WHITE, kind=KING, cell=cell)
    assert piece.color == WHITE
    assert piece.kind == KING
    assert piece.cell == cell
