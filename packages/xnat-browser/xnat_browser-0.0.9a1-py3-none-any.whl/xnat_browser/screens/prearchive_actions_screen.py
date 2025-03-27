import enum

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button


class PrearchiveActionResult(enum.IntEnum):
    ABORT = enum.auto()
    ARCHIVE = enum.auto()
    REBUILD = enum.auto()
    DELETE = enum.auto()
    MOVE = enum.auto()


class PrearchiveActionsScreen(ModalScreen[PrearchiveActionResult]):
    BINDINGS = [
        ('escape', 'pop_screen')
    ]
    CSS_PATH = 'screen.tcss'

    DEFAULT_CSS = """
    PrearchiveActionsScreen {
        align: center middle;
        width: auto;
        height: auto;
    }

    PrearchiveActionsScreen Vertical {
        height: auto;
        width: auto;
    }

    PrearchiveActionsScreen Horizontal {
        width: auto;
        height: auto;
    }

    PrearchiveActionsScreen Horizontal Button {
        margin: 2;
        width: 10;
    }
    """

    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Button('Archive', id='archive')
            yield Button('Rebuild', id='rebuild')
            yield Button('Move', id='move')
            yield Button('Delete', id='delete')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case 'archive':
                self.dismiss(PrearchiveActionResult.ARCHIVE)
            case 'rebuild':
                self.dismiss(PrearchiveActionResult.REBUILD)
            case 'delete':
                self.dismiss(PrearchiveActionResult.DELETE)
            case 'move':
                self.dismiss(PrearchiveActionResult.MOVE)
            case _:
                raise RuntimeError(f'Unknown button pressed "{event.button.id}"')

    def action_pop_screen(self) -> None:
        self.dismiss(PrearchiveActionResult.ABORT)
