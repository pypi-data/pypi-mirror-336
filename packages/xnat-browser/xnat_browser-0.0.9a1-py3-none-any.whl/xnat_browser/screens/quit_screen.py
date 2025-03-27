from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Label, Button


class QuitScreen(ModalScreen):
    """Screen with a dialog to quit."""
    BINDINGS = [
        ('escape', 'pop_screen')
    ]
    CSS_PATH = 'screen.tcss'

    DEFAULT_CSS = """
    QuitScreen {
        align: center middle;
    }
    
    QuitScreen Grid {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: 1fr 3;
        padding: 0 1;
        width: 40;
        height: 11;
        border: thick $background 80%;
        background: $surface;
    }
    
    QuitScreen Label {
        column-span: 2;
        height: 1fr;
        width: 1fr;
        content-align: center middle;
    }    
    """

    def compose(self) -> ComposeResult:
        yield Grid(
            Label('Are you sure you want to quit?', id='question'),
            Button('Quit', variant='success', id='quit'),
            Button('Cancel', variant='primary', id='cancel'),
            id='quit_dialog',
        )

    def action_pop_screen(self) -> None:
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'quit':
            self.app.exit()
        else:
            self.app.pop_screen()
