"""
TextTestRunner drives a full script (board text + commands) end-to-end
without any GUI (architecture Rule 2 — Textual I/O Simulation for Testing).

PrintBoard is the one command currently supported: it renders the current
Board via BoardPrinter. It is deliberately its own tiny class — rather than
a branch inline in TextTestRunner — so that adding future commands means
adding another small command class and one line in KNOWN_COMMANDS, never
editing TextTestRunner's control flow itself.

Recognized commands are data-driven (KNOWN_COMMANDS), not hardcoded
if/elif chains, so a new command is a one-line addition here.
"""
from typing import Dict, Optional, Set, TextIO

from ..io.board_parser import BoardParser
from ..io.board_printer import BoardPrinter
from ..io.exceptions import BoardTextError
from ..model.board import Board
from .script_parser import ScriptParser

PRINT_BOARD = "print_board"

KNOWN_COMMANDS: Dict[str, str] = {
    "print board": PRINT_BOARD,
}


class PrintBoard:
    def __init__(self, printer: Optional[BoardPrinter] = None):
        self._printer = printer or BoardPrinter()

    def execute(self, board: Board, output_stream: TextIO) -> None:
        print(self._printer.render(board), file=output_stream)


class TextTestRunner:
    def __init__(
        self,
        script_parser: Optional[ScriptParser] = None,
        board_parser: Optional[BoardParser] = None,
        print_board: Optional[PrintBoard] = None,
    ):
        self._script_parser = script_parser or ScriptParser()
        self._board_parser = board_parser or BoardParser()
        self._print_board = print_board or PrintBoard()

    def run(self, input_stream: TextIO, output_stream: TextIO) -> None:
        raw_text = input_stream.read().strip()
        if not raw_text:
            return

        board_text, command_lines = self._script_parser.parse(raw_text)
        if not board_text:
            return

        try:
            board = self._board_parser.parse(board_text)
        except BoardTextError as error:
            print(error.error_code, file=output_stream)
            return

        commands = self._recognize_commands(command_lines)
        if PRINT_BOARD in commands:
            self._print_board.execute(board, output_stream)

    @staticmethod
    def _recognize_commands(command_lines) -> Set[str]:
        recognized: Set[str] = set()
        for line in command_lines:
            for phrase, command_id in KNOWN_COMMANDS.items():
                if phrase in line:
                    recognized.add(command_id)
        return recognized
