"""
InputParser: turns the raw input text into (board rows, recognized commands).

Splitting board-section-detection and command-recognition into two separate
classes would have separated two steps of the *same* responsibility -
"understand what the user's input text means" - into two files that always
have to be used together and never vary independently. Here they're kept as
one class with two small private helpers, which is a better fit for the
project's own guidance against unnecessary abstraction.

Recognized commands are still driven entirely by data (`KNOWN_COMMANDS`), so
adding a future command is a one-line change here and nowhere else.
"""
from typing import List, Set, Tuple

BOARD_SECTION_MARKER = "board:"
COMMANDS_SECTION_MARKER = "commands:"

KNOWN_COMMANDS = {
    "print board": "print_board",
}


class InputParser:
    def parse(self, raw_text: str) -> Tuple[List[List[str]], Set[str]]:
        board_rows, command_lines = self._split_sections(raw_text)
        commands = self._recognize_commands(command_lines)
        return board_rows, commands

    def _split_sections(self, raw_text: str) -> Tuple[List[List[str]], List[str]]:
        board_rows: List[List[str]] = []
        command_lines: List[str] = []
        in_board_section = False

        for line in self._non_empty_lines(raw_text):
            lowered_line = line.lower()

            if BOARD_SECTION_MARKER in lowered_line:
                in_board_section = True
                continue
            if COMMANDS_SECTION_MARKER in lowered_line:
                in_board_section = False
                continue

            if in_board_section:
                board_rows.append(line.split())
            else:
                command_lines.append(lowered_line)

        return board_rows, command_lines

    @staticmethod
    def _recognize_commands(command_lines: List[str]) -> Set[str]:
        recognized: Set[str] = set()
        for line in command_lines:
            for phrase, command_id in KNOWN_COMMANDS.items():
                if phrase in line:
                    recognized.add(command_id)
        return recognized

    @staticmethod
    def _non_empty_lines(raw_text: str) -> List[str]:
        return [line.strip() for line in raw_text.strip().split("\n") if line.strip()]
