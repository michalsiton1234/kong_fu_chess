"""Text I/O simulation for testing without a GUI (architecture Rule 2):
ScriptParser splits a raw script into its board/commands sections, and
TextTestRunner drives execution of the recognized commands (currently only
"print board", via the PrintBoard command)."""
