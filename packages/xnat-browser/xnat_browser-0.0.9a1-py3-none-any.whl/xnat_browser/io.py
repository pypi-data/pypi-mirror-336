import dataclasses
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol, Any, cast, Optional

import pandas as pd
import xnat
from textual.css.query import QueryType
from textual.widgets import SelectionList, RadioSet, RadioButton

from xnat_browser.constants import QUERY_SELECTIONS


@dataclass
class Search:
    search_base: str = ''
    search_fields: list[str] = field(default_factory=list)
    constraints: list[tuple[str, Any, Any]] = field(default_factory=list)


class QueryProtocol(Protocol):
    # noinspection PyPropertyDefinition
    @property
    def fields(self) -> list[tuple[str, str]]:
        ...

    def set_query_constraints(self, constraints: list[xnat.search.Constraint]) -> None:
        ...

    def update_fields(self) -> None:
        ...

    def get_query_constraints(self) -> list[xnat.search.Constraint]:
        ...

    def query_one(self, selector: str, expect_type: type[QueryType]) -> QueryType:
        ...


def load_search(filename: Optional[Path], app: QueryProtocol) -> None:
    if filename is None:
        return

    with filename.open('r') as input_file:
        data = Search(**json.load(input_file))

    if len(data.search_base) > 0:
        search_base = data.search_base[:-4]
        radio_set = app.query_one('#root_element', RadioSet)
        for button in radio_set.query(RadioButton):
            if str(button.label) == search_base:
                button.value = True
                break

    if len(data.search_fields) > 0:
        search_fields = app.query_one('#selections', SelectionList)
        search_fields.deselect_all()
        for value in QUERY_SELECTIONS:
            if value.value in data.search_fields:
                search_fields.select(value)  # type: ignore

    app.update_fields()

    app.set_query_constraints([xnat.search.Constraint(*x) for x in data.constraints])


def save_search(filename: Optional[Path], app: QueryProtocol) -> None:
    if filename is None:
        return

    constraints = []
    for val in app.get_query_constraints():
        search_entry = next((x for x in app.fields if x[1] == val.identifier), None)
        if search_entry is None:
            continue
        constraints.append((search_entry[0], val.operator, val.right_hand))

    fields = app.query_one('#selections', SelectionList).selected
    base = str(app.query_one('#root_element', RadioSet).pressed_button.label) + 'Data'  # type: ignore

    with filename.open('w') as output_file:
        output_file.write(json.dumps(dataclasses.asdict(Search(base, cast(list[str], fields), constraints)),
                                     indent=4, sort_keys=True))


def save_result(filename: Optional[Path], query_result: pd.DataFrame | None) -> None:
    if filename is None or query_result is None:
        return

    if filename.suffix == '.csv':
        query_result.to_csv(filename, index=False)
        return

    if filename.suffix == '.xlsx':
        query_result.to_excel(filename, index=False)
        return
