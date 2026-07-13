
# import io
# import pytest
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
#     # המרה לפרמטרים העדכניים של איטרציה 2 כדי למנוע TypeError
#     runner = TextTestRunner(
#         script_parser=None, 
#         board_parser=None, 
#         board_printer=None, 
#         board_mapper=None
#     )
#     output = io.StringIO()
#     runner.run(io.StringIO(VALID_SCRIPT), output)
#     assert output.getvalue() != ""


# # ====================================================================
# # טסטים חדשים עבור איטרציה 2 - בדיקת פקודות click ו-wait וכיסוי קוד מלא
# # ====================================================================

# def test_click_moves_piece_and_updates_board():
#     """
#     בודק שלחיצה על צריח לבן (שורה 2, עמודה 0 -> פיקסלים x=50, y=250)
#     ולאחר מכן לחיצה על משבצת ריקה מימין (שורה 2, עמודה 1 -> פיקסלים x=150, y=250)
#     מזיזה את הצריח בהצלחה.
#     """
#     script = (
#         "Board:\n"
#         "wK . . bK\n"
#         ". . . .\n"
#         "wR . . bR\n"
#         "Commands:\n"
#         "click 50 250\n"    # בוחר את wR ב-(2, 0)
#         "click 150 250\n"   # מזיז ל-(2, 1)
#         "print board\n"
#     )
#     expected = (
#         "wK . . bK\n"
#         ". . . .\n"
#         ". wR . bR"
#     )
#     assert run(script).strip() == expected


# def test_click_friendly_piece_changes_selection():
#     """
#     בודק שלחיצה על כלי חברותי אחר מחליפה את הבחירה במקום להזיז.
#     נלחץ על המלך wK (פיקסלים 50, 50), אז נחליף לצריח wR (פיקסלים 50, 250),
#     ואז נזיז את הצריח ל- (2, 1). המלך צריך להישאר במקומו.
#     """
#     script = (
#         "Board:\n"
#         "wK . . bK\n"
#         ". . . .\n"
#         "wR . . bR\n"
#         "Commands:\n"
#         "click 50 50\n"     # בוחר את wK
#         "click 50 250\n"    # מחליף בחירה ל-wR (כי הוא מאותו צבע)
#         "click 150 250\n"   # מזיז את wR ל-(2, 1)
#         "print board\n"
#     )
#     expected = (
#         "wK . . bK\n"
#         ". . . .\n"
#         ". wR . bR"
#     )
#     assert run(script).strip() == expected


# def test_click_outside_board_or_empty_without_selection_ignored():
#     """
#     בודק שלחיצות לא תקינות (מחוץ ללוח או על משבצת ריקה כשאין בחירה) נתעלמות.
#     כן בודק שפקודת wait מתקבלת ללא שגיאות.
#     """
#     script = (
#         "Board:\n"
#         "wK . . bK\n"
#         "Commands:\n"
#         "click -50 50\n"    # מחוץ לגבולות - מתעלם
#         "click 999 50\n"    # מחוץ לגבולות - מתעלם
#         "click 150 50\n"    # לחיצה על ריק ללא בחירה מוקדמת - מתעלם
#         "wait 500\n"        # פקודת המתנה - מעבירה זמן ללא שגיאה
#         "print board\n"
#     )
#     expected = "wK . . bK"
#     assert run(script).strip() == expected

# def test_king_illegal_move_ignored():
#     """מלך מנסה לזוז 2 משבצות ימינה - המהלך לא חוקי וצריך להתעלם ממנו"""
#     script = (
#         "Board:\n"
#         "wK . . .\n"
#         "Commands:\n"
#         "click 50 50\n"   # בחירת המלך ב-(0,0)
#         "click 250 50\n"  # ניסיון תנועה ל-(0,2) - לא חוקי!
#         "print board\n"
#     )
#     # המלך חייב להישאר במיקומו המקורי
#     assert run(script).strip() == "wK . . ."


# def test_rook_diagonal_move_ignored():
#     """צריח מנסה לזוז באלכסון - המהלך לא חוקי וצריך להתעלם ממנו"""
#     script = (
#         "Board:\n"
#         "wR . . .\n"
#         ". . . .\n"
#         "Commands:\n"
#         "click 50 50\n"   # בחירת הצריח ב-(0,0)
#         "click 150 150\n" # ניסיון תנועה אלכסונית ל-(1,1) - לא חוקי!
#         "print board\n"
#     )
#     assert run(script).strip() == "wR . . .\n. . . ."


# def test_knight_legal_l_shape_move():
#     """פרש מצעד מהלך חוקי בצורת L וזז בהצלחה"""
#     script = (
#         "Board:\n"
#         "wN . . .\n"
#         ". . . .\n"
#         ". . . .\n"
#         "Commands:\n"
#         "click 50 50\n"   # בחירת הפרש ב-(0,0)
#         "click 150 250\n" # תנועה חוקית ל-(2,1)
#         "print board\n"
#     )
#     expected = (
#         ". . . .\n"
#         ". . . .\n"
#         ". wN . ."
#     )
#     assert run(script).strip() == expected
# def test_bishop_legal_diagonal_move():
#     """בדיקה של מהלך חוקי עבור רץ באלכסון"""
#     script = (
#         "Board:\n"
#         "wB . . .\n"
#         ". . . .\n"
#         "Commands:\n"
#         "click 50 50\n"   # בחירת רץ ב-(0,0)
#         "click 150 150\n" # תנועה חוקית ל-(1,1)
#         "print board\n"
#     )
#     assert ". wB . ." in run(script)

# def test_queen_legal_straight_move():
#     """בדיקה של מהלך חוקי עבור מלכה בקו ישר"""
#     script = (
#         "Board:\n"
#         "wQ . . .\n"
#         ". . . .\n"
#         "Commands:\n"
#         "click 50 50\n"   # בחירת מלכה ב-(0,0)
#         "click 50 150\n"  # תנועה חוקית למטה ל-(1,0)
#         "print board\n"
#     )
#     assert ".\nwQ" in run(script)

# def test_malformed_click_command_ignored():
#     """בדיקה שפקודת קליק עם פורמט שגוי לא שוברת את התוכנית ומתעלמים ממנה"""
#     script = (
#         "Board:\n"
#         "wK . . .\n"
#         "Commands:\n"
#         "click abc 50\n"  # קואורדינטה לא מספרית - חסר טקסט
#         "click 50\n"      # חסר פרמטר Y
#         "print board\n"
#     )
#     assert run(script).strip() == "wK . . ."
# # ====================================================================
# # טסטים ממוקדים לאיטרציה 4 - להשגת 100% כיסוי (Coverage) מלא
# # ====================================================================

# def test_rook_blocked_by_intervening_piece():
#     """שורה 202: בדיקה שהלוגיקה מזהה חסימה ומחזירה False במסלול ישר"""
#     script = (
#         "Board:\n"
#         "wR wP . bK\n"
#         "Commands:\n"
#         "click 50 50\n"   # בחירת wR
#         "click 250 50\n"  # ניסיון לעבור דרך wP - חסום!
#         "print board\n"
#     )
#     assert run(script).strip() == "wR wP . bK"


# def test_bishop_blocked_by_intervening_piece():
#     """שורה 202: בדיקה שהלוגיקה מזהה חסימה ומחזירה False במסלול אלכסוני"""
#     script = (
#         "Board:\n"
#         "wB . . \n"
#         ". bP . \n"
#         ". . . \n"
#         "Commands:\n"
#         "click 50 50\n"   # בחירת wB
#         "click 250 250\n" # ניסיון לנוע באלכסון דרך bP - חסום!
#         "print board\n"
#     )
#     assert "wB" in run(script).split('\n')[0]


# def test_queen_diagonal_blocked():
#     """שורה 228: מפעיל את פונקציית המסלול האלכסוני הספציפית של המלכה"""
#     script = (
#         "Board:\n"
#         "wQ . .\n"
#         ". wP .\n"
#         ". . .\n"
#         "Commands:\n"
#         "click 50 50\n"
#         "click 250 250\n"  # מלכה מנסה לזוז באלכסון דרך wP - חסום!
#         "print board\n"
#     )
#     assert "wQ" in run(script).split('\n')[0]


# def test_invalid_geometric_move_for_pieces():
#     """שורה 222 + 246: מהלך שאינו תואם את הגאומטריה של הכלי (למשל רץ שזז ישר או מלכה שזזה כמו פרש)"""
#     script = (
#         "Board:\n"
#         "wB . . \n"
#         "Commands:\n"
#         "click 50 50\n"   # בחירת רץ
#         "click 150 50\n"  # רץ מנסה לזוז ישר למטה - לא חוקי גאומטרית!
#         "print board\n"
#     )
#     assert "wB" in run(script).split('\n')[0]


# def test_pawn_always_returns_true_geometry():
#     """שורה 251: מפעיל את ה-return True הייחודי של הרגלי (Pawn) בשלב הסטטי של איטרציה 4"""
#     script = (
#         "Board:\n"
#         "wP . .\n"
#         ". . .\n"
#         "Commands:\n"
#         "click 50 50\n"   # בחירת רגלי
#         "click 50 150\n"  # הזזת רגלי למטה
#         "print board\n"
#     )
#     assert "wP" in run(script).split('\n')[1]


# def test_click_on_empty_square_with_no_selection():
#     """שורה 277-278: לחיצה על משבצת ריקה כשאין שום כלי נבחר - מתעלם ולא קורס"""
#     script = (
#         "Board:\n"
#         ". . wK\n"
#         "Commands:\n"
#         "click 50 50\n"   # לחיצה על משבצת ריקה
#         "print board\n"
#     )
#     assert run(script).strip() == ". . wK"


# def test_captures_enemy_piece_and_friendly_block():
#     """בדיקת הכאת אויב מוצלחת ומניעת הכאת חבר"""
#     script = (
#         "Board:\n"
#         "wR . bR\n"
#         "Commands:\n"
#         "click 50 50\n"   # בחירת wR
#         "click 250 50\n"  # הכאת bR
#         "print board\n"
#     )
#     assert run(script).strip() == ". . wR"
#  # ====================================================================
# # טסטים מתוקנים ומדויקים לאיטרציה 5 - חוקי רגלי (Pawn) וכיסוי 100%
# # ====================================================================

# def test_pawn_move_forward_empty_square():
#     """רגלי לבן נע שורה אחת למעלה (מאינדקס 1 ל-0), רגלי שחור נע שורה אחת למטה (מאינדקס 1 ל-2)"""
#     script = (
#         "Board:\n"
#         ". . . .\n"
#         ". bP wP .\n"
#         ". . . .\n"
#         "Commands:\n"
#         "click 250 150\n" # בחירת wP שנמצא בשורה 1, עמודה 2
#         "click 250 50\n"  # תנועה למעלה לשורה 0, עמודה 2 - חוקי!
#         "click 150 150\n" # בחירת bP שנמצא בשורה 1, עמודה 1
#         "click 150 250\n" # תנועה למטה לשורה 2, עמודה 1 - חוקי!
#         "print board\n"
#     )
#     expected = (
#         ". . wP .\n"
#         ". . . .\n"
#         ". bP . ."
#     )
#     assert run(script).strip() == expected


# def test_pawn_cannot_move_two_squares():
#     """רגלי אינו יכול לנוע שתי משבצות קדימה באיטרציה זו"""
#     script = (
#         "Board:\n"
#         ". . . .\n"
#         ". . . .\n"
#         ". wP . .\n"
#         "Commands:\n"
#         "click 150 250\n" # בחירת wP בשורה 2, עמודה 1
#         "click 150 50\n"  # ניסיון לנוע 2 משבצות למעלה לשורה 0, עמודה 1 - לא חוקי!
#         "print board\n"
#     )
#     assert "wP" in run(script).split('\n')[2]


# def test_pawn_cannot_capture_forward():
#     """רגלי חסום ואינו יכול להכות כלי שנמצא ישירות מלפניו"""
#     script = (
#         "Board:\n"
#         ". bR . .\n"
#         ". wP . .\n"
#         "Commands:\n"
#         "click 150 150\n" # בחירת wP בשורה 1, עמודה 1
#         "click 150 50\n"  # ניסיון להכות את bR קדימה בשורה 0, עמודה 1 - אסור!
#         "print board\n"
#     )
#     assert "wP" in run(script).split('\n')[1]

# def test_pawn_captures_diagonally():
#     """רגלי מכה כלי אויב באלכסון קדימה בהצלחה ומדפיס את הלוח המלא בשתי שורות"""
#     script = (
#         "Board:\n"
#         ". bP . .\n"
#         "wP . . .\n"
#         "Commands:\n"
#         "click 50 150\n"  # בחירת wP בשורה 1, עמודה 0
#         "click 150 50\n"  # הכאת bP באלכסון בשורה 0, עמודה 1 - חוקי!
#         "print board\n"
#     )
#     expected = (
#         ". wP . .\n"
#         ". . . ."
#     )
#     assert run(script).strip() == expected
# def test_pawn_cannot_capture_friendly_diagonally():
#     """רגלי אינו יכול להכות כלי מאותו צבע באלכסון"""
#     script = (
#         "Board:\n"
#         ". wK . .\n"
#         "wP . . .\n"
#         "Commands:\n"
#         "click 50 150\n"  # בחירת wP בשורה 1, עמודה 0
#         "click 150 50\n"  # לחיצה על כלי חבר wK בשורה 0, עמודה 1 - מחליף בחירה
#         "print board\n"
#     )
#     assert "wP" in run(script).split('\n')[1]


# def test_pawn_always_returns_true_geometry():
#     """טסט משלים להפעלת שורה 251 עם תנועה אנכית תקינה של רגלי לבן"""
#     script = (
#         "Board:\n"
#         ". . .\n"
#         "wP . .\n"
#         "Commands:\n"
#         "click 50 150\n"  # בחירת wP בשורה 1
#         "click 50 50\n"   # תנועה למעלה לשורה 0
#         "print board\n"
#     )
#     assert "wP" in run(script).split('\n')[0]

#     # ====================================================================
# # טסטים עבור איטרציה 6 - תנועה לאורך זמן (Movement Over Time)
# # ====================================================================

# def test_pawn_move_delayed_by_time():
#     """בדיקה שרגלי לא זז מיד, ורק לאחר זמן המתנה מספיק הוא מגיע ליעד"""
#     script = (
#         "Board:\n"
#         ". . .\n"
#         "wP . .\n"
#         "Commands:\n"
#         "click 50 150\n"  # בחירת wP
#         "click 50 50\n"   # פקודת תנועה למעלה
#         "print board\n"   # הדפסה מיידית בזמן 0 - הכלי עדיין למטה!
#         "wait 500\n"
#         "print board\n"   # הדפסה בזמן 500 - עדיין לא הגיע (דורש 1000)
#         "wait 500\n"      # הגעה לזמן 1000
#         "print board\n"   # עכשיו הכלי חייב להופיע למעלה!
#     )
    
#     output = run(script).strip().split("\n\n")
    
#     # הדפסה 1 (זמן 0) - בשורה השנייה יש wP
#     assert "wP" in output[0].split("\n")[1]
    
#     # הדפסה 2 (זמן 500) - בשורה השנייה עדיין יש wP
#     assert "wP" in output[1].split("\n")[1]
    
#     # הדפסה 3 (זמן 1000) - הכלי הגיע לשורה הראשונה (אינדקס 0)
#     assert "wP" in output[2].split("\n")[0]
import io
import pytest
from kungfu_chess.texttests.script_runner import TextTestRunner


def run(script_text: str) -> str:
    """פונקציית עזר להרצת ה-ScriptRunner וקבלת הפלט כמחרוזת"""
    runner = TextTestRunner()
    input_stream = io.StringIO(script_text)
    output_stream = io.StringIO()
    runner.run(input_stream, output_stream)
    return output_stream.getvalue()


# ====================================================================
# טסטים בסיסיים ואינטראקציות לחיצה (איטרציות 4 ו-5 מעודכנות לזמן)
# ====================================================================

def test_click_moves_piece_and_updates_board():
    """
    בודק שלחיצה על צריח לבן ולאחר מכן לחיצה על משבצת ריקה מימין
    מזיזה את הצריח בהצלחה לאחר זמן ההמתנה הדרוש.
    """
    script = (
        "Board:\n"
        "wK . . bK\n"
        ". . . .\n"
        "wR . . bR\n"
        "Commands:\n"
        "click 50 250\n"    # בוחר את wR ב-(2, 0)
        "click 150 250\n"   # מזיז ל-(2, 1)
        "wait 1000\n"       # המתנה להגעת הכלי ליעדו
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
    נלחץ על המלך wK, אז נחליף לצריח wR, ואז נזיז את הצריח.
    """
    script = (
        "Board:\n"
        "wK . . bK\n"
        ". . . .\n"
        "wR . . bR\n"
        "Commands:\n"
        "click 50 50\n"     # בוחר את wK
        "click 50 250\n"    # מחליף בחירה ל-wR (מאותו הצבע)
        "click 150 250\n"   # מזיז את wR ל-(2, 1)
        "wait 1000\n"       # המתנה להגעת הכלי ליעדו
        "print board\n"
    )
    expected = (
        "wK . . bK\n"
        ". . . .\n"
        ". wR . bR"
    )
    assert run(script).strip() == expected


# ====================================================================
# בדיקות חוקיות תנועה גיאומטרית עבור כל סוגי הכלים (כולל wait)
# ====================================================================

def test_knight_legal_l_shape_move():
    """פרש מבצע מהלך חוקי בצורת L וזז בהצלחה"""
    script = (
        "Board:\n"
        "wN . . .\n"
        ". . . .\n"
        ". . . .\n"
        "Commands:\n"
        "click 50 50\n"   # בחירת הפרש ב-(0,0)
        "click 150 250\n" # תנועה חוקית ל-(2,1)
        "wait 1000\n"     # המתנה להגעת הכלי
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
        "wait 1000\n"     # המתנה להגעת הכלי
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
        "wait 1000\n"     # המתנה להגעת הכלי
        "print board\n"
    )
    assert ".\nwQ" in run(script)


def test_captures_enemy_piece_and_friendly_block():
    """בדיקת הכאת אויב מוצלחת ומניעת הכאת חבר"""
    script = (
        "Board:\n"
        "wR . bR\n"
        "Commands:\n"
        "click 50 50\n"   # בחירת wR ב-(0,0)
        "click 250 50\n"  # הכאת bR ב-(0,2) - מרחק של 2 משבצות
        "wait 2000\n"     # המתנה של 2000ms כי המרחק הוא 2 משבצות
        "print board\n"
    )
    assert run(script).strip() == ". . wR"


# ====================================================================
# בדיקות חוקיות רגלי (Pawn Rules)
# ====================================================================

def test_pawn_move_forward_empty_square():
    """רגלי לבן נע שורה אחת למעלה, רגלי שחור נע שורה אחת למטה"""
    script = (
        "Board:\n"
        ". . . .\n"
        ". bP wP .\n"
        ". . . .\n"
        "Commands:\n"
        "click 250 150\n" # בחירת wP שנמצא בשורה 1, עמודה 2
        "click 250 50\n"  # תנועה למעלה לשורה 0, עמודה 2 - חוקי!
        "click 150 150\n" # בחירת bP שנמצא בשורה 1, עמודה 1
        "click 150 250\n" # תנועה למטה לשורה 2, עמודה 1 - חוקי!
        "wait 1000\n"     # המתנה להגעת הכלים
        "print board\n"
    )
    expected = (
        ". . wP .\n"
        ". . . .\n"
        ". bP . ."
    )
    assert run(script).strip() == expected


def test_pawn_captures_diagonally():
    """רגלי מכה כלי אויב באלכסון קדימה בהצלחה ומדפיס את הלוח המלא"""
    script = (
        "Board:\n"
        ". bP . .\n"
        "wP . . .\n"
        "Commands:\n"
        "click 50 150\n"  # בחירת wP בשורה 1, עמודה 0
        "click 150 50\n"  # הכאת bP באלכסון בשורה 0, עמודה 1 - חוקי!
        "wait 1000\n"     # המתנה להגעת הכלי
        "print board\n"
    )
    expected = (
        ". wP . .\n"
        ". . . ."
    )
    assert run(script).strip() == expected


def test_pawn_always_returns_true_geometry():
    """טסט משלים לתנועה אנכית תקינה של רגלי לבן"""
    script = (
        "Board:\n"
        ". . .\n"
        "wP . .\n"
        "Commands:\n"
        "click 50 150\n"  # בחירת wP בשורה 1
        "click 50 50\n"   # תנועה למעלה לשורה 0
        "wait 1000\n"     # המתנה להגעת הכלי
        "print board\n"
    )
    assert "wP" in run(script).split('\n')[0]


# ====================================================================
# בדיקות מיוחדות לאיטרציה 6 - תנועה לאורך זמן (Movement Over Time)
# ====================================================================

def test_pawn_move_delayed_by_time():
    """בודק תנועה בשלבים: זמן 0, זמן 500 (טרם הגעה), וזמן 1000 (הגעה מלאה)"""
    script = (
        "Board:\n"
        ". . .\n"
        "wP . .\n"
        "Commands:\n"
        "click 50 150\n"
        "click 50 50\n"
        "print board\n"  # הדפסה 1 - שורות 0-1 (זמן 0)
        "wait 500\n"
        "print board\n"  # הדפסה 2 - שורות 2-3 (זמן 500)
        "wait 500\n"
        "print board\n"  # הדפסה 3 - שורות 4-5 (זמן 1000)
    )
    
    # פיצול לפי שורות בודדות
    lines = run(script).strip().split("\n")
    
    # הדפסה 1 (זמן 0) - הכלי עדיין למטה בשורה השנייה (אינדקס 1)
    assert "wP" in lines[1]
    
    # הדפסה 2 (זמן 500) - הכלי עדיין למטה בשורה הרביעית (אינדקס 3)
    assert "wP" in lines[3]
    
    # הדפסה 3 (זמן 1000) - הכלי הגיע למעלה לשורה החמישית (אינדקס 4)
    assert "wP" in lines[4]


def test_script_runner_invalid_wait_and_clicks():
    """מכסה מקרי קצה של פקודות wait לא תקינות ולחיצות מחוץ לגבולות/לא מספריות"""
    script = (
        "Board:\n"
        "wP . .\n"
        "Commands:\n"
        "wait abc\n"       # שורה לא מספרית ב-wait (לא מזיז את הזמן)
        "click abc 50\n"   # קואורדינטה לא מספרית
        "click 999 999\n"  # מחוץ לגבולות הלוח
        "print board\n"
    )
    assert "wP" in run(script)