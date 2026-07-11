"""
ScriptParser splits a raw test-script into a board-text block and a list of
command lines, based on the "Board:" / "Commands:" section markers.

It only knows about *script structure* — it does not know board notation
(that's BoardParser's job) and it does not know what any given command
means (that's TextTestRunner's job). This split keeps each class to one
reason to change (SRP, Rule 1).
"""
from typing import List, Tuple

BOARD_MARKER = "board:"
COMMANDS_MARKER = "commands:"


class ScriptParser:
    def parse(self, raw_text: str) -> Tuple[str, List[str]]:
        board_lines: List[str] = []
        command_lines: List[str] = []
        section = None

        for line in self._non_empty_lines(raw_text):
            lowered_line = line.lower()

            if BOARD_MARKER in lowered_line:
                section = "board"
                continue
            if COMMANDS_MARKER in lowered_line:
                section = "commands"
                continue

            if section == "board":
                board_lines.append(line)
            elif section == "commands":
                command_lines.append(lowered_line)

        return "\n".join(board_lines), command_lines

    @staticmethod
    def _non_empty_lines(raw_text: str) -> List[str]:
        return [line.strip() for line in raw_text.strip().split("\n") if line.strip()]
