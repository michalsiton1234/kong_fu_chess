"""
TextTestRunner drives a full script (board text + commands) end-to-end
without any GUI (architecture Rule 2 — Textual I/O Simulation for Testing).
"""
from typing import Optional, TextIO

from ..controller.controller import Controller
from ..engine.game_engine import GameEngine
from ..io.board_parser import BoardParser
from ..io.board_printer import BoardPrinter
from ..io.exceptions import BoardTextError
from ..model.board import Board
from .print_board import PrintBoard
from .script_parser import ScriptParser


class TextTestRunner:
    def __init__(
        self,
        script_parser: Optional[ScriptParser] = None,
        board_parser: Optional[BoardParser] = None,
        board_printer: Optional[BoardPrinter] = None,
        game_engine: Optional[GameEngine] = None,
        controller: Optional[Controller] = None,
    ):
        self._script_parser = script_parser or ScriptParser()
        self._board_parser = board_parser or BoardParser()
        self._board_printer = board_printer or BoardPrinter()
        self._game_engine = game_engine or GameEngine()
        self._controller = controller or Controller(self._game_engine)

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

        self._reset_for_new_run()

        print_board = PrintBoard(
            self._game_engine,
            self._board_printer,
            output_stream,
        )

        for line in command_lines:
            normalized = line.strip()
            if not normalized:
                continue

            if normalized == "print board":
                print_board.execute(board)
            elif normalized.startswith("click "):
                self._handle_click_command(normalized, board)
            elif normalized.startswith("wait "):
                self._handle_wait_command(normalized, board)

    def _reset_for_new_run(self) -> None:
        self._game_engine.reset()
        self._controller.reset()

    def _handle_wait_command(self, command_line: str, board: Board) -> None:
        parts = command_line.split()
        if len(parts) != 2:
            return
        try:
            milliseconds = int(parts[1])
        except ValueError:
            return
        self._game_engine.advance_time(board, milliseconds)

    def _handle_click_command(self, command_line: str, board: Board) -> None:
        parts = command_line.split()
        if len(parts) != 3:
            return
        try:
            x = int(parts[1])
            y = int(parts[2])
        except ValueError:
            return
        self._controller.handle_click(board, x, y)
