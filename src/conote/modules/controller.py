#!/usr/bin/env python3

import os
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import box
from rich.markdown import Markdown
from rich.panel import Panel
from conote.modules import MarkDownInit, NoteDataBase


class NoteCommandController(NoteDataBase, MarkDownInit):
    
    def __init__(self) -> None:
        NoteDataBase.__init__(self)
        MarkDownInit.__init__(self)

        self.dbase_dir = str(Path.home() / "Documents/CNotes")
          
        self.console = Console()

    
    def add(self, note):
        
        self.create_note(note)
        self.insert()



    def ls(self):

        table = Table(title='Notes List', box=box.HORIZONTALS, caption='END OF LIST', show_lines=False, header_style='red')

        table.add_column("ID", justify="right", style="red", no_wrap=True)
        table.add_column("NAME", justify="right", style="cyan", no_wrap=True)
        table.add_column("CREATED", justify="right", style="cyan", no_wrap=True)
                
        for record in self.select():         
            
            table.add_row(f'{record[0]}', f'{record[1]}', f'{record[2]}')

        return self.console.print(table)

    def rm(self, id: int):

        path = self.is_exists(id)

        if path:
            
           os.remove(path)
           self.drop(id)
                
           print('file sucsessfully deleted')

        else:
            
            print('not deleted')


    def cat(self, id: int):

        path = self.is_exists(id)

        if path:
            md = Markdown(self.read_file(path))
 
            return self.console.print(Panel(md, title=f'{path}', box=box.HORIZONTALS, expand=True))

    
    def is_exists(self, id: int):
        
        record: tuple = self.select(id=id)

        if record:
            
            file = "".join([record[1], '.md',])
        
            file_path = os.path.join(self.dbase_dir, file)
            if os.path.exists(file_path):
                return file_path
        else:
            return None
        
    def export(self):
        pass


if __name__ == '__main__':
    note = NoteCommandController()
    note.add('this is a test note !!!')
    note.ls()
    note.cat(4)
