"""Shared text I/O for the board: BoardParser (text -> Board) and BoardPrinter
(Board -> text). Kept in a shared io package rather than hidden inside
texttests, so any future consumer (e.g. a future GUI's debug view) can reuse
them without depending on the test-running machinery."""
