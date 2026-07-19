from typing import Optional, Tuple

from kungfu_chess.engine.game_engine import GameEngine
from kungfu_chess.engine.motion import Motion
from kungfu_chess.engine.rest import LONG_REST_MS, SHORT_REST_MS
from kungfu_chess.model.board import Board
from kungfu_chess.model.piece import KNIGHT, Piece
from kungfu_chess.model.position import Position

from kungfu_chess.graphics.bridge.legal_moves_finder import LegalMovesFinder
from kungfu_chess.graphics.bridge.match_recorder import MatchRecorder
from kungfu_chess.graphics.view.board_layout import interpolate_pixel, to_pixel
from kungfu_chess.graphics.view.game_snapshot import GameSnapshot, PieceView


class SnapshotBuilder:
    def build(
        self,
        board: Board,
        engine: GameEngine,
        *,
        selected_piece: Optional[Piece] = None,
        hover_cell: Optional[Tuple[int, int]] = None,
        reject_cell: Optional[Tuple[int, int]] = None,
        match_recorder: Optional[MatchRecorder] = None,
    ) -> GameSnapshot:
        piece_views = []
        for row in range(board.height):
            for col in range(board.width):
                piece = board.piece_at(Position(row, col))
                if piece is None:
                    continue
                pixel_x, pixel_y = self._pixel_for_piece(engine, piece)
                visual_state, animation_time_ms = self._visual_state(engine, piece)
                piece_views.append(
                    PieceView(
                        piece_id=piece.id,
                        color=piece.color,
                        kind=piece.kind,
                        row=piece.cell.row,
                        col=piece.cell.col,
                        pixel_x=pixel_x,
                        pixel_y=pixel_y,
                        visual_state=visual_state,
                        animation_time_ms=animation_time_ms,
                    )
                )

        selected_row = None
        selected_col = None
        if selected_piece is not None:
            selected_row = selected_piece.cell.row
            selected_col = selected_piece.cell.col

        hover_row = hover_col = None
        if hover_cell is not None:
            hover_row, hover_col = hover_cell

        reject_row = reject_col = None
        if reject_cell is not None:
            reject_row, reject_col = reject_cell

        selected_label = None
        if selected_piece is not None:
            selected_label = (
                f"Selected: ({selected_piece.cell.row}, {selected_piece.cell.col})"
            )

        score_white = 0
        score_black = 0
        white_moves = []
        black_moves = []
        if match_recorder is not None:
            score_white = match_recorder.score_white
            score_black = match_recorder.score_black
            white_moves = list(match_recorder.white_moves)
            black_moves = list(match_recorder.black_moves)

        legal_targets = []
        if selected_piece is not None:
            legal_targets = LegalMovesFinder().find(
                board, engine, selected_piece
            )

        return GameSnapshot(
            board_width=board.width,
            board_height=board.height,
            pieces=piece_views,
            selected_row=selected_row,
            selected_col=selected_col,
            hover_row=hover_row,
            hover_col=hover_col,
            reject_row=reject_row,
            reject_col=reject_col,
            legal_targets=legal_targets,
            game_over=engine.game_over,
            score_white=score_white,
            score_black=score_black,
            white_moves=white_moves,
            black_moves=black_moves,
            selected_label=selected_label,
        )

    def _visual_state(
        self, engine: GameEngine, piece: Piece
    ) -> Tuple[str, int]:
        current_time = engine.arbiter.current_time

        if engine.arbiter.is_piece_airborne(piece):
            jump = self._find_jump(engine, piece)
            if jump is not None:
                return "jump", current_time - jump.start_time
            return "jump", 0

        motion = self._find_motion(engine, piece)
        if motion is not None:
            travel_ms = self._travel_time_ms(
                piece, motion.source, motion.destination
            )
            start_time = motion.arrival_time - travel_ms
            return "move", current_time - start_time

        if engine.arbiter.is_piece_resting(piece):
            rest_until = engine.arbiter._rest_until_by_piece_id.get(piece.id)
            if rest_until is not None:
                remaining = rest_until - current_time
                rest_kind = (
                    "long_rest"
                    if remaining > (SHORT_REST_MS + LONG_REST_MS) // 2
                    else "short_rest"
                )
                rest_start = rest_until - (
                    LONG_REST_MS if rest_kind == "long_rest" else SHORT_REST_MS
                )
                return rest_kind, current_time - rest_start

        return "idle", current_time

    def _pixel_for_piece(self, engine: GameEngine, piece: Piece) -> Tuple[int, int]:
        motion = self._find_motion(engine, piece)
        if motion is None:
            return to_pixel(piece.cell.row, piece.cell.col)

        travel_ms = self._travel_time_ms(
            piece, motion.source, motion.destination
        )
        start_time = motion.arrival_time - travel_ms
        current_time = engine.arbiter.current_time
        if travel_ms <= 0:
            progress = 1.0
        else:
            progress = (current_time - start_time) / travel_ms

        return interpolate_pixel(
            motion.source.row,
            motion.source.col,
            motion.destination.row,
            motion.destination.col,
            progress,
        )

    @staticmethod
    def _find_motion(engine: GameEngine, piece: Piece) -> Optional[Motion]:
        for motion in engine.arbiter._pending_motions:
            if motion.piece is piece:
                return motion
        return None

    @staticmethod
    def _find_jump(engine: GameEngine, piece: Piece):
        for jump in engine.arbiter._pending_jumps:
            if jump.piece is piece:
                return jump
        return None

    @staticmethod
    def _travel_time_ms(piece: Piece, source: Position, destination: Position) -> int:
        delta_row = abs(destination.row - source.row)
        delta_col = abs(destination.col - source.col)
        distance = max(delta_row, delta_col)
        if piece.kind == KNIGHT:
            distance = 1
        return distance * 1000
