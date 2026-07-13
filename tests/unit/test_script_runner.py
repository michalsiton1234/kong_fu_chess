
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
        ". bP . .\n"
        ". . . ."
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
    # ====================================================================
# בדיקות מיוחדות לאיטרציה 7 - חוקי Common Route (No Redirection & No Cooldown)
# ====================================================================

def test_piece_cannot_be_redirected_while_moving():
    """בודק שלא ניתן לשנות את היעד של כלי בזמן שהוא כבר בתנועה"""
    script = (
        "Board:\n"
        "wR . . .\n"
        "Commands:\n"
        "click 50 50\n"   # בוחר wR ב-(0,0)
        "click 350 50\n"  # פוקד לזוז ל-(0,3) - מרחק 3 משבצות (3000ms)
        "wait 1000\n"     # מחכה 1000ms (הכלי בדרך, רשום ב-_pending_moves)
        
        # ניסיון לבצע מהלך חדש לגמרי בזמן שהכלי בתנועה - אמור להתעלם לחלוטין!
        "click 350 50\n"  
        "click 150 50\n"  
        
        "wait 2000\n"     # מחכה עוד 2000ms (סך הכל 3000ms)
        "print board\n"
    )
    # הכלי חייב להגיע ליעד המקורי שלו (0,3) ולא להיעצר או לשנות כיוון באמצע
    expected = ". . . wR"
    assert run(script).strip() == expected


def test_piece_can_move_immediately_after_arrival():
    """בודק שכלי שהגיע ליעדו יכול לזוז שוב מיד ללא cooldown"""
    script = (
        "Board:\n"
        "wR . . .\n"
        "Commands:\n"
        "click 50 50\n"   # בוחר wR ב-(0,0)
        "click 150 50\n"  # מזיז ל-(0,1) - לוקח 1000ms
        "wait 1000\n"     # מחכה שיגיע (הזמן עכשיו 1000 והכלי נחת פיזית בלוח)
        "click 150 50\n"  # בוחר אותו מיד ממיקומו החדש ב-(0,1) - חוקי! (No Cooldown)
        "click 250 50\n"  # מזיז ל-(0,2) - לוקח עוד 1000ms
        "wait 1000\n"     # מחכה שיגיע
        "print board\n"
    )
    expected = ". . wR ."
    assert run(script).strip() == expected