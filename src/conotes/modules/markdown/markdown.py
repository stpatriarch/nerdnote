#!/usr/bin/env python3

import os
from pathlib import Path
from mdutils import MdUtils
from mdutils.fileutils.fileutils import MarkDownFile
from datetime import datetime

NOTES = Path.home() / "Documents/CNotes"

now:object = datetime.now()

# time and date
date_now:str = now.strftime("%Y-%m-%d")
date_now_undercored:str = now.strftime("%Y_%m_%d")
time_now:str = now.strftime("%H:%M:%S")



class MarkDownInit(MdUtils):

    def __init__(self, file_name:str=date_now_undercored) -> None:

        self.note_path = str(NOTES / file_name)
        self.note_path_with_extension = str(NOTES / file_name) + '.md'

        super().__init__(file_name=self.note_path)

        self.md = MarkDownFile(dirname=self.note_path_with_extension)
    
    def create(self) -> None:
        if os.path.exists(self.note_path_with_extension):

            file_content = self.md.read_file(self.note_path_with_extension)
        
            self.new_header(level=2, title=f'{time_now}', add_table_of_contents='n')
            
            self.new_paragraph('Հայաստանի և Արցախի պետական լեզուն է։ Իր շուրջ հինգհազարամյա')

            with open(self.note_path_with_extension, 'w', encoding='utf-8') as f:
                f.write(file_content + self.get_md_text())
 
        else: 
            self.new_header(level=1, title=f'{date_now}')
            self.new_header(level=2, title=f'{time_now}')
            self.save
       



    @property
    def save(self):
        return self.create_md_file() 
    
    @property
    def make_notes_directory(self):
        os.makedirs(NOTES, exist_ok=True)


if __name__ == '__main__':
    m = MarkDownInit()
    m.make_notes_directory
    m.create()
