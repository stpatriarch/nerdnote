#!/usr/bin/env python3

import os
from rich.prompt import Prompt
from nerdnote.modules.tools import PATH, DecoMixin


import sqlite3


DATABASE = os.path.join(PATH, 'note_base.db')

class NoteDataBase(DecoMixin):
    """
    Responsible for any CRUD like interactions with the database.

    """

    def __init__(self) -> None:

        self.connect = sqlite3.connect(DATABASE)
        super().__init__()


    def connection(self, content: str, values: tuple[str | int] | tuple[str, str] | None = None) -> sqlite3.Cursor:
        """
        Performs operations assosiated with read and write to DB.

        :param content: Perfroms a database query.
        :type content: str
        :param values: Optional data to be written to the database.
        :type values: tuple | None
        :return: Cursor object resulting from the executed query.
        """      
        with self.connect:

            cursor = self.connect.cursor()
            
            if values is None:
                cursor.execute(content)

            else:
                cursor.execute(content, values)

            return cursor

    def _create(self) -> sqlite3.Cursor:
        """
        Creates a db table in connected database

        :return: Cursor object resulting from the executed query.

        """

        table = '''CREATE TABLE IF NOT EXISTS notes (

            id INTEGER PRIMARY KEY,
            name TEXT,
            created_date TEXT NOT NULL
        )'''

        return self.connection(table)


    def insert(self) -> None | sqlite3.Cursor:
        """
        The execution of the _create function and inserts a data to database.

        :return: Cursor object resulting from the executed query.
        """
        
        self._create()
        
        if self.is_record_exists():
            self.message_info.print('Your thoughts are supplemented!')
            pass

        else:
            query = "INSERT OR REPLACE INTO notes (name, created_date) VALUES (?, ?)"
        
            return self.connection(query, (self.date_now_undercored, self.date_now))


    def select(self, id: int | None = None) -> list[tuple[int, str, str]] | None:
        """
        Checks are database not empty and select data from connected database.

        :param id: Id of record to fetch from the database.
        :type id: int | None

        :return: list of records or do operations with target id.
        """

        if os.path.getsize(DATABASE) == 0:

            self.message_info.print('No Data file has detected. Try adding some notes')
            return
        
        if id is None:
            
            query = "SELECT * FROM notes ORDER BY id"

            return self.connection(query).fetchall()

        query = "SELECT * FROM notes WHERE id = ?"

        record = self.connection(query, (id,)).fetchone()

        return [] if record is None else [record]


    def drop(self, id: int) -> str | sqlite3.Cursor | None:
        """
        Delete record from database by id.

        :param id: Id of record to delete from the database.
        :type id: int

        :return: Cursor object resulting from the executed query.
        """       

        query = "DELETE FROM notes WHERE id = ?"

        if self.is_record_exists(id):
        
            confirm = Prompt.ask(f'DELETE note by id: {id} Continue( yes | no)?', console=self.message_warn)

            if confirm in ('yes', 'YES', 'y', 'Y', ):

                return self.connection(query, (id,))
            else:

                return 'REJECTATION'
        else:

            return 'REJECTATION'


    def is_record_exists(self, id: int | None = None) -> bool:
        """
        Checks is record exists in database.

        :return: Status of the record as a boolean.
        """

        if id is None:

            query = 'SELECT EXISTS(SELECT 1 FROM notes WHERE name = ?);'
             
            status = self.connection(query, (self.date_now_undercored,)).fetchone()[0]

        else:
            query = 'SELECT EXISTS(SELECT 1 FROM notes WHERE id = ?);'

            status = self.connection(query, (id,)).fetchone()[0]
        
        return bool(status)
