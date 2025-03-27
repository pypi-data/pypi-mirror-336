import enum
from typing import Final

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button


class ArchiveActionResult(enum.IntEnum):
    ABORT = enum.auto()
    DELETE = enum.auto()
    SHARE = enum.auto()
    EDIT = enum.auto()


RESULT_LUT: Final[dict[str, ArchiveActionResult]] = {
    'share': ArchiveActionResult.SHARE,
    'edit': ArchiveActionResult.EDIT,
    'delete': ArchiveActionResult.DELETE,
    'abort': ArchiveActionResult.ABORT
}


class ArchiveActionsScreen(ModalScreen[ArchiveActionResult]):
    BINDINGS = [
        ('escape', 'pop_screen')
    ]
    CSS_PATH = 'screen.tcss'

    DEFAULT_CSS = """
    ArchiveActionsScreen {
        align: center middle;
        width: auto;
        height: auto;
    }

    ArchiveActionsScreen Vertical {
        height: auto;
        width: auto;
    }

    ArchiveActionsScreen Horizontal {
        width: auto;
        height: auto;
    }

    ArchiveActionsScreen Horizontal Button {
        margin: 2;
        width: 10;
    }
    """

    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Button('Share', id='share')
            yield Button('Edit', id='edit')
            yield Button('Delete', id='delete')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        assert event.button.id is not None
        if (result := RESULT_LUT.get(event.button.id, None)) is None:
            raise RuntimeError(f'Unknown button pressed "{event.button.id}"')

        self.dismiss(result)

    def action_pop_screen(self) -> None:
        self.dismiss(ArchiveActionResult.ABORT)
