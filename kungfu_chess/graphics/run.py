import cv2
from kungfu_chess.controller.controller import Controller
from kungfu_chess.engine.game_engine import GameEngine
from kungfu_chess.engine.game_events import CounterCaptureEvent, MoveCompletedEvent
from kungfu_chess.graphics.assets import BOARD_PNG
from kungfu_chess.graphics.bridge.match_recorder import MatchRecorder
from kungfu_chess.graphics.bridge.snapshot_builder import SnapshotBuilder
from kungfu_chess.graphics.input.mouse_adapter import MouseAdapter
from kungfu_chess.graphics.view.board_layout import BOARD_OFFSET_X, cell_bounds
from kungfu_chess.graphics.view.graphics_board_mapper import GraphicsBoardMapper
from kungfu_chess.graphics.view.renderer import Renderer
from kungfu_chess.graphics.view.window_fit import fit_display_scale
from kungfu_chess.io.board_parser import BoardParser
from kungfu_chess.model.position import Position

OPENING_BOARD = """
bR bN bB bQ bK bB bN bR
bP bP bP bP bP bP bP bP
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
wP wP wP wP wP wP wP wP
wR wN wB wQ wK wB wN wR
""".strip()

WINDOW_NAME = "KungFu Chess"
FRAME_MS = 16
TIME_SCALE = 4
REJECT_FLASH_MS = 600


def _cell_center_pixels(row: int, col: int) -> tuple:
    x0, y0, x1, y1 = cell_bounds(row, col)
    return BOARD_OFFSET_X + (x0 + x1) // 2, (y0 + y1) // 2


def _try_jump(
    controller: Controller,
    board,
    engine: GameEngine,
    recorder: MatchRecorder,
    row: int,
    col: int,
) -> None:
    piece = board.piece_at(Position(row, col))
    if piece is None:
        return
    was_airborne = engine.arbiter.is_piece_airborne(piece)
    image_x, image_y = _cell_center_pixels(row, col)
    controller.handle_jump(board, image_x, image_y)
    if not was_airborne and engine.arbiter.is_piece_airborne(piece):
        recorder.log_jump(engine.arbiter.current_time, piece)


def main() -> None:
    board = BoardParser().parse(OPENING_BOARD)
    engine = GameEngine()
    match_recorder = MatchRecorder()
    engine.subscribe(MoveCompletedEvent, match_recorder)
    engine.subscribe(CounterCaptureEvent, match_recorder)

    controller = Controller(engine, GraphicsBoardMapper())
    builder = SnapshotBuilder()
    renderer = Renderer(BOARD_PNG)

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

    hover_cell = None

    def _on_mouse_event(event, image_x, image_y, cell) -> None:
        nonlocal hover_cell
        hover_cell = cell

    mouse = MouseAdapter(WINDOW_NAME, on_mouse_event=_on_mouse_event)

    reject_cell = None
    reject_until = 0
    window_initialized = False

    while True:
        try:
            if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
                break
        except cv2.error:
            break

        click = mouse.consume_click()
        if click is not None:
            image_x, image_y = click
            controller.handle_click(board, image_x, image_y)
            failed = controller.last_failed_destination
            if failed is not None:
                reject_cell = (failed.row, failed.col)
                reject_until = engine.arbiter.current_time + REJECT_FLASH_MS
                controller.clear_failed_destination()

        right_click = mouse.consume_right_click()
        if right_click is not None:
            image_x, image_y = right_click
            mapper = controller._board_mapper
            pos = mapper.to_position(board, image_x, image_y)
            if pos is not None:
                _try_jump(
                    controller,
                    board,
                    engine,
                    match_recorder,
                    pos.row,
                    pos.col,
                )

        if reject_cell is not None and engine.arbiter.current_time >= reject_until:
            reject_cell = None

        snapshot = builder.build(
            board,
            engine,
            selected_piece=controller.selected_piece,
            hover_cell=hover_cell,
            reject_cell=reject_cell,
            match_recorder=match_recorder,
        )
        img = renderer.render(snapshot)

        height, width = img.img.shape[:2]
        mouse.set_image_size(width, height)

        if not window_initialized:
            scale = fit_display_scale(width, height)
            start_w = max(1, int(width * scale))
            start_h = max(1, int(height * scale))
            cv2.resizeWindow(WINDOW_NAME, start_w, start_h)
            window_initialized = True

        cv2.imshow(WINDOW_NAME, img.img)

        key = cv2.waitKey(FRAME_MS) & 0xFF
        if key == ord("q"):
            break
        if key in (ord("j"), ord("J")):
            selected = controller.selected_piece
            if selected is not None:
                _try_jump(
                    controller,
                    board,
                    engine,
                    match_recorder,
                    selected.cell.row,
                    selected.cell.col,
                )

        if not engine.game_over or engine.arbiter._pending_motions:
            engine.advance_time(board, FRAME_MS * TIME_SCALE)

    cv2.destroyAllWindows()
