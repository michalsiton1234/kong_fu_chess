"""KungFuChessApp is the composition root: it wires TextTestRunner and hands
it real stdin/stdout. Kept separate from main.py so tests can construct and
run the app against io.StringIO without touching sys.stdin/sys.stdout."""
from typing import Optional, TextIO

from .texttests.script_runner import TextTestRunner


class KungFuChessApp:
    def __init__(self, runner: Optional[TextTestRunner] = None):
        self._runner = runner or TextTestRunner()

    def run(self, input_stream: TextIO, output_stream: TextIO) -> None:
        self._runner.run(input_stream, output_stream)
