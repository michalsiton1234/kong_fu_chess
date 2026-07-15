import io
from unittest.mock import Mock

from kungfu_chess.texttests.script_runner import TextTestRunner


def run(script_text: str) -> str:
    output = io.StringIO()
    TextTestRunner().run(io.StringIO(script_text), output)
    return output.getvalue()


class TestScriptRunnerEdgeCases:
    def test_empty_input_produces_no_output(self):
        assert run("") == ""

    def test_missing_board_section_produces_no_output(self):
        assert run("Commands:\nprint board\n") == ""

    def test_empty_command_line_in_loop_is_skipped(self):
        mock_parser = Mock()
        mock_parser.parse.return_value = (".", ["", "print board"])
        output = io.StringIO()
        TextTestRunner(script_parser=mock_parser).run(io.StringIO("x"), output)
        assert output.getvalue().strip() == "."

    def test_blank_command_lines_are_skipped(self):
        script = "Board:\n.\nCommands:\n   \nprint board\n"
        assert run(script).strip() == "."

    def test_invalid_wait_command_is_ignored(self):
        script = (
            "Board:\n"
            "wR . .\n"
            "Commands:\n"
            "wait\n"
            "wait abc\n"
            "wait 100 200\n"
            "print board\n"
        )
        assert run(script).strip() == "wR . ."

    def test_invalid_click_command_is_ignored(self):
        script = (
            "Board:\n"
            "wR . .\n"
            "Commands:\n"
            "click\n"
            "click 50\n"
            "click abc 50\n"
            "print board\n"
        )
        assert run(script).strip() == "wR . ."

    def test_invalid_jump_command_is_ignored(self):
        script = (
            "Board:\n"
            "wR . .\n"
            "Commands:\n"
            "jump\n"
            "jump 50\n"
            "jump abc 50\n"
            "print board\n"
        )
        assert run(script).strip() == "wR . ."
