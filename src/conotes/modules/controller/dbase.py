#!/usr/bin/env python3

import os
from pathlib import Path

import sqlite3


dbase_dir = str(Path.home() / "Documents/CNotes")

dbase = os.path.join(dbase_dir, 'note_base.db')

class NoteDataBase:

    def __init__(self) -> None:

        self.connect = sqlite3.connect(dbase)


    def connection(self, content: str, values: tuple[str | int] | None = None) -> sqlite3.Cursor:
        
        with self.connect:
            self.connect.row_factory = sqlite3.Row
            cursor = self.connect.cursor()
            
            if values is None:
                cursor.execute(content)
            else:
                cursor.execute(content, values or [])

            return cursor

    def _create(self) -> sqlite3.Cursor:

        table = '''CREATE TABLE IF NOT EXISTS notes (

            id INTEGER PRIMARY KEY,
            name TEXT
        )'''

        return self.connection(table)


    def insert(self, date: str):
        
        self._create()

        query = "INSERT OR REPLACE INTO notes (name) VALUES (?)"
        
        return self.connection(query, (date,))

    def select(self, id: int | None = None):


        if id is None:

            query = "SELECT * FROM notes"
            return self.connection(query).fetchall()
        
        query = "SELECT * FROM notes WHERE id = ?"


        return self.connection(query, (id,)).fetchone()






if __name__ == '__main__':
    base = NoteDataBase()
    base._create()
    base.insert('25_25_25')
    s2 = dict(base.select(6))
    s = dict(base.select())
    print(s, s2)
