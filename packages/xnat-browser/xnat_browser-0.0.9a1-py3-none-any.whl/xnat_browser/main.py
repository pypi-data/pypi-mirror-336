""" CLI """
import logging
from pathlib import Path
from typing import cast, Union

import rich.traceback
import typer
import xnat_browser.io
from xnat_browser.browse_app import XnatBrowser
from xnat_browser.compare_app import XnatCompare
from xnat_browser.query_app import XnatQuery

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command()
def browse(server: str,
           verbose: bool = typer.Option(False, '--verbose', '-v'),
           username: Union[str, None] = typer.Option(None, '--username', '-u'),
           password: Union[str, None] = typer.Option(None, '--password', '-p')) -> None:
    log_level = logging.DEBUG if verbose else logging.INFO
    XnatBrowser(server, username, password, log_level).run()


@app.command()
def compare(server: str,
            verbose: bool = typer.Option(False, '--verbose', '-v'),
            username: Union[str, None] = typer.Option(None, '--username', '-u'),
            password: Union[str, None] = typer.Option(None, '--password', '-p')) -> None:
    log_level = logging.DEBUG if verbose else logging.INFO
    XnatCompare(server, username, password, log_level).run()


@app.command()
def query(server: str,
          search: Path = typer.Option(None, '--search', '-s', help='Search to load at startup'),
          verbose: bool = typer.Option(False, '--verbose', '-v'),
          username: Union[str, None] = typer.Option(None, '--username', '-u'),
          password: Union[str, None] = typer.Option(None, '--password', '-p')) -> None:
    log_level = logging.DEBUG if verbose else logging.INFO
    query_widget: xnat_browser.io.QueryProtocol = XnatQuery(server, username, password, log_level, search)
    cast(XnatQuery, query_widget).run()


if __name__ == "__main__":
    rich.traceback.install(width=None, word_wrap=True)
    app()
