#!/usr/bin/env python3

import os
from rich.prompt import Prompt
from nerdnote.modules.tools import PATH, messages, stamps

import sqlite3


DATABASE = os.path.join(PATH, 'note_base.db')

class NoteDataBase:

    def __init__(self) -> None:

        self.connect = sqlite3.connect(DATABASE)



    def connection(self, content: str, values: tuple[str | int] | None = None) -> sqlite3.Cursor:
        
        with self.connect:

            cursor = self.connect.cursor()
            
            if values is None:
                cursor.execute(content)
            else:
                cursor.execute(content, values)

            return cursor

    def _create(self) -> sqlite3.Cursor:

        table = '''CREATE TABLE IF NOT EXISTS notes (

            id INTEGER PRIMARY KEY,
            name TEXT,
            created_date DATE DEFAULT (DATE('now')) NOT NULL
        )'''

        return self.connection(table)


    def insert(self) -> None | sqlite3.Cursor:
        
        self._create()
        
        if self.is_record_exists:
            messages.info.print('Your thoughts are supplemented!')
            pass

        else:
            query = "INSERT OR REPLACE INTO notes (name) VALUES (?)"
        
            return self.connection(query, (stamps.date_now_undercored,))


    def select(self, id: int | None = None) -> tuple | list:

        if os.path.getsize(DATABASE) == 0:
            
           return messages.info.print('No Data file has detected. Try adding some notes')

        if id is None:
            
            query = "SELECT * FROM notes ORDER BY id"

            return self.connection(query).fetchall()

        query = "SELECT * FROM notes WHERE id = ?"

        return self.connection(query, (id,)).fetchone()


    def drop(self, id: int) -> sqlite3.Cursor:
        
        query = "DELETE FROM notes WHERE id = ?"
        
        confirm = Prompt.ask(f'DELETE note by id: {id} Continue( yes | no)?', console=messages.confirm)

        if confirm in ('yes', 'YES', 'Y', 'y',):

            return self.connection(query, (id,))

        else:
            return None

    @property
    def is_record_exists(self) -> bool:

        query = 'SELECT EXISTS(SELECT 1 FROM notes WHERE name = ?);'

        status = self.connection(query, (stamps.date_now_undercored,)).fetchone()[0]

        return bool(status)




if __name__ == '__main__':
    base = NoteDataBase()
    base.insert('2025_11_03')
    # base.insert('25_25_25')
    # s2 = dict(base.select(6))
    s = base.select() 

    print(type(s))
