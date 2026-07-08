import pytest

from kfc.board_validator import BoardValidator
from kfc.exceptions import RowWidthMismatchError, UnknownTokenError
from kfc.piece_registry import PieceRegistry


def make_validator():
    return BoardValidator(PieceRegistry())


def test_valid_board_passes_without_raising():
    make_validator().validate([["wR", "."], [".", "bK"]])


def test_empty_board_passes_without_raising():
    make_validator().validate([])


def test_unknown_token_raises_unknown_token_error():
    with pytest.raises(UnknownTokenError) as exc_info:
        make_validator().validate([["wX", "."]])
    assert exc_info.value.error_code == "ERROR UNKNOWN_TOKEN"


def test_row_width_mismatch_raises():
    with pytest.raises(RowWidthMismatchError) as exc_info:
        make_validator().validate([["wR", "."], ["."]])
    assert exc_info.value.error_code == "ERROR ROW_WIDTH_MISMATCH"


def test_token_check_happens_before_width_check():
    # A row-width problem exists too, but the unknown token must be reported first,
    # matching the original program's checking order.
    with pytest.raises(UnknownTokenError):
        make_validator().validate([["wX", "."], ["."]])
