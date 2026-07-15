import io

from kungfu_chess.texttests.script_runner import TextTestRunner


def run(script_text: str) -> str:
    runner = TextTestRunner()
    output = io.StringIO()
    runner.run(io.StringIO(script_text), output)
    return output.getvalue().strip()


def test_jump_keeps_piece_on_same_cell():
    script = (
        "Board:\n"
        "wR . .\n"
        "Commands:\n"
        "jump 50 50\n"
        "wait 1000\n"
        "print board\n"
    )
    assert run(script) == "wR . ."


def test_airborne_piece_captures_arriving_enemy():
    script = (
        "Board:\n"
        "wR bR .\n"
        "Commands:\n"
        "jump 50 50\n"
        "click 150 50\n"
        "click 50 50\n"
        "wait 1000\n"
        "print board\n"
    )
    assert run(script) == "wR . ."


def test_moving_piece_cannot_jump():
    script = (
        "Board:\n"
        "wR . . .\n"
        "Commands:\n"
        "click 50 50\n"
        "click 350 50\n"
        "jump 50 50\n"
        "wait 3000\n"
        "print board\n"
    )
    assert run(script) == ". . . wR"


def test_airborne_piece_cannot_jump_again():
    script = (
        "Board:\n"
        "wR . .\n"
        "Commands:\n"
        "jump 50 50\n"
        "jump 50 50\n"
        "wait 1000\n"
        "print board\n"
    )
    assert run(script) == "wR . ."


def test_enemy_arrives_after_jump_window_captures_normally():
    script = (
        "Board:\n"
        "wR bR .\n"
        "Commands:\n"
        "jump 50 50\n"
        "wait 500\n"
        "click 150 50\n"
        "click 50 50\n"
        "wait 1000\n"
        "print board\n"
    )
    assert run(script) == "bR . ."
