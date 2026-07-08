from kfc.input_parser import InputParser


def test_parses_board_rows_and_recognizes_print_command():
    text = "board:\nwR wN\n. .\ncommands:\nprint board"
    board_rows, commands = InputParser().parse(text)
    assert board_rows == [["wR", "wN"], [".", "."]]
    assert commands == {"print_board"}


def test_marker_detection_is_case_insensitive():
    text = "Board:\nwR .\nCommands:\nPrint Board"
    board_rows, commands = InputParser().parse(text)
    assert board_rows == [["wR", "."]]
    assert commands == {"print_board"}


def test_blank_lines_are_ignored():
    text = "board:\n\nwR .\n\ncommands:\n\nprint board\n"
    board_rows, commands = InputParser().parse(text)
    assert board_rows == [["wR", "."]]
    assert commands == {"print_board"}


def test_no_board_marker_means_all_lines_are_command_lines():
    text = "print board"
    board_rows, commands = InputParser().parse(text)
    assert board_rows == []
    assert commands == {"print_board"}


def test_command_recognized_when_embedded_in_a_longer_line():
    text = "board:\nwR .\ncommands:\nplease print board now"
    _, commands = InputParser().parse(text)
    assert commands == {"print_board"}


def test_unknown_command_line_is_ignored():
    text = "board:\nwR .\ncommands:\nfly to the moon"
    _, commands = InputParser().parse(text)
    assert commands == set()


def test_missing_commands_section_yields_no_commands():
    text = "board:\nwR .\n"
    _, commands = InputParser().parse(text)
    assert commands == set()


def test_empty_text_yields_empty_results():
    board_rows, commands = InputParser().parse("")
    assert board_rows == []
    assert commands == set()
