import pytest
from nerdnote.modules.controller import NoteCommandController
from nerdnote.modules import controller

@pytest.fixture
def control():
    nc = NoteCommandController()
    yield nc


def test_add(control, monkeypatch):

    calls = []
    
    note_content = 'notes for testing'

    def adding(note):
        calls.append(('create_note', note))
         
    def inserting():
        calls.append(('insert', None))
        
    monkeypatch.setattr(control, 'create_note', adding) 
    monkeypatch.setattr(control, 'insert', inserting) 
    
    control.add(note_content)

    assert calls == [
            ('create_note', note_content),
            ('insert', None)
            ]

def test_ls_no_record(control, monkeypatch):

    calls = []

    monkeypatch.setattr(control, 'select', lambda: []) 
    monkeypatch.setattr(control.message_info, 'print', lambda msg: calls.append(('print', msg)))
    
    control.ls()

    assert calls == [('print', 'No records found for showing !')]


def test_ls_records(control, monkeypatch):

    calls = []

    records = [
            (1, 'two', 'three'), 
            (4, 'five', 'six')]

    monkeypatch.setattr(control, 'select', lambda: records) 
    

    monkeypatch.setattr(control.table, 'add_row', lambda *args: calls.append(('row', args)))
    monkeypatch.setattr(control.console, 'print', lambda table: calls.append(('print', table)))
    
    control.ls()

    assert calls == [
            ('row', ('1', 'two', 'three')),
            ('row',('4', 'five', 'six')), 
            ('print', control.table)]


def test_rm_no_record(control, monkeypatch):

    calls = []

    monkeypatch.setattr(control, 'is_exists', lambda id: calls.append(('called', id)))
    monkeypatch.setattr(control.message_warn, 'print', lambda msg: calls.append(('print', msg)))
    
    control.rm(1)

    assert calls == [('called', 1), ('print', 'removing !')]


def test_rm_rejection(control, monkeypatch):

    calls = []

    monkeypatch.setattr(control, 'is_exists', lambda _: True)
    monkeypatch.setattr(control, 'drop', lambda _: "REJECTATION")
    monkeypatch.setattr(control.message_info, 'print', lambda msg: calls.append(('print', msg)))
    
    control.rm(1)

    assert calls == [('print', 'File not removed, canceled by user !')]


def test_rm_record(control, monkeypatch):

    calls = []

    monkeypatch.setattr(control, 'is_exists', lambda _: True)
    monkeypatch.setattr(control, 'drop', lambda _: False)
    monkeypatch.setattr(controller.os, 'remove', lambda msg: calls.append(('print', ("Remove_status", msg))))
    monkeypatch.setattr(control.message_info, 'print', lambda msg: calls.append(('print', msg)))
    
    control.rm(1)

    assert calls == [('print', ('Remove_status', True)), ('print', 'File successfully deleted')]


def test_cat_no_file_showing(control, monkeypatch):

    calls = []

    monkeypatch.setattr(control, 'is_exists', lambda id: calls.append(('called', id)))
    monkeypatch.setattr(control.message_warn, 'print', lambda msg: calls.append(('print', msg)))


    control.cat(1)

    assert calls == [('called', 1), ('print', 'showing !')]


def test_cat_file_showing(control, monkeypatch):

    calls = []

    monkeypatch.setattr(control, 'is_exists', lambda _: True)
    monkeypatch.setattr(control, 'read_file', lambda _: '# 2026-01-09 **23:34:49** note')
    monkeypatch.setattr(control.console, 'print', lambda panel: calls.append(('print', panel)))


    control.cat(1)

    assert len(calls) == 1
    assert calls[0][0] == 'print'
    assert isinstance(calls[0][1], controller.Panel)

def test_export_file(control, monkeypatch):

    calls = []

    monkeypatch.setattr(control, 'is_exists', lambda _: 'file.md')
    monkeypatch.setattr(control, 'read_file', lambda _: '# 2026-01-09 **23:34:49** note')
    monkeypatch.setattr(control, 'exporter', lambda path, raw_file, pattern: calls.append(('calls', (path, raw_file, pattern))))
    
    args = (1, 'pdf')
    control.export(*args)

    assert calls == [('calls', ('file', '# 2026-01-09 **23:34:49** note', 'pdf'))]

def test_no_file_export(control, monkeypatch):

    calls = []

    monkeypatch.setattr(control, 'is_exists', lambda _: False)
    monkeypatch.setattr(control.message_warn, 'print', lambda msg: calls.append(('print', msg)))

    args = (1, 'pdf')
    control.export(*args)

    assert calls == [('print', 'exportation !')]

def test_is_exists_record_exixts(control, monkeypatch):

    calls = []

    record = [['', 'file']]

    monkeypatch.setattr(control, 'select', lambda id: (calls.append(('calls', (id))), record)[1]) 
    monkeypatch.setattr(controller.os.path, 'join', lambda *args: (calls.append(('calls', (args))), 'file/path')[1])
    monkeypatch.setattr(controller.os.path, 'exists', lambda _: True) 

    control.is_exists(1)

    assert calls[1][1][1] == 'file.md'

def test_is_exists_no_founds_record(control, monkeypatch):

    calls = []

    monkeypatch.setattr(control, 'select', lambda id: (calls.append(('calls', (id))), None)[1]) 
    monkeypatch.setattr(control.message_warn, 'print', lambda *args, **kwargs: calls.append(('print', args, kwargs)))

    control.is_exists(1)

    assert calls[1][1]== ('No files found for',)


def test_note_mkdir(control, monkeypatch):

    calls = []

    monkeypatch.setattr(controller.os, 'makedirs', lambda path, exist_ok: calls.append((path, exist_ok)))
    
    control.note_mkdir


    assert calls == [(controller.PATH, True)]
