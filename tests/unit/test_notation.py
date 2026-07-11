import pytest

from kungfu_chess.io.exceptions import UnknownTokenError
from kungfu_chess.io.notation import parse_token, token_for
from kungfu_chess.model.piece import BLACK, KING, ROOK, WHITE


def test_token_for_white_king():
    assert token_for(WHITE, KING) == "wK"


def test_token_for_black_rook():
    assert token_for(BLACK, ROOK) == "bR"


def test_parse_token_round_trips_token_for():
    assert parse_token(token_for(WHITE, KING)) == (WHITE, KING)


def test_parse_empty_token_returns_none():
    assert parse_token(".") is None


def test_parse_unknown_token_raises():
    with pytest.raises(UnknownTokenError):
        parse_token("xZ")
