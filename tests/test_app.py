import io

from kfc.app import KongFuChessApp

VALID_BOARD = (
    "board:\n"
    "wR wN wB wQ wK wB wN wR\n"
    "wP wP wP wP wP wP wP wP\n"
    ". . . . . . . .\n"
    ". . . . . . . .\n"
    ". . . . . . . .\n"
    ". . . . . . . .\n"
    "bP bP bP bP bP bP bP bP\n"
    "bR bN bB bQ bK bB bN bR\n"
    "commands:\n"
    "print board\n"
)


def run_app(input_text: str) -> str:
    output = io.StringIO()
    KongFuChessApp().run(io.StringIO(input_text), output)
    return output.getvalue()


def test_prints_board_on_valid_input_with_print_command():
    output = run_app(VALID_BOARD)
    assert output.strip().splitlines()[0] == "wR wN wB wQ wK wB wN wR"
    assert output.strip().splitlines()[-1] == "bR bN bB bQ bK bB bN bR"


def test_no_output_when_print_command_absent():
    text = "board:\nwR .\n. .\ncommands:\n"
    assert run_app(text) == ""


def test_unknown_token_error_is_printed():
    text = "board:\nwX .\n. .\ncommands:\nprint board"
    assert run_app(text).strip() == "ERROR UNKNOWN_TOKEN"


def test_row_width_mismatch_error_is_printed():
    text = "board:\nwR . .\n. .\ncommands:\nprint board"
    assert run_app(text).strip() == "ERROR ROW_WIDTH_MISMATCH"


def test_empty_input_produces_no_output():
    assert run_app("") == ""


def test_no_board_section_produces_no_output():
    assert run_app("commands:\nprint board") == ""


def test_default_dependencies_are_constructed_when_none_provided():
    # Exercises the default-dependency branches of the constructor directly.
    app = KongFuChessApp(parser=None, validator=None)
    output = io.StringIO()
    app.run(io.StringIO(VALID_BOARD), output)
    assert output.getvalue() != ""
