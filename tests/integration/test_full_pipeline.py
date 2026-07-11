import io

from kungfu_chess.app import KungFuChessApp


def run_app(text: str) -> str:
    output = io.StringIO()
    KungFuChessApp().run(io.StringIO(text), output)
    return output.getvalue()


def test_full_pipeline_parses_and_prints_a_rectangular_board():
    script = (
        "Board:\n"
        "wK . . bK\n"
        ". . . .\n"
        "wR . . bR\n"
        "Commands:\n"
        "print board\n"
    )
    assert run_app(script).strip() == "wK . . bK\n. . . .\nwR . . bR"


def test_full_pipeline_reports_unknown_token():
    script = "Board:\nwK xZ\n. .\nCommands:\nprint board"
    assert run_app(script).strip() == "ERROR UNKNOWN_TOKEN"


def test_full_pipeline_reports_row_width_mismatch():
    script = "Board:\nwK . .\n. bK\nCommands:\nprint board"
    assert run_app(script).strip() == "ERROR ROW_WIDTH_MISMATCH"


def test_full_pipeline_trivial_board_round_trip():
    script = "Board:\n.\nCommands:\nprint board"
    assert run_app(script).strip() == "."
