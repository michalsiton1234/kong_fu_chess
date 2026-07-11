from kungfu_chess.model.position import Position


def test_two_positions_with_same_row_and_col_are_equal():
    assert Position(2, 3) == Position(2, 3)


def test_two_positions_with_different_row_are_not_equal():
    assert Position(2, 3) != Position(5, 3)


def test_two_positions_with_different_col_are_not_equal():
    assert Position(2, 3) != Position(2, 9)


def test_position_has_readable_representation():
    text = str(Position(2, 3))
    assert "2" in text and "3" in text
