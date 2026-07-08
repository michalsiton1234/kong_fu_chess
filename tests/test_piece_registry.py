from kfc.piece_registry import PieceRegistry


def test_empty_square_token_is_valid():
    registry = PieceRegistry()
    assert registry.is_valid_token(".") is True
    assert registry.parse_token(".") is None


def test_canonical_token_is_valid_and_parses_color_and_type():
    registry = PieceRegistry()
    assert registry.is_valid_token("wK") is True
    piece = registry.parse_token("wK")
    assert piece.color == "w"
    assert piece.piece_type == "K"
    assert piece.original_token == "wK"
    assert piece.display_token() == "wK"


def test_alternate_case_convention_token_is_valid():
    registry = PieceRegistry()
    assert registry.is_valid_token("Bp") is True
    piece = registry.parse_token("Bp")
    assert piece.color == "b"
    assert piece.piece_type == "P"


def test_unknown_token_is_invalid():
    registry = PieceRegistry()
    assert registry.is_valid_token("wX") is False
    assert registry.parse_token("wX") is None


def test_all_valid_tokens_includes_empty_square_and_expected_count():
    registry = PieceRegistry()
    tokens = registry.all_valid_tokens()
    assert "." in tokens
    # 2 colors * 6 piece types * 2 case-conventions + empty square
    assert len(tokens) == 2 * 6 * 2 + 1


def test_register_adds_new_piece_type():
    registry = PieceRegistry(colors=("w",), piece_types=("K",))
    assert registry.is_valid_token("wQ") is False
    registry.register("w", "Q")
    assert registry.is_valid_token("wQ") is True


def test_token_id_is_stable_and_none_for_unknown():
    registry = PieceRegistry()
    first_id = registry.token_id("w", "K")
    second_id = registry.token_id("w", "K")
    assert first_id is not None
    assert first_id == second_id
    assert registry.token_id("z", "Z") is None
