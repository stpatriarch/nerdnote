import pytest
from nerdnote.modules.mdown import MarkDownInit


@pytest.fixture
def note(tmp_path):
    md = MarkDownInit(tmp_path)
    yield md, tmp_path

def test_create_note(note):

    md, tmp_path = note

    note_content = 'note for testing'
    file_path = tmp_path / "".join([md.file_name, '.md',]) 

    md.create_note(note_content)
    md.create_note(note_content)
    assert file_path.is_file()

def test_exporter(note):
    
    md, tmp_path = note

    note_content = 'note for testing'
    md.create_note(note_content)

    raw_md = md.read_file(md.note_path)

    md.exporter(md.note_path, raw_md, 'pdf')
    md.exporter(md.note_path, raw_md, 'html')
    
    file_path_pdf = tmp_path / "".join([md.file_name, '.pdf',]) 
    file_path_html = tmp_path / "".join([md.file_name, '.html',]) 

    assert file_path_pdf.is_file()
    assert file_path_html.is_file()


