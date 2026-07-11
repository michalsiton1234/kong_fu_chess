"""BoardPrinter prints a Board's logical occupancy back to text, using the
same notation table as BoardParser (notation.py) so parsing and printing
can never drift apart (DRY)."""
from ..model.board import Board
from ..model.position import Position
from .notation import EMPTY_TOKEN, token_for


class BoardPrinter:
    def render(self, board: Board) -> str:
        lines = []
        for row in range(board.height):
            cells = []
            for col in range(board.width):
                piece = board.piece_at(Position(row, col))
                cells.append(token_for(piece.color, piece.kind) if piece else EMPTY_TOKEN)
            lines.append(" ".join(cells))
        return "\n".join(lines)
