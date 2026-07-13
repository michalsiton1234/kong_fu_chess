# import io

# from kungfu_chess.texttests.script_runner import TextTestRunner

# VALID_SCRIPT = (
#     "Board:\n"
#     "wK . . bK\n"
#     ". . . .\n"
#     "wR . . bR\n"
#     "Commands:\n"
#     "print board\n"
# )


# def run(text: str) -> str:
#     output = io.StringIO()
#     TextTestRunner().run(io.StringIO(text), output)
#     return output.getvalue()


# def test_prints_board_on_valid_script_with_print_command():
#     assert run(VALID_SCRIPT).strip() == "wK . . bK\n. . . .\nwR . . bR"


# def test_no_output_when_print_command_absent():
#     text = "Board:\nwK .\n. .\nCommands:\n"
#     assert run(text) == ""


# def test_unknown_token_error_is_printed():
#     text = "Board:\nxZ .\n. .\nCommands:\nprint board"
#     assert run(text).strip() == "ERROR UNKNOWN_TOKEN"


# def test_row_width_mismatch_error_is_printed():
#     text = "Board:\nwK . .\n. .\nCommands:\nprint board"
#     assert run(text).strip() == "ERROR ROW_WIDTH_MISMATCH"


# def test_empty_input_produces_no_output():
#     assert run("") == ""


# def test_missing_board_section_produces_no_output():
#     assert run("Commands:\nprint board") == ""


# def test_default_dependencies_are_constructed_when_none_provided():
#     runner = TextTestRunner(script_parser=None, board_parser=None, print_board=None)
#     output = io.StringIO()
#     runner.run(io.StringIO(VALID_SCRIPT), output)
#     assert output.getvalue() != ""
import io
import pytest
from kungfu_chess.texttests.script_runner import TextTestRunner

VALID_SCRIPT = (
    "Board:\n"
    "wK . . bK\n"
    ". . . .\n"
    "wR . . bR\n"
    "Commands:\n"
    "print board\n"
)


def run(text: str) -> str:
    output = io.StringIO()
    TextTestRunner().run(io.StringIO(text), output)
    return output.getvalue()


def test_prints_board_on_valid_script_with_print_command():
    assert run(VALID_SCRIPT).strip() == "wK . . bK\n. . . .\nwR . . bR"


def test_no_output_when_print_command_absent():
    text = "Board:\nwK .\n. .\nCommands:\n"
    assert run(text) == ""


def test_unknown_token_error_is_printed():
    text = "Board:\nxZ .\n. .\nCommands:\nprint board"
    assert run(text).strip() == "ERROR UNKNOWN_TOKEN"


def test_row_width_mismatch_error_is_printed():
    text = "Board:\nwK . .\n. .\nCommands:\nprint board"
    assert run(text).strip() == "ERROR ROW_WIDTH_MISMATCH"


def test_empty_input_produces_no_output():
    assert run("") == ""


def test_missing_board_section_produces_no_output():
    assert run("Commands:\nprint board") == ""


def test_default_dependencies_are_constructed_when_none_provided():
    # המרה לפרמטרים העדכניים של איטרציה 2 כדי למנוע TypeError
    runner = TextTestRunner(
        script_parser=None, 
        board_parser=None, 
        board_printer=None, 
        board_mapper=None
    )
    output = io.StringIO()
    runner.run(io.StringIO(VALID_SCRIPT), output)
    assert output.getvalue() != ""


# ====================================================================
# טסטים חדשים עבור איטרציה 2 - בדיקת פקודות click ו-wait וכיסוי קוד מלא
# ====================================================================

def test_click_moves_piece_and_updates_board():
    """
    בודק שלחיצה על צריח לבן (שורה 2, עמודה 0 -> פיקסלים x=50, y=250)
    ולאחר מכן לחיצה על משבצת ריקה מימין (שורה 2, עמודה 1 -> פיקסלים x=150, y=250)
    מזיזה את הצריח בהצלחה.
    """
    script = (
        "Board:\n"
        "wK . . bK\n"
        ". . . .\n"
        "wR . . bR\n"
        "Commands:\n"
        "click 50 250\n"    # בוחר את wR ב-(2, 0)
        "click 150 250\n"   # מזיז ל-(2, 1)
        "print board\n"
    )
    expected = (
        "wK . . bK\n"
        ". . . .\n"
        ". wR . bR"
    )
    assert run(script).strip() == expected


def test_click_friendly_piece_changes_selection():
    """
    בודק שלחיצה על כלי חברותי אחר מחליפה את הבחירה במקום להזיז.
    נלחץ על המלך wK (פיקסלים 50, 50), אז נחליף לצריח wR (פיקסלים 50, 250),
    ואז נזיז את הצריח ל- (2, 1). המלך צריך להישאר במקומו.
    """
    script = (
        "Board:\n"
        "wK . . bK\n"
        ". . . .\n"
        "wR . . bR\n"
        "Commands:\n"
        "click 50 50\n"     # בוחר את wK
        "click 50 250\n"    # מחליף בחירה ל-wR (כי הוא מאותו צבע)
        "click 150 250\n"   # מזיז את wR ל-(2, 1)
        "print board\n"
    )
    expected = (
        "wK . . bK\n"
        ". . . .\n"
        ". wR . bR"
    )
    assert run(script).strip() == expected


def test_click_outside_board_or_empty_without_selection_ignored():
    """
    בודק שלחיצות לא תקינות (מחוץ ללוח או על משבצת ריקה כשאין בחירה) נתעלמות.
    כן בודק שפקודת wait מתקבלת ללא שגיאות.
    """
    script = (
        "Board:\n"
        "wK . . bK\n"
        "Commands:\n"
        "click -50 50\n"    # מחוץ לגבולות - מתעלם
        "click 999 50\n"    # מחוץ לגבולות - מתעלם
        "click 150 50\n"    # לחיצה על ריק ללא בחירה מוקדמת - מתעלם
        "wait 500\n"        # פקודת המתנה - מעבירה זמן ללא שגיאה
        "print board\n"
    )
    expected = "wK . . bK"
    assert run(script).strip() == expected

def test_king_illegal_move_ignored():
    """מלך מנסה לזוז 2 משבצות ימינה - המהלך לא חוקי וצריך להתעלם ממנו"""
    script = (
        "Board:\n"
        "wK . . .\n"
        "Commands:\n"
        "click 50 50\n"   # בחירת המלך ב-(0,0)
        "click 250 50\n"  # ניסיון תנועה ל-(0,2) - לא חוקי!
        "print board\n"
    )
    # המלך חייב להישאר במיקומו המקורי
    assert run(script).strip() == "wK . . ."


def test_rook_diagonal_move_ignored():
    """צריח מנסה לזוז באלכסון - המהלך לא חוקי וצריך להתעלם ממנו"""
    script = (
        "Board:\n"
        "wR . . .\n"
        ". . . .\n"
        "Commands:\n"
        "click 50 50\n"   # בחירת הצריח ב-(0,0)
        "click 150 150\n" # ניסיון תנועה אלכסונית ל-(1,1) - לא חוקי!
        "print board\n"
    )
    assert run(script).strip() == "wR . . .\n. . . ."


def test_knight_legal_l_shape_move():
    """פרש מצעד מהלך חוקי בצורת L וזז בהצלחה"""
    script = (
        "Board:\n"
        "wN . . .\n"
        ". . . .\n"
        ". . . .\n"
        "Commands:\n"
        "click 50 50\n"   # בחירת הפרש ב-(0,0)
        "click 150 250\n" # תנועה חוקית ל-(2,1)
        "print board\n"
    )
    expected = (
        ". . . .\n"
        ". . . .\n"
        ". wN . ."
    )
    assert run(script).strip() == expected
def test_bishop_legal_diagonal_move():
    """בדיקה של מהלך חוקי עבור רץ באלכסון"""
    script = (
        "Board:\n"
        "wB . . .\n"
        ". . . .\n"
        "Commands:\n"
        "click 50 50\n"   # בחירת רץ ב-(0,0)
        "click 150 150\n" # תנועה חוקית ל-(1,1)
        "print board\n"
    )
    assert ". wB . ." in run(script)

def test_queen_legal_straight_move():
    """בדיקה של מהלך חוקי עבור מלכה בקו ישר"""
    script = (
        "Board:\n"
        "wQ . . .\n"
        ". . . .\n"
        "Commands:\n"
        "click 50 50\n"   # בחירת מלכה ב-(0,0)
        "click 50 150\n"  # תנועה חוקית למטה ל-(1,0)
        "print board\n"
    )
    assert ".\nwQ" in run(script)

def test_malformed_click_command_ignored():
    """בדיקה שפקודת קליק עם פורמט שגוי לא שוברת את התוכנית ומתעלמים ממנה"""
    script = (
        "Board:\n"
        "wK . . .\n"
        "Commands:\n"
        "click abc 50\n"  # קואורדינטה לא מספרית - חסר טקסט
        "click 50\n"      # חסר פרמטר Y
        "print board\n"
    )
    assert run(script).strip() == "wK . . ."