from nerdnote.modules.tools.tool import DecoMixin
from rich.table import Table
from rich import box
import pytest


@pytest.fixture
def deco():
    dm = DecoMixin()
    yield dm


def test_table_gen(deco):
    
    table = deco.table_gen()

    headers = [column.header for column in table.columns]
    styles = [column.style for column in table.columns]
    justify = set(column.justify for column in table.columns)
    no_wrap = set(column.no_wrap for column in table.columns)


    assert isinstance(table, Table)
    assert table.title == 'Notes List'
    assert table.box == box.HORIZONTALS
    assert table.caption == 'END OF LIST'
    assert table.show_lines is False
    assert table.header_style == 'red'
    assert headers == ['ID', 'NAME', 'CREATED']
    assert styles == ['red', 'cyan', 'cyan']
    assert len(justify) == 1
    assert len(no_wrap) == 1
