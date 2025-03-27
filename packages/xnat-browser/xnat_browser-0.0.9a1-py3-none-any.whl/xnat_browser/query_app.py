from __future__ import annotations

import functools
import http
import logging
from pathlib import Path
from typing import cast, Optional, Iterator

import xnat
import xnat.search
from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, ScrollableContainer
from textual.widgets import Button, Header, Footer, SelectionList, RadioSet, RichLog, TabbedContent, TabPane
from textual_fspicker import FileOpen, Filters, FileSave
from xnat.core import XNATBaseObject
from xnat.exceptions import XNATResponseError

from textual_sortable_datatable.sortable_data_table import SortableDataTable

from xnat_browser import io
from xnat_browser.app_base import XnatBase, Loading
from xnat_browser.constants import SEARCH_BASE_BUTTONS, QUERY_SELECTIONS
from xnat_browser.io import QueryProtocol
from xnat_browser.search_entry import get_select_fields, get_search_terms, SearchEntry, SearchConstraintError
from xnat_browser.xnat_plot import XnatPlot
from xnat_browser.xnat_tree import _get_http_status_code


class XnatQuery(XnatBase):
    CSS_PATH = 'query.tcss'
    BINDINGS = [
        Binding('a', 'add_constraint', 'Add Constraint'),
        Binding('f2', 'load_search', 'Load Search'),
        Binding('f3', 'save_search', 'Save Search'),
        Binding('s', 'save_result', 'Save Result'),
        Binding('ctrl+s', 'show_selections', 'Root/Fields'),
    ]

    def __init__(self, server: str, username: str | None, password: str | None, log_level: int = logging.INFO,
                 search: Path | None = None) -> None:
        super().__init__(server, username, password, log_level)
        self.fields = get_select_fields(get_search_terms(self._get_classes([x.value for x in QUERY_SELECTIONS])))
        self._search = search

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id='horizontal'):
            with TabbedContent():
                with TabPane('Query', id='tab_query'):
                    yield from self._compose_query_tab()
                with TabPane('Data', id='tab_data'):
                    yield SortableDataTable(id='data_table')
                with TabPane('Graph', id='tab_graph'):
                    yield XnatPlot(self.logger, id='xnat_plot')
        yield self._setup_logging()
        yield Footer()

    def _compose_query_tab(self) -> ComposeResult:
        with ScrollableContainer(id='query_input'):
            with Horizontal(id='search_base_fields'):
                yield RadioSet(*SEARCH_BASE_BUTTONS, id='root_element')
                yield SelectionList[str](*QUERY_SELECTIONS, id='selections')
            yield Button(label='Run Query...', id='query_button')
            yield SearchEntry(fields=self.fields, id='id_0')

    @staticmethod
    def _get_next_id(entries: Iterator[SearchEntry]) -> str:
        max_id = max(int(x.id.lstrip('id_')) for x in entries)  # type: ignore
        return f'id_{max_id + 1}'

    def on_mount(self) -> None:
        self.query_one('#selections', SelectionList).border_title = 'Search Fields'
        self.query_one('#root_element', RadioSet).border_title = 'Root Element'
        data_table = self.query_one('#data_table', SortableDataTable)
        data_table.border_title = 'Results'
        data_table.zebra_stripes = True
        self.query_one('#query_input', ScrollableContainer).border_title = 'Input'
        self.query_one('#rich_log', RichLog).border_title = 'Log'

        if self._search is not None:
            io.load_search(self._search, cast(QueryProtocol, self))
            self._run_query()

    def get_query_constraints(self) -> list[xnat.search.Constraint]:
        constraints = []
        entries = self.query('SearchEntry').results(SearchEntry)
        for entry in entries:
            constraints.append(entry.constraint)
        return constraints

    def set_query_constraints(self, constraints: list[xnat.search.Constraint]) -> None:
        entries = list(self.query(SearchEntry).results(SearchEntry))

        diff = len(constraints) - len(entries)
        if diff > 0:
            parent = self.query_one('#query_input', ScrollableContainer)
            for _ in range(diff):
                next_id = self._get_next_id(self.query(SearchEntry).results(SearchEntry))
                parent.mount(SearchEntry(fields=self.fields, id=f'{next_id}'))
            entries = list(self.query(SearchEntry).results(SearchEntry))

        for index, constraint in enumerate(constraints):
            try:
                entries[index].constraint = constraint
            except SearchConstraintError as e:
                self.logger.error(e)

    def update_fields(self) -> None:
        search_fields = self.query_one('#selections', SelectionList)
        self.fields = get_select_fields(get_search_terms(self._get_classes(search_fields.selected)))
        entries = self.query(SearchEntry).results(SearchEntry)
        for entry in entries:
            entry.update_fields(self.fields)

    @on(SelectionList.SelectedChanged, '#selections')
    def fields_changed(self, _: SelectionList.SelectedChanged) -> None:
        self.update_fields()

    def _get_classes(self, selected: list[str]) -> list[XNATBaseObject]:
        assert self.session
        classes: list[XNATBaseObject] = []
        for data_type in selected:
            classes.append(getattr(self.session.classes, data_type))
        return classes

    def _get_root_element_name(self) -> Optional[xnat.search.Query]:
        assert self.session
        button = self.query_one('#root_element', RadioSet).pressed_button
        if button is None:
            return None

        return cast(xnat.search.Query, getattr(self.session.classes, str(button.label) + 'Data').query())

    def _get_query(self) -> Optional[xnat.search.Query]:
        query = self._get_root_element_name()
        if query is not None:
            for constraint in self.get_query_constraints():
                query = query.filter(constraint)

        return query

    @work(thread=True)
    def _run_query(self) -> None:
        data_table = self.query_one('#data_table', SortableDataTable)
        self.query_one(TabbedContent).active = "tab_data"
        with Loading(data_table):
            query = self._get_query()
            if query is None:
                self.logger.error('No search base specified.')
                return

            # fields = [xnat.search.SearchField(self.session.classes.SubjectData,
            #                                   'MR_COUNT',
            #                                   'integer')]
            # query = query.view(*fields)
            # val = query.to_string()

            try:
                query_result = query.tabulate_pandas().dropna(axis='columns', how='all')
                # self.query_result = (query.tabulate_pandas().dropna(axis='columns', how='all').
                #                      drop(columns=['project', 'quality', 'uid', 'quarantine_status'], errors='ignore'))
            except XNATResponseError as e:
                query_result = None
                status = _get_http_status_code(e)
                if status == http.HTTPStatus.FORBIDDEN:
                    self.logger.error('Server returned a "forbidden" error.')

        data_table.set_data(query_result)
        self.query_one('#xnat_plot', XnatPlot).set_data(query_result)

    @on(Button.Pressed, '#query_button')
    def run_query(self, _: Button.Pressed) -> None:
        self._run_query()

    def action_add_constraint(self) -> None:
        new_entry = \
            SearchEntry(fields=self.fields, id=self._get_next_id(self.query(SearchEntry).results(SearchEntry)))
        self.query_one('#query_input').mount(new_entry)
        new_entry.scroll_visible()

    @on(SearchEntry.Remove)
    def remove_constraint(self, entry: SearchEntry.Remove) -> None:
        if len(list(self.query(SearchEntry).results(SearchEntry))) == 1:
            return

        self.query_one(f'#{entry.id}', SearchEntry).remove()

    def action_load_search(self) -> None:
        self.push_screen(
            FileOpen('..', filters=Filters(('Searches', lambda p: p.suffix.lower() == '.json'))),
            callback=functools.partial(io.load_search, app=self))

    def action_save_search(self) -> None:
        self.push_screen(
            FileSave(filters=Filters(('Searches', lambda p: p.suffix.lower() == '.json'))),
            callback=functools.partial(io.save_search, app=self))

    def action_save_result(self) -> None:
        pass
        # data_table = self.query_one('#data_table', SortableDataTable)
        # self.push_screen(
        #     FileSave(),
        #     callback=functools.partial(io.save_result, query_result=data_table.data))

    def action_show_selections(self) -> None:
        self.query_one('#search_base_fields', Horizontal).toggle_class('remove')
