# Kung-Fu Chess — Iteration 1: Board and Pieces (pure model + text I/O)

## מה יש כאן
מימוש מלא של **Phase 1–2** מה-roadmap הרשמי (`kung_fu_chess_architecture.md`):
1. **Board Presentation without UI** — Text I/O / test framework
2. **Clean State** — המודל הטהור: `Position`, `Piece`, `Board`

מבנה החבילות, שמות המחלקות, וכללי ה-notation תואמים **בדיוק** למסמכי
הארכיטקטורה והדרישות שסופקו (`kung_fu_chess_architecture.md`,
`kung_fu_chess_requirements.md`, ותמונות ה-Ultracode). זו לא ארכיטקטורה
שאני בחרתי — זו הארכיטקטורה שנדרשה, מיושמת כלשונה.

**שינוי מהותי מהגרסה הקודמת:** בסבב הקודם צמצמתי ל-5 מחלקות "שטוחות"
לפי עקרון "לא להגזים". עכשיו יש מסמך ארכיטקטורה רשמי ומחייב מהקורס עם
שמות קבצים ומחלקות מדויקים (`Position`, `Piece`, `Board`, `BoardParser`,
`BoardPrinter`, `TextTestRunner`, `ScriptParser`, `PrintBoard`) — אז אני
עוקבת אחריו במדויק, גם אם יש יותר קבצים מקודם. זו לא חריגה מ"לא להגזים" —
זו פשוט דרישה מפורשת וברורה יותר שדורסת את ברירת המחדל שלי.

## מבנה החבילה

```
main.py                                # entry point דק — VPL מריץ אותו ישירות
kungfu_chess/
  model/                                # המודל הטהור — בלי רינדור, בלי I/O, בלי כללי משחק
    position.py                         # Position — value object (row, col)
    piece.py                            # Piece — id, color, kind, cell, state (idle/moving/captured)
    board.py                            # Board — אחסון לוגי: add/remove/piece_at/move/in_bounds
    exceptions.py                       # DuplicateOccupancyError, PieceNotFoundError, OutOfBoundsError
  io/                                   # I/O משותף לטקסט — לא תלוי ב-texttests
    notation.py                         # טבלת token <-> (color, kind) המשותפת ל-parser ול-printer
    board_parser.py                     # BoardParser — טקסט -> Board
    board_printer.py                    # BoardPrinter — Board -> טקסט
    exceptions.py                       # UnknownTokenError, RowWidthMismatchError
  texttests/                            # סימולציית קלט/פלט טקסטואלית (Rule 2)
    script_parser.py                    # ScriptParser — מפצל "Board:"/"Commands:" לשני חלקים
    script_runner.py                    # TextTestRunner + PrintBoard
  app.py                                # KungFuChessApp — composition root
tests/
  unit/                                 # טסט לכל מודול, אחד-לאחד
  integration/                          # קצה-לקצה דרך KungFuChessApp
```

## מיפוי ל-15 כללי הארכיטקטורה (הרלוונטיים לאיטרציה זו)

| כלל | איך מיושם |
|---|---|
| **1 — SRP** | כל קובץ = אחריות אחת: `Position` נתונים בלבד, `Board` אחסון בלבד, `BoardParser` המרת טקסט→Board בלבד, `ScriptParser` פיצול מבנה הסקריפט בלבד (לא יודע על notation), `TextTestRunner` תזמור בלבד |
| **2 — Textual I/O** | `TextTestRunner` + `PrintBoard` — מאפשרים בדיקה מלאה בלי GUI |
| **3 — Separation of Concerns** | Model (`model/`) לא מכיר I/O; I/O (`io/`) לא מכיר את מבנה הסקריפט; אף אחד לא מכיר רינדור/פיקסלים |
| **9 — זמן דטרמיניסטי** | לא רלוונטי עדיין (אין תנועה/זמן באיטרציה זו) — יגיע ב-`RealTimeArbiter` בהמשך |
| **13 — Robust Error Handling** | `test_board_parser.py`: reject illegal token, reject inconsistent row length; `test_script_runner.py`: ERROR codes מודפסים נכון |
| **15 — Refactoring / Code Smells** | `notation.py` משותף ל-parser+printer (DRY) — טבלת ה-token מוגדרת פעם אחת; כל קובץ קטן וממוקד |

## דברים שנדחו בכוונה לאיטרציות הבאות (לפי ה-roadmap)
- `BoardMapper`, `Controller` — Phase 3
- `RookRule` (Strategy per piece) — Phase 4
- `RuleEngine`, `GameEngine` — Phase 5
- `RealTimeArbiter`, `Motion` — Phase 6
- לכידות, ניצחון — Phase 7
- הכתרה — Phase 8
- שאר הכלים — Phase 9
- קפיצה/Dodge, Drone, אנימציות, matchmaking — לפי `kung_fu_chess_requirements.md` §3-4, כשיגיע הזמן

זה בכוונה — Rule 12 (roadmap) אומר לא להוסיף כלים/מנגנונים לפני שהשלד יציב,
ועקרון העיצוב במסמך הדרישות אומר לא לבנות אבסטרקציות ספקולטיביות למה
שעוד לא נדרש בפועל.

## פורמט הטקסט (Board Notation)
תואם בדיוק למה שכבר אושר ב-VPL (הבדיקות שראינו עם "Expected output"):
```
Board:
wK . . bK
. . . .
wR . . bR
Commands:
print board
```
- שורה נפרדת לכל row, תאים מופרדים ברווח
- `.` = תא ריק
- קידומת `w`/`b` + אות שחמט אחת: `K, Q, R, B, N, P`
- שגיאות: `ERROR UNKNOWN_TOKEN`, `ERROR ROW_WIDTH_MISMATCH`

**שינוי מגרסה קודמת:** הוסרה התמיכה בקונבנציית ה-case החלופית (`Wk`
לעומת `wK`) — היא לא מופיעה בשום מקום בספסיפיקציה הרשמית, והשארתה הייתה
עלולה לגרום לקבלה שגויה של טוקנים שאמורים להידחות ב"reject illegal piece
token".

## איך מריצים

```bash
pip install -r requirements-dev.txt
pytest
# 51 טסטים, 100% coverage. דוח HTML: htmlcov/index.html
```

## לגבי ה-URL של ה-git repo
כמו קודם — placeholder בשורה הראשונה של `main.py`, למלא לפני ההגשה.
