from kfc.board import Board


def test_width_and_height():
    board = Board([["wR", "wN"], [".", "."]])
    assert board.height == 2
    assert board.width == 2


def test_empty_board_has_zero_width_and_height():
    board = Board([])
    assert board.height == 0
    assert board.width == 0


def test_get_row_returns_defensive_copy():
    board = Board([["wR", "wN"]])
    row = board.get_row(0)
    row[0] = "MUTATED"
    assert board.get_row(0) == ["wR", "wN"]


def test_rows_iterates_all_rows_in_order():
    board = Board([["a", "b"], ["c", "d"]])
    assert list(board.rows()) == [["a", "b"], ["c", "d"]]


def test_constructor_copies_input_rows_defensively():
    original_rows = [["wR", "wN"]]
    board = Board(original_rows)
    original_rows[0][0] = "MUTATED"
    assert board.get_row(0) == ["wR", "wN"]


def test_to_text_renders_rows_joined_by_spaces_and_newlines():
    board = Board([["wR", "wN"], [".", "."]])
    assert board.to_text() == "wR wN\n. ."


def test_to_text_renders_empty_board_as_empty_string():
    assert Board([]).to_text() == ""
