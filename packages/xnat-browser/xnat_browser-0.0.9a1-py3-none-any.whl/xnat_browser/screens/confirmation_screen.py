import enum

from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Label, Button


class ConfirmationResult(enum.IntEnum):
    YES = enum.auto()
    NO = enum.auto()


class ConfirmationScreen(ModalScreen[ConfirmationResult]):
    """Screen with a dialog to confirm or cancel an action."""
    BINDINGS = [
        ('escape', 'pop_screen')
    ]
    CSS_PATH = 'screen.tcss'

    DEFAULT_CSS = """
    ConfirmationScreen {
        align: center middle;
    }

    ConfirmationScreen Grid {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: 1fr 3;
        padding: 0 1;
        width: 40;
        height: 11;
        border: thick $background 80%;
        background: $surface;
    }

    ConfirmationScreen Label {
        column-span: 2;
        height: 1fr;
        width: 1fr;
        content-align: center middle;
    }    
    """

    def __init__(self, action_text: str) -> None:
        super().__init__()
        self.action_text = action_text

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.action_text, id='question'),
            Button('Yes', variant='success', id='yes'),
            Button('No', variant='error', id='no'),
            id='confirmation_dialog',
        )

    def action_pop_screen(self) -> None:
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case 'yes':
                self.dismiss(ConfirmationResult.YES)
            case 'no':
                self.dismiss(ConfirmationResult.NO)
            case _:
                raise RuntimeError(f'Unknown button pressed "{event.button.id}"')
