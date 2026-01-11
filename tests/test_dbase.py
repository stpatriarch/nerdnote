import pytest
from nerdnote.modules.dbase import NoteDataBase

@pytest.fixture
def base():
    db = NoteDataBase(database=":memory:")
    db.connection('''CREATE TABLE IF NOT EXISTS notes (

            id INTEGER PRIMARY KEY,
            name TEXT,
            created_date TEXT NOT NULL
        )''')
    db.connection("INSERT INTO notes (name, created_date) VALUES (?, ?)", (db.date_now_undercored, db.date_now))
    yield db
    db.connect.close()


def test_connection(base):

    db = base
    
    db.connection("INSERT INTO notes (name, created_date) VALUES (?, ?)", (db.date_now_undercored, db.date_now))

    result_one = db.connection("SELECT * FROM notes WHERE id = ?", (1,)).fetchone()
    result_all = db.connection("SELECT * FROM notes ORDER BY id").fetchall()

    assert result_one == (1, db.date_now_undercored, db.date_now)

    assert result_all == [(1, db.date_now_undercored, db.date_now), (2, db.date_now_undercored, db.date_now)]


def test_insert(base):
    db = base
    
    result = db.select()
    assert len(result) == 1


def test_select_all(base):
    db = base
    
    db.connection("INSERT INTO notes (name, created_date) VALUES (?, ?)", (db.date_now_undercored, db.date_now))
    
    result = db.select()
    assert len(result) == 2


def test_select_by_id(base):

    db = base
    
    result = db.select(1)
    assert result == [(1, db.date_now_undercored, db.date_now)]

def test_select_invalid_id(base):
    db = base

    result = db.select(2)

    assert result == []

def test_drop_confirm_yes(base, monkeypatch):
    db = base

    monkeypatch.setattr(
        "nerdnote.modules.dbase.Prompt.ask",
        lambda *args, **kwargs: "yes"
    )

    result = db.drop(1)

    assert result is not None
    assert db.select() == []


def test_drop_confirm_no(base, monkeypatch):
    db = base

    monkeypatch.setattr(
        "nerdnote.modules.dbase.Prompt.ask",
        lambda *args, **kwargs: "no"
    )

    result = db.drop(1)

    assert result == "REJECTATION"
    assert len(db.select()) == 1


def test_drop_missing_id(base):

    db = base

    result = db.drop(999)

    assert result == "REJECTATION"

def test_is_record_exists(base):

    db = base

    assert db.is_record_exists() is True
    
def test_is_record_exists_by_id(base):

    db = base

    assert db.is_record_exists(1) is True


def test_is_record_not_exists(base):

    db = base

    db.connection("DELETE FROM notes WHERE id = ?", (1,))


    assert db.is_record_exists() is False
   
def test_is_record_not_exists_by_id(base):

    db = base

    db.connection("DELETE FROM notes WHERE id = ?", (1,))

    assert db.is_record_exists(1) is False
