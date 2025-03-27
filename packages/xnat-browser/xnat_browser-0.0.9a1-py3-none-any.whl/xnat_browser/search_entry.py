from dataclasses import dataclass, astuple
from typing import Any, cast, Optional

import xnat
import xnat.core
from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Select, Input, Button

from xnat_browser.constants import OPERATOR_OPTIONS


@dataclass(frozen=True)
class SearchField:
    name: str
    identifier: str

    @staticmethod
    def __convert(name: str) -> str:
        return name.replace('_', '').casefold()

    def __eq__(self, other: object) -> bool:
        return self.__convert(self.name) == self.__convert(cast(SearchField, other).name)

    def __hash__(self) -> int:
        return hash(self.__convert(self.name))


class SearchConstraintError(RuntimeError):
    ...


class SearchEntry(Widget):
    """Search entry widget. Consists of a search field, operator and value."""
    DEFAULT_CSS = """
    SearchEntry {
        height: 3;
    }
    SearchEntry Input {
        width: 1fr;
    }
    
    #search_remove {
        max-width: 5;
    }
    
    .search_field{
        min-width: 45;
        width: 1fr;
    }
    .search_operator {
        width: 15;
    }
    """

    class Remove(Message):
        def __init__(self, _id: Optional[str]) -> None:
            self.id = _id
            super().__init__()

    def __init__(self, fields: list[tuple[str, str]], *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields = fields

    def compose(self) -> ComposeResult:
        with Horizontal(id='horizontal'):
            yield Button(label=Text('X', style='bold'), id='search_remove')
            yield Select(self.fields, id='field', classes='search_field')
            yield Select(OPERATOR_OPTIONS, id='operator', classes='search_operator')
            yield Input(id='value', placeholder='Value...')

    def update_fields(self, fields: list[tuple[str, str]]) -> None:
        self.query_one('#field', Select).set_options(fields)

    @on(Button.Pressed, '#search_remove')
    def remove_constraint(self, _: Button.Pressed) -> None:
        self.post_message(self.Remove(self.id))

    @property
    def constraint(self) -> None | xnat.search.Constraint:
        identifier = self.query_one('#field', Select).value
        operator = self.query_one('#operator', Select).value
        value = self.query_one('#value', Input).value
        if identifier is None or operator is None:
            return None

        return xnat.search.Constraint(identifier, operator, value)

    @constraint.setter
    def constraint(self, data: xnat.search.Constraint) -> None:
        search_entry = next((x for x in self.fields if x[0] == data.identifier), None)
        if search_entry is None:
            raise SearchConstraintError(f'Could not find search_entry: {data.identifier}')

        self.query_one('#field', Select).value = search_entry[1]
        self.query_one('#operator', Select).value = data.operator
        self.query_one('#value', Input).value = data.right_hand


# noinspection PyPep8Naming
def get_search_terms(classes: list[xnat.core.XNATBaseObject]) -> dict[Any, list[str]]:
    search_fields = {}
    for xnat_type in classes:
        search_fields[xnat_type] = \
            [x for x in dir(xnat_type) if isinstance(getattr(xnat_type, x), xnat.search.BaseSearchField)]

    return search_fields


def get_select_fields(search_terms: dict[Any, list[str]]) -> list[tuple[str, str]]:
    fields: set[SearchField] = set()
    for xnat_type, search_fields in search_terms.items():
        # noinspection PyProtectedMember
        # pylint: disable=protected-access
        new_fields = {SearchField(name=x.casefold(), identifier=f'{xnat_type._XSI_TYPE}/{x}') for x in search_fields}
        fields.update(new_fields)
        # pylint: enable=protected-access
    return [cast(tuple[str, str], astuple(x)) for x in sorted(fields, key=lambda x: x.name.casefold())]
