#!/usr/bin/env python3      

import os
from rich.console import Console
from rich import box
from rich.markdown import Markdown
from rich.panel import Panel
from nerdnote.modules import MarkDownInit, NoteDataBase
from nerdnote.modules.tools import PATH


class NoteCommandController(NoteDataBase, MarkDownInit):
    """
    Class manages CLI commands and binds the logic of
    other modules into a single class.
    """
    
    def __init__(self) -> None:

        self.note_mkdir
        NoteDataBase.__init__(self)
        MarkDownInit.__init__(self)
          
        self.console = Console()
        self.table = self.table_gen()


    def add(self, note: str) -> None:
        """
        The function transmits controls to create_note, which
        writes given notes into mardown file and
        inserts record into database.

        :param note: The note content entered by the user.
        :type note: str
        """
        
        self.create_note(note)
        self.insert()


    def ls(self) -> None:
        """
        The fucntion checks records alailability.

        if no records are found, it informs the user.
        if any records are found, it displays them in a table.

        """

        records = self.select()
        
        if not records:
            self.message_info.print('No records found for showing !')
            return

        if records:

            for record in records:         
            
                self.table.add_row(f'{record[0]}', f'{record[1]}', f'{record[2]}')

        return self.console.print(self.table)



    def rm(self, id: int) -> None:
        """
        The fuction performs record and file removing operations.

        Checks is operation not canceled by user.

        If file available and operation not canceled,
        it removes record and file from system.

        :param id: Record identification namber
        :type id: int
        """

        path = self.is_exists(id)

        if path is None:

            self.message_warn.print('removing !')
            return

        if  not self.drop(id):

            self.message_info.print('File not removed, canceled by user !')
            return

        if path:

            os.remove(path) 
            self.message_info.print('File successfully deleted')


    def cat(self, id: int) -> None:
        """
        The function renders a mardown content in terminal.

        if no record are found by given id, it informs the user.
        if record are found, it displays content in terminal.

        :param id: Record identification namber
        :type id: int
        """

        path = self.is_exists(id)

        if path:

            md = Markdown(self.read_file(path)) 
            return self.console.print(Panel(md, title=f'{path}', box=box.HORIZONTALS, expand=True))

        else:

            self.message_warn.print('showing !')


    def export(self, id: int, pattern: str) -> None:
        """
        The function converts mardown by given pattern.
        Availbale patterns are PDF and HTML.

        :param id: Record identification namber
        :type id: int
        :param pattern:
        :type pattern: str
        """


        path = self.is_exists(id)
        
        if path:

            file_name = path.split('.')[0]
            raw_md = self.read_file(path)
            self.exporter(path=file_name, raw_file=raw_md, pattern=pattern)

        else:

            self.message_warn.print('exportation !')
            
 
    def is_exists(self, id: int) -> str | None:
        """
        It checks file and record availablility.    
        If them exists give a file path,
        othervise it informs the user.

        :param id: Record identification namber
        :type id: int
        """
        
        record = self.select(id=id)

        if record:
            
            file = "".join([record[0][1], '.md',])
        
            file_path = os.path.join(PATH, file)
            if os.path.exists(file_path):
                return file_path

        else:

            self.message_warn.print('No files found for', end=' ')
            return

    @property
    def note_mkdir(self):
        """
        Makes directory in Documents, for containig...

        database file,
        mardown files,
        converted file.
        """
        os.makedirs(PATH, exist_ok=True)
