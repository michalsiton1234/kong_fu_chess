
# """
# TextTestRunner drives a full script (board text + commands) end-to-end
# without any GUI (architecture Rule 2 — Textual I/O Simulation for Testing).

# In Iteration 2, commands are executed sequentially in the order they appear.
# Supported commands:
#   - click x y: maps pixels to cells, manages piece selection and movement requests.
#   - wait ms: advances game clock (stubbed for now).
#   - print board: renders the settled board state.
# """
# from typing import Dict, Optional, List, TextIO

# from ..io.board_parser import BoardParser
# from ..io.board_printer import BoardPrinter
# from ..io.board_mapper import BoardMapper
# from ..io.exceptions import BoardTextError
# from ..model.board import Board
# from ..model.position import Position
# from ..model.piece import Piece
# from .script_parser import ScriptParser


# class TextTestRunner:
#     def __init__(
#         self,
#         script_parser: Optional[ScriptParser] = None,
#         board_parser: Optional[BoardParser] = None,
#         board_printer: Optional[BoardPrinter] = None,
#         board_mapper: Optional[BoardMapper] = None,
#     ):
#         self._script_parser = script_parser or ScriptParser()
#         self._board_parser = board_parser or BoardParser()
#         self._board_printer = board_printer or BoardPrinter()
#         self._board_mapper = board_mapper or BoardMapper()
        
#         # Iteration 2 state: Track the currently selected piece
#         self._selected_piece: Optional[Piece] = None

#     def run(self, input_stream: TextIO, output_stream: TextIO) -> None:
#         raw_text = input_stream.read().strip()
#         if not raw_text:
#             return

#         board_text, command_lines = self._script_parser.parse(raw_text)
#         if not board_text:
#             return

#         try:
#             board = self._board_parser.parse(board_text)
#         except BoardTextError as error:
#             print(error.error_code, file=output_stream)
#             return

#         # Reset selection state for each run
#         self._selected_piece = None

#         # Execute commands sequentially
#         for line in command_lines:
#             normalized = line.strip()
#             if not normalized:
#                 continue

#             if normalized == "print board":
#                 print(self._board_printer.render(board), file=output_stream)
                
#             elif normalized.startswith("click "):
#                 self._handle_click_command(normalized, board)
                
#             elif normalized.startswith("wait "):
#                 # Wait command parses the milliseconds but does not affect the board state in this iteration
#                 pass

#     def _handle_click_command(self, command_line: str, board: Board) -> None:
#         parts = command_line.split()
#         if len(parts) != 3:
#             return  # Malformed command ignored
            
#         try:
#             x = int(parts[1])
#             y = int(parts[2])
#         except ValueError:
#             return  # Invalid numbers ignored

#         pos = self._board_mapper.to_position(board, x, y)
#         if pos is None:
#             return  # Clicking outside the board is ignored

#         clicked_piece = board.piece_at(pos)

#         if self._selected_piece is None:
#             # No piece selected currently
#             if clicked_piece is not None:
#                 self._selected_piece = clicked_piece
#         else:
#             # A piece is already selected
#             if clicked_piece is not None and clicked_piece.color == self._selected_piece.color:
#                 # Clicking another friendly piece replaces the selection
#                 self._selected_piece = clicked_piece
#             else:
#                 # Clicking an empty cell or an enemy piece sends a move request
#                 source_pos = self._selected_piece.cell
#                 board.move_piece(source_pos, pos)
#                 self._selected_piece = None  # Clear selection after move request
"""
TextTestRunner drives a full script (board text + commands) end-to-end
without any GUI (architecture Rule 2 — Textual I/O Simulation for Testing).

In Iteration 3, basic chess movement rules are enforced before a move is applied:
  - King: maximum 1 cell in any direction.
  - Rook: straight lines only (row or col change, not both).
  - Bishop: diagonals only (abs row delta == abs col delta).
  - Queen: combined Rook and Bishop patterns.
  - Knight: L-shapes (2x1 or 1x2).
"""
from typing import Dict, Optional, List, TextIO

from ..io.board_parser import BoardParser
from ..io.board_printer import BoardPrinter
from ..io.board_mapper import BoardMapper
from ..io.exceptions import BoardTextError
from ..model.board import Board
from ..model.position import Position
from ..model.piece import Piece
from .script_parser import ScriptParser


class TextTestRunner:
    def __init__(
        self,
        script_parser: Optional[ScriptParser] = None,
        board_parser: Optional[BoardParser] = None,
        board_printer: Optional[BoardPrinter] = None,
        board_mapper: Optional[BoardMapper] = None,
    ):
        self._script_parser = script_parser or ScriptParser()
        self._board_parser = board_parser or BoardParser()
        self._board_printer = board_printer or BoardPrinter()
        self._board_mapper = board_mapper or BoardMapper()
        
        # Track the currently selected piece
        self._selected_piece: Optional[Piece] = None

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

        # Reset selection state for each run
        self._selected_piece = None

        # Execute commands sequentially
        for line in command_lines:
            normalized = line.strip()
            if not normalized:
                continue

            if normalized == "print board":
                print(self._board_printer.render(board), file=output_stream)
                
            elif normalized.startswith("click "):
                self._handle_click_command(normalized, board)
                
            elif normalized.startswith("wait "):
                # Wait command parses the milliseconds but does not affect the board state
                pass

    def _is_legal_move(self, piece: Piece, source: Position, dest: Position) -> bool:
        """
        Validates basic chess geometric movement patterns for Iteration 3.
        Returns True if the move is legal for the piece type, otherwise False.
        """
        if source == dest:
            return False

        delta_row = abs(dest.row - source.row)
        delta_col = abs(dest.col - source.col)

        if piece.kind == "king":
            return delta_row <= 1 and delta_col <= 1
            
        elif piece.kind == "rook":
            return delta_row == 0 or delta_col == 0
            
        elif piece.kind == "bishop":
            return delta_row == delta_col
            
        elif piece.kind == "queen":
            return (delta_row == 0 or delta_col == 0) or (delta_row == delta_col)
            
        elif piece.kind == "knight":
            return (delta_row == 2 and delta_col == 1) or (delta_row == 1 and delta_col == 2)
            
        elif piece.kind == "pawn":
            # Pawns are not explicitly limited by constraints in this iteration
            return True
            
        return False

    def _handle_click_command(self, command_line: str, board: Board) -> None:
        parts = command_line.split()
        if len(parts) != 3:
            return  # Malformed command ignored
            
        try:
            x = int(parts[1])
            y = int(parts[2])
        except ValueError:
            return  # Invalid numbers ignored

        pos = self._board_mapper.to_position(board, x, y)
        if pos is None:
            return  # Clicking outside the board is ignored

        clicked_piece = board.piece_at(pos)

        if self._selected_piece is None:
            # No piece selected currently
            if clicked_piece is not None:
                self._selected_piece = clicked_piece
        else:
            # A piece is already selected
            if clicked_piece is not None and clicked_piece.color == self._selected_piece.color:
                # Clicking another friendly piece replaces the selection
                self._selected_piece = clicked_piece
            else:
                # Clicking an empty cell or an enemy piece sends a move request
                source_pos = self._selected_piece.cell
                
                # Check geometric legality according to Iteration 3 specs
                if self._is_legal_move(self._selected_piece, source_pos, pos):
                    board.move_piece(source_pos, pos)
                    
                self._selected_piece = None  # Clear selection after a move attempt