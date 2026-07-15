from kungfu_chess.io.board_mapper import BoardMapper
from kungfu_chess.io.board_parser import BoardParser


class TestBoardMapper:
    def setup_method(self):
        self._mapper = BoardMapper()
        self._board = BoardParser().parse("wR . .\n. . .\n. . .")

    def test_maps_pixel_coordinates_to_position(self):
        pos = self._mapper.to_position(self._board, 50, 50)
        assert pos.row == 0 and pos.col == 0

    def test_returns_none_for_negative_coordinates(self):
        assert self._mapper.to_position(self._board, -1, 50) is None
        assert self._mapper.to_position(self._board, 50, -1) is None

    def test_returns_none_for_out_of_bounds_coordinates(self):
        assert self._mapper.to_position(self._board, 999, 999) is None
