import io

from kungfu_chess.texttests.script_runner import TextTestRunner

VALID_SCRIPT = (
    "Board:\n"
    "wK . . bK\n"
    ". . . .\n"
    "wR . . bR\n"
    "Commands:\n"
    "print board\n"
)


def run(text: str) -> str:
    output = io.StringIO()
    TextTestRunner().run(io.StringIO(text), output)
    return output.getvalue()


def test_prints_board_on_valid_script_with_print_command():
    assert run(VALID_SCRIPT).strip() == "wK . . bK\n. . . .\nwR . . bR"


def test_no_output_when_print_command_absent():
    text = "Board:\nwK .\n. .\nCommands:\n"
    assert run(text) == ""


def test_unknown_token_error_is_printed():
    text = "Board:\nxZ .\n. .\nCommands:\nprint board"
    assert run(text).strip() == "ERROR UNKNOWN_TOKEN"


def test_row_width_mismatch_error_is_printed():
    text = "Board:\nwK . .\n. .\nCommands:\nprint board"
    assert run(text).strip() == "ERROR ROW_WIDTH_MISMATCH"


def test_empty_input_produces_no_output():
    assert run("") == ""


def test_missing_board_section_produces_no_output():
    assert run("Commands:\nprint board") == ""


def test_default_dependencies_are_constructed_when_none_provided():
    runner = TextTestRunner(script_parser=None, board_parser=None, print_board=None)
    output = io.StringIO()
    runner.run(io.StringIO(VALID_SCRIPT), output)
    assert output.getvalue() != ""
