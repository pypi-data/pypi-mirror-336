import logging

import rich.logging
from textual.widgets import RichLog


class TextualLogHandler(logging.Handler):
    def __init__(self, _text_edit: RichLog) -> None:
        super().__init__()

        self.text_edit = _text_edit
        self.handler = rich.logging.RichHandler()

    def setFormatter(self, fmt: logging.Formatter | None) -> None:
        super().setFormatter(fmt)
        self.handler.setFormatter(fmt)

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.handler.render_message(record, self.format(record))
        self.text_edit.write(msg)
