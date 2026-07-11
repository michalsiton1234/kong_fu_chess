from kungfu_chess.texttests.script_parser import ScriptParser


def test_splits_board_text_and_command_lines():
    text = "Board:\nwK . bR\n. . .\nCommands:\nprint board"
    board_text, commands = ScriptParser().parse(text)
    assert board_text == "wK . bR\n. . ."
    assert commands == ["print board"]


def test_marker_detection_is_case_insensitive():
    text = "board:\nwK .\ncommands:\nprint board"
    board_text, commands = ScriptParser().parse(text)
    assert board_text == "wK ."
    assert commands == ["print board"]


def test_blank_lines_are_ignored():
    text = "Board:\n\nwK .\n\nCommands:\n\nprint board\n"
    board_text, commands = ScriptParser().parse(text)
    assert board_text == "wK ."
    assert commands == ["print board"]


def test_missing_commands_section_yields_no_commands():
    board_text, commands = ScriptParser().parse("Board:\nwK .")
    assert board_text == "wK ."
    assert commands == []


def test_missing_board_section_yields_empty_board_text():
    board_text, commands = ScriptParser().parse("Commands:\nprint board")
    assert board_text == ""
    assert commands == ["print board"]


def test_empty_text_yields_empty_results():
    board_text, commands = ScriptParser().parse("")
    assert board_text == ""
    assert commands == []
