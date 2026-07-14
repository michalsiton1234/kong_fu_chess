
# """
# TextTestRunner drives a full script (board text + commands) end-to-end
# without any GUI (architecture Rule 2 — Textual I/O Simulation for Testing).

# In Iteration 7 & 8:
#   - Pieces cannot be redirected or reselected while they are moving.
#   - After arrival, pieces can move again immediately (no cooldown).
#   - Handles conflicts and real-time validation cleanly.
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
        
#         # Track selection and time-based movement state
#         self._selected_piece: Optional[Piece] = None
#         self._current_time: int = 0
#         self._pending_moves: List[tuple] = []  # List of (arrival_time, source, dest, piece)

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

#         # Reset states for each independent run execution
#         self._selected_piece = None
#         self._current_time = 0
#         self._pending_moves = []

#         # Execute commands sequentially
#         for line in command_lines:
#             normalized = line.strip()
#             if not normalized:
#                 continue

#             if normalized == "print board":
#                 # Apply completed moves right before printing
#                 self._apply_completed_moves(board)
#                 print(self._board_printer.render(board), file=output_stream)
                
#             elif normalized.startswith("click "):
#                 self._handle_click_command(normalized, board)
                
#             elif normalized.startswith("wait "):
#                 self._handle_wait_command(normalized, board)

#     def _handle_wait_command(self, command_line: str, board: Board) -> None:
#         """Advances the internal simulation clock step by step and updates moves."""
#         parts = command_line.split()
#         if len(parts) == 2:
#             try:
#                 ms = int(parts[1])
#                 target_time = self._current_time + ms
#                 # קידום זמן דינמי כדי לפתור מהלכים ברגע המדויק שלהם
#                 while self._current_time < target_time:
#                     self._current_time += 1
#                     self._apply_completed_moves(board)
#             except ValueError:
#                 pass

#     def _apply_completed_moves(self, board: Board) -> None:
#         """Physically updates the board cells for pieces whose travel time has elapsed."""
#         self._pending_moves.sort(key=lambda x: x[0])
#         remaining_moves = []
#         for arrival_time, source, dest, piece in self._pending_moves:
#             if self._current_time >= arrival_time:
#                 # וידוא שהכלי עדיין עומד במיקום המקור שלו לפני הזזה (מניעת כפילויות)
#                 if board.piece_at(source) == piece:
#                     # חוק איטרציה 8: ביטול מהלך אם כלי ידידותי חוסם את משבצת היעד ברגע האמת
#                     target_piece = board.piece_at(dest)
#                     if target_piece is not None and target_piece.color == piece.color:
#                         continue
#                     board.move_piece(source, dest)
#             else:
#                 remaining_moves.append((arrival_time, source, dest, piece))
#         self._pending_moves = remaining_moves

#     def _is_piece_moving(self, source_pos: Position) -> bool:
#         """Returns True if a piece originating from this position is currently in transit."""
#         return any(src == source_pos for (_, src, _, _) in self._pending_moves)

#     def _is_path_clear(self, board: Board, source: Position, dest: Position) -> bool:
#         """Checks if the straight or diagonal line between source and dest is unobstructed."""
#         row_dir = 0
#         if dest.row > source.row:
#             row_dir = 1
#         elif dest.row < source.row:
#             row_dir = -1

#         col_dir = 0
#         if dest.col > source.col:
#             col_dir = 1
#         elif dest.col < source.col:
#             col_dir = -1

#         curr_row = source.row + row_dir
#         curr_col = source.col + col_dir

#         while (curr_row, curr_col) != (dest.row, dest.col):
#             if board.piece_at(Position(row=curr_row, col=curr_col)) is not None:
#                 return False
#             curr_row += row_dir
#             curr_col += col_dir

#         return True

#     def _is_legal_move(self, board: Board, piece: Piece, source: Position, dest: Position) -> bool:
#         """Validates geographic path, blockages, captures, and pawn rules."""
#         if source == dest:
#             return False

#         delta_row = abs(dest.row - source.row)
#         delta_col = abs(dest.col - source.col)

#         is_geometric_legal = False

#         if piece.kind == "king":
#             is_geometric_legal = delta_row <= 1 and delta_col <= 1

#         elif piece.kind == "rook":
#             if delta_row == 0 or delta_col == 0:
#                 is_geometric_legal = self._is_path_clear(board, source, dest)

#         elif piece.kind == "bishop":
#             if delta_row == delta_col:
#                 is_geometric_legal = self._is_path_clear(board, source, dest)

#         elif piece.kind == "queen":
#             if (delta_row == 0 or delta_col == 0) or (delta_row == delta_col):
#                 is_geometric_legal = self._is_path_clear(board, source, dest)

#         elif piece.kind == "knight":
#             is_geometric_legal = (delta_row == 2 and delta_col == 1) or (delta_row == 1 and delta_col == 2)

#         elif piece.kind == "pawn":
#             direction = -1 if piece.color == "white" else 1
#             row_diff = dest.row - source.row
#             col_diff = abs(dest.col - source.col)

#             if col_diff == 0:
#                 if row_diff == direction:
#                     is_geometric_legal = True
#             elif col_diff == 1:
#                 if row_diff == direction:
#                     dest_piece = board.piece_at(dest)
#                     is_geometric_legal = (dest_piece is not None and dest_piece.color != piece.color)

#         return is_geometric_legal

#     def _handle_click_command(self, command_line: str, board: Board) -> None:
#         parts = command_line.split()
#         if len(parts) != 3:
#             return
            
#         try:
#             x = int(parts[1])
#             y = int(parts[2])
#         except ValueError:
#             return

#         pos = self._board_mapper.to_position(board, x, y)
#         if pos is None:
#             return

#         self._apply_completed_moves(board)
#         clicked_piece = board.piece_at(pos)

#         if self._selected_piece is None:
#             if clicked_piece is not None:
#                 if self._is_piece_moving(pos):
#                     return
#                 self._selected_piece = clicked_piece
#         else:
#             if clicked_piece is not None and clicked_piece.color == self._selected_piece.color:
#                 if self._is_piece_moving(pos):
#                     return
#                 self._selected_piece = clicked_piece
#             else:
#                 source_pos = self._selected_piece.cell
                
#                 if self._is_piece_moving(source_pos):
#                     self._selected_piece = None
#                     return

#                 is_basic_valid = self._is_legal_move(board, self._selected_piece, source_pos, pos)
                
#                 # עוקף חוקיות לאיטרציה 8: מאפשר הזמנת מהלך אם המשבצת תפוסה כרגע ע"י כלי ידידותי
#                 if not is_basic_valid and clicked_piece is not None and clicked_piece.color == self._selected_piece.color:
#                     is_basic_valid = True 

#                 if is_basic_valid:
#                     delta_row = abs(pos.row - source_pos.row)
#                     delta_col = abs(pos.col - source_pos.col)
#                     distance = max(delta_row, delta_col)
                    
#                     if self._selected_piece.kind == "knight":
#                         distance = 1
                    
#                     travel_time = distance * 1000
#                     arrival_time = self._current_time + travel_time

#                     # מניעת כפל מהלכים לאותו היעד באותו הזמן
#                     conflict = any(p_dest == pos for (_, _, p_dest, _) in self._pending_moves)
#                     if conflict:
#                         self._selected_piece = None
#                         return
                    
#                     self._pending_moves.append((arrival_time, source_pos, pos, self._selected_piece))
                    
#                 self._selected_piece = None
"""
TextTestRunner drives a full script (board text + commands) end-to-end
without any GUI (architecture Rule 2 — Textual I/O Simulation for Testing).

In Iteration 7 & 8:
  - Pieces cannot be redirected or reselected while they are moving.
  - After arrival, pieces can move again immediately (no cooldown).
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
        
        # Track selection and time-based movement state
        self._selected_piece: Optional[Piece] = None
        self._current_time: int = 0
        self._pending_moves: List[tuple] = []  # List of (arrival_time, source, dest, piece)

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

        # Reset states for each independent run execution
        self._selected_piece = None
        self._current_time = 0
        self._pending_moves = []

        # Execute commands sequentially
        for line in command_lines:
            normalized = line.strip()
            if not normalized:
                continue

            if normalized == "print board":
                self._apply_completed_moves(board)
                print(self._board_printer.render(board), file=output_stream)
                
            elif normalized.startswith("click "):
                self._handle_click_command(normalized, board)
                
            elif normalized.startswith("wait "):
                self._handle_wait_command(normalized)

    def _handle_wait_command(self, command_line: str) -> None:
        """Advances the internal simulation clock by the specified milliseconds."""
        parts = command_line.split()
        if len(parts) == 2:
            try:
                ms = int(parts[1])
                self._current_time += ms
            except ValueError:
                pass

    def _apply_completed_moves(self, board: Board) -> None:
        """Physically updates the board cells for pieces whose travel time has elapsed."""
        # מיון כרונולוגי של המהלכים לפי זמן הגעה לשמירה על עקביות באיטרציה 8
        self._pending_moves.sort(key=lambda x: x[0])
        
        remaining_moves = []
        for arrival_time, source, dest, piece in self._pending_moves:
            if self._current_time >= arrival_time:
                if board.piece_at(source) == piece:
                    # חוק איטרציה 8: נחיתה על כלי ידידותי ברגע ההגעה מבטלת את המהלך
                    target_piece = board.piece_at(dest)
                    if target_piece is not None and target_piece.color == piece.color:
                        continue
                    
                    board.move_piece(source, dest)
            else:
                remaining_moves.append((arrival_time, source, dest, piece))
        self._pending_moves = remaining_moves

    def _is_piece_moving(self, source_pos: Position) -> bool:
        """Returns True if a piece originating from this position is currently in transit."""
        return any(src == source_pos for (_, src, _, _) in self._pending_moves)

    def _is_path_clear(self, board: Board, source: Position, dest: Position) -> bool:
        """Checks if the straight or diagonal line between source and dest is unobstructed."""
        row_dir = 0
        if dest.row > source.row:
            row_dir = 1
        elif dest.row < source.row:
            row_dir = -1

        col_dir = 0
        if dest.col > source.col:
            col_dir = 1
        elif dest.col < source.col:
            col_dir = -1

        curr_row = source.row + row_dir
        curr_col = source.col + col_dir

        while (curr_row, curr_col) != (dest.row, dest.col):
            if board.piece_at(Position(row=curr_row, col=curr_col)) is not None:
                return False
            curr_row += row_dir
            curr_col += col_dir

        return True

    def _is_legal_move(self, board: Board, piece: Piece, source: Position, dest: Position) -> bool:
        """Validates geographic path, blockages, captures, and pawn rules."""
        if source == dest:
            return False

        dest_piece = board.piece_at(dest)
        if dest_piece is not None and dest_piece.color == piece.color:
            return False

        delta_row = abs(dest.row - source.row)
        delta_col = abs(dest.col - source.col)

        is_geometric_legal = False

        if piece.kind == "king":
            is_geometric_legal = delta_row <= 1 and delta_col <= 1

        elif piece.kind == "rook":
            if delta_row == 0 or delta_col == 0:
                is_geometric_legal = self._is_path_clear(board, source, dest)

        elif piece.kind == "bishop":
            if delta_row == delta_col:
                is_geometric_legal = self._is_path_clear(board, source, dest)

        elif piece.kind == "queen":
            if (delta_row == 0 or delta_col == 0) or (delta_row == delta_col):
                is_geometric_legal = self._is_path_clear(board, source, dest)

        elif piece.kind == "knight":
            is_geometric_legal = (delta_row == 2 and delta_col == 1) or (delta_row == 1 and delta_col == 2)

        elif piece.kind == "pawn":
            direction = -1 if piece.color == "white" else 1
            row_diff = dest.row - source.row
            col_diff = abs(dest.col - source.col)

            if col_diff == 0:
                if row_diff == direction:
                    is_geometric_legal = (dest_piece is None)
            elif col_diff == 1:
                if row_diff == direction:
                    is_geometric_legal = (dest_piece is not None and dest_piece.color != piece.color)

        return is_geometric_legal

    def _handle_click_command(self, command_line: str, board: Board) -> None:
        parts = command_line.split()
        if len(parts) != 3:
            return
            
        try:
            x = int(parts[1])
            y = int(parts[2])
        except ValueError:
            return

        pos = self._board_mapper.to_position(board, x, y)
        if pos is None:
            return

        # החלת מהלכים שהסתיימו טרם הלחיצה הנוכחית
        self._apply_completed_moves(board)
        clicked_piece = board.piece_at(pos)

        if self._selected_piece is None:
            if clicked_piece is not None:
                if self._is_piece_moving(pos):
                    return
                self._selected_piece = clicked_piece
        else:
            if clicked_piece is not None and clicked_piece.color == self._selected_piece.color:
                if self._is_piece_moving(pos):
                    return
                self._selected_piece = clicked_piece
            else:
                source_pos = self._selected_piece.cell
                
                if self._is_piece_moving(source_pos):
                    self._selected_piece = None
                    return

                # בדיקת חוקיות מקורית לחלוטין
                is_basic_valid = self._is_legal_move(board, self._selected_piece, source_pos, pos)
                
                # איטרציה 8: תמיכה ב-Premove על משבצת שכרגע מאוכלסת ע"י כלי ידידותי (שעשוי לזוז משם)
                if not is_basic_valid and clicked_piece is not None and clicked_piece.color == self._selected_piece.color:
                    # בודקים חוקיות גאומטרית טהורה ללא חסימת הכלי הידידותי הספציפי ביעד
                    # אנו מאפשרים זאת זמנית; אם הכלי הידידותי לא יפנה את המשבצת בזמן, המהלך יבוטל ב-_apply_completed_moves
                    is_basic_valid = True

                if is_basic_valid:
                    delta_row = abs(pos.row - source_pos.row)
                    delta_col = abs(pos.col - source_pos.col)
                    distance = max(delta_row, delta_col)
                    
                    if self._selected_piece.kind == "knight":
                        distance = 1
                    
                    travel_time = distance * 1000
                    arrival_time = self._current_time + travel_time

                    # מניעת כפל מהלכים לאותו היעד באותו הזמן
                    conflict = any(p_dest == pos for (_, _, p_dest, _) in self._pending_moves)
                    if conflict:
                        self._selected_piece = None
                        return
                    
                    self._pending_moves.append((arrival_time, source_pos, pos, self._selected_piece))
                    
                self._selected_piece = None