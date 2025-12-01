#!/usr/bin/env python3

import os
from pathlib import Path
from datetime import datetime

import sqlite3

date_now_undercored:str = datetime.now().strftime("%Y_%m_%d")

dbase_dir = str(Path.home() / "Documents/CNotes")
os.makedirs(dbase_dir, exist_ok=True)
dbase = os.path.join(dbase_dir, 'note_base.db')

class NoteDataBase:

    def __init__(self) -> None:

        self.connect = sqlite3.connect(dbase)


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


    def insert(self):
        
        self._create()
        
        if self.is_record_exists:
            print('record is axists')
            pass

        else:
            query = "INSERT OR REPLACE INTO notes (name) VALUES (?)"
        
            return self.connection(query, (date_now_undercored,))


    def select(self, id: int | None = None) -> tuple | list:


        if id is None:
            
            query = "SELECT * FROM notes ORDER BY id"

            return self.connection(query).fetchall()

        query = "SELECT * FROM notes WHERE id = ?"


        return self.connection(query, (id,)).fetchone()

    def drop(self, id: int):
        
        query = "DELETE FROM notes WHERE id = ?"

        return self.connection(query, (id,))


    @property
    def is_record_exists(self):

        query = 'SELECT EXISTS(SELECT 1 FROM notes WHERE name = ?);'

        status = self.connection(query, (date_now_undercored,)).fetchone()[0]

        return bool(status)




if __name__ == '__main__':
    base = NoteDataBase()
    base.insert('2025_11_03')
    # base.insert('25_25_25')
    # s2 = dict(base.select(6))
    s = base.select() 

    print(type(s))
