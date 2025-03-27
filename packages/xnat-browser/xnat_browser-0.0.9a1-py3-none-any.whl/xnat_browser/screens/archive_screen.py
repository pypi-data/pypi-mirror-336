import enum
from dataclasses import dataclass

from textual.app import ComposeResult
from textual.containers import Grid, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Label, Input, Select, Switch, Rule, Button


class Overwrite(str, enum.Enum):
    NONE = 'none'
    APPEND = 'append'
    DELETE = 'delete'


@dataclass
class ArchiveResult:
    project: str
    subject: str
    experiment: str
    overwrite: Overwrite = Overwrite.NONE
    quarantine: bool = False
    trigger_pipelines: bool = False


class ArchiveScreen(ModalScreen[ArchiveResult | None]):
    """Screen with a dialog to confirm or cancel an action."""
    BINDINGS = [
        ('escape', 'pop_screen')
    ]
    CSS_PATH = 'screen.tcss'

    DEFAULT_CSS = """
    ArchiveScreen {
        align: center middle;
    }

    ArchiveScreen  Grid {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: 1fr 3;
        padding: 0 1;
        width: 100;
        height: 100%;
        border: thick $background 80%;
        background: $surface;
    }

    ArchiveScreen Input {
        column-span: 2;
        height: 3;
        width: 1fr;
        content-align: center middle;
    }
    """

    def __init__(self, project: str | None, subject: str | None, experiment: str | None) -> None:
        super().__init__()
        self.project = project
        self.subject = subject
        self.experiment = experiment

    def compose(self) -> ComposeResult:
        with Grid(id='archive_dialog'):
            yield Label('Project:')
            yield Input(value=self.project, placeholder='Project', id='project_input')
            yield Label('Subject:')
            yield Input(value=self.subject, placeholder='Subject', id='subject_input')
            yield Label('Experiment:')
            yield Input(value=self.experiment, placeholder='Experiment', id='experiment_input')
            yield Label('Overwrite:', id='overwrite')
            yield Select([('None', Overwrite.NONE), ('Append', Overwrite.APPEND), ('Delete', Overwrite.DELETE)],
                         allow_blank=False, value=Overwrite.NONE, id='overwrite_select')
            yield Label('Quarantine:')
            yield Switch(id='switch_quarantine')
            yield Label('Trigger pipelines:')
            yield Switch(id='switch_trigger_pipelines')
            yield Rule(line_style='double')
            yield Label('Proceed with archive action?', id='question')
            with Horizontal():
                yield Button('Yes', variant='success', id='yes')
                yield Button('No', variant='error', id='no')

    def action_pop_screen(self) -> None:
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        result = ArchiveResult(project=self.query_exactly_one('#project_input', Input).value,
                               subject=self.query_exactly_one('#subject_input', Input).value,
                               experiment=self.query_exactly_one('#experiment_input', Input).value,
                               overwrite=self.query_exactly_one('#overwrite_select', Select).value,  # type: ignore
                               quarantine=self.query_exactly_one('#switch_quarantine', Switch).value,
                               trigger_pipelines=self.query_exactly_one('#switch_trigger_pipelines', Switch).value)

        match event.button.id:
            case 'yes':
                self.dismiss(result)
            case 'no':
                self.dismiss(None)
            case _:
                raise RuntimeError(f'Unknown button pressed "{event.button.id}"')
