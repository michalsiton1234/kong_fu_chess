"""Computes legal destination cells for the selected piece (view helper)."""
from typing import List, Tuple

from kungfu_chess.engine.game_engine import GameEngine
from kungfu_chess.model.board import Board
from kungfu_chess.model.piece import Piece
from kungfu_chess.model.position import Position


class LegalMovesFinder:
    def find(
        self, board: Board, engine: GameEngine, piece: Piece
    ) -> List[Tuple[int, int]]:
        if engine.game_over:
            return []
        if engine.arbiter.is_piece_resting(piece):
            return []
        if engine.arbiter.is_piece_moving(piece.cell):
            return []
        if engine.arbiter.is_piece_airborne(piece):
            return []

        targets: List[Tuple[int, int]] = []
        source = piece.cell
        for row in range(board.height):
            for col in range(board.width):
                destination = Position(row, col)
                if not engine.validate_move(board, piece, source, destination):
                    continue
                if engine.arbiter.has_destination_conflict(destination):
                    continue
                targets.append((row, col))
        return targets
