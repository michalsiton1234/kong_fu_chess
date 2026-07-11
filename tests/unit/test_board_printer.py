from kungfu_chess.io.board_parser import BoardParser
from kungfu_chess.io.board_printer import BoardPrinter
from kungfu_chess.model.board import Board


def test_board_printer_round_trips_a_simple_board():
    text = ". . .\n. wK .\n. . ."
    board = BoardParser().parse(text)
    assert BoardPrinter().render(board) == text


def test_board_printer_renders_empty_board_as_empty_string():
    assert BoardPrinter().render(Board(width=0, height=0)) == ""
