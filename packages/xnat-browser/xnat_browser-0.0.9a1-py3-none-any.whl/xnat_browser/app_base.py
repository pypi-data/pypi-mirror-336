import atexit
import logging
from typing import Any

import textual
import xnat
from textual.app import App
from textual.binding import Binding
from textual.widgets import RichLog
from xnat.exceptions import XNATAuthError, XNATLoginFailedError, XNATExpiredCredentialsError, XNATNotConnectedError

from xnat_browser.log_handler import TextualLogHandler
from xnat_browser.screens.quit_screen import QuitScreen


class Loading:
    def __init__(self, widget: textual.widget.Widget) -> None:
        self.widget = widget

    def __enter__(self) -> None:
        self.widget.loading = True

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.widget.loading = False

    async def __aenter__(self) -> None:
        self.widget.loading = True

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.widget.loading = False


class XnatBase(App):
    DEFAULT_CSS = """
    RichLog.remove {
        display: none;
    }
    
    #rich_log {
        height: 4;
        border: panel;
    }
    """

    BINDINGS = [
        Binding('f1', 'show_log', 'Log'),
        Binding('q', 'quit', 'Quit'),
        Binding('f12', 'screenshot', 'Screenshot', show=False),
    ]

    def __init__(self, server: str, username: str | None, password: str | None, log_level: int = logging.INFO) -> None:
        super().__init__()
        # noinspection PyTypeChecker
        self.title = f'{self.__class__.__name__} ({server})'
        self._server = server
        self.logger = logging.getLogger('xnat_browser')
        self.logger.setLevel(log_level)
        self.logger.debug(f'XNATpy version: {xnat.__version__}')

        atexit.register(self.disconnect)
        self.logger.debug('Starting XNAT session.')
        try:
            self.session = xnat.connect(server=self._server, user=username, password=password, default_timeout=900)
            self.logger.debug('Login succeeded.')
            self.logger.debug(f'XNAT server version: {self.session.xnat_version}')
        except (XNATAuthError, XNATLoginFailedError, XNATExpiredCredentialsError, XNATNotConnectedError) as e:
            self.logger.error('Error connecting to XNAT server.')
            self.logger.debug(e)

    def disconnect(self) -> None:
        """Disconnect from the server."""
        if self.session is not None:
            self.session.logger.handlers.clear()
            self.session.disconnect()
            self.session = None

    def _setup_logging(self) -> RichLog:
        log_window = RichLog(id='rich_log', name='Log')

        log_handler = TextualLogHandler(log_window)
        log_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)7s [%(filename)25s:%(lineno)3s - %(funcName)25s()] %(message)s'))

        self.logger.addHandler(log_handler)

        if self.logger.level > logging.DEBUG:
            log_window.set_class(True, 'remove')

        self.logger.debug('Logger started')
        return log_window

    def action_screenshot(self, filename: str | None = None, path: str | None = None) -> None:
        self.save_screenshot(filename, path)

    def action_show_log(self) -> None:
        self.query_one('#rich_log', RichLog).toggle_class('remove')

    async def action_quit(self) -> None:
        await self.push_screen(QuitScreen())
