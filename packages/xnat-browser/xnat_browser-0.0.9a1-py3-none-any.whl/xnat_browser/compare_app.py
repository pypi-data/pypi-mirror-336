import logging

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, RichLog, SelectionList, DataTable

from xnat_browser.app_base import XnatBase


class XnatCompare(XnatBase):
    CSS_PATH = 'compare.tcss'
    BINDINGS = [
        Binding('f5', 'refresh', 'Refresh'),
    ]

    def __init__(self, server: str, username: str | None = None, password: str | None = None,
                 log_level: int = logging.INFO) -> None:
        super().__init__(server, username, password, log_level)

    def compose(self) -> ComposeResult:
        logger = self._setup_logging()

        yield Header(show_clock=True)
        with Vertical():
            with Horizontal():
                yield SelectionList(id='project_selection_list')
                yield SelectionList(id='subject_selection_list')
            with Horizontal():
                yield DataTable(id='left_table')
                yield DataTable(id='right_table')
        yield logger
        yield Footer()

    def on_mount(self) -> None:
        self.query_one('#rich_log', RichLog).border_title = 'Log'
        self.logger.debug('Welcome')
