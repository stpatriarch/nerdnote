#!/usr/bin/env python3      

import os
from pathlib import Path
from sys import path_importer_cache
from rich.console import Console
from rich.table import Table
from rich import box
from rich.markdown import Markdown
from rich.panel import Panel
from conote.modules import MarkDownInit, NoteDataBase
from conote.modules.tools import PATH, stamps, messages, tables

NOTE_DIR = Path.home() / "Documents/CNotes"

class NoteCommandController(NoteDataBase, MarkDownInit):
    
    def __init__(self) -> None:

        self.note_mkdir
        NoteDataBase.__init__(self)
        MarkDownInit.__init__(self)

        self.dbase_dir = str(Path.home() / "Documents/CNotes")
          
        self.console = Console()

    
    def add(self, note) -> None:
        
        self.create_note(note)
        self.insert()


    def ls(self) -> None:

        path = self.select()

        if path:

            for record in self.select():         
            
                tables.add_row(f'{record[0]}', f'{record[1]}', f'{record[2]}')

        return self.console.print(tables)



    def rm(self, id: int) -> None:

        path = self.is_exists(id)

        if path and self.drop(id) is not None:
            
           os.remove(path)
                
           messages.info.print('file sucsessfully deleted')

        else:
            
            print('not deleted')


    def cat(self, id: int):

        path = self.is_exists(id)

        if path:
            md = Markdown(self.read_file(path))
 
            return self.console.print(Panel(md, title=f'{path}', box=box.HORIZONTALS, expand=True))

        else:
            print('No note files for showing')

    
    def is_exists(self, id: int) -> str | None:
        
        record: tuple = self.select(id=id)

        if record:
            
            file = "".join([record[1], '.md',])
        
            file_path = os.path.join(PATH, file)
            if os.path.exists(file_path):
                return file_path
        else:
            return None
        

    def export(self, id: int, pattern: str) -> None:

        path = self.is_exists(id)
        
        if path:
            file_name = path.split('.')[0]

            raw_md = self.read_file(path)

            self.exporter(path=file_name, raw_file=raw_md, pattern=pattern)

        else:
            print('file note exists')

    @property
    def note_mkdir(self):
        os.makedirs(PATH, exist_ok=True)

if __name__ == '__main__':
    note = NoteCommandController()
    note.add('this is a test note !!!')
    note.ls()
    note.cat(4)
