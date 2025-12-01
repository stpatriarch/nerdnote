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



class MarkDownInit(MdUtils, MarkDownFile):

    def __init__(self, file_name:str=date_now_undercored) -> None:

        self.note_path = os.path.join(NOTES, file_name)
        self.note_path_with_ext = self.note_path + '.md'

        super().__init__(file_name=self.note_path)

    
    def create_note(self, note: str) -> None:
        
        self.make_notes_directory

        if os.path.exists(self.note_path_with_ext):

            file_content = self.read_file(self.note_path)
        
            self.write(f"{time_now}", bold_italics_code='b')
            self.new_paragraph(f'{note}')

            with open(self.note_path_with_ext, 'w', encoding='utf-8') as f:
                f.write(file_content + self.get_md_text())
        
            
        else: 
            self.write(f'# {date_now}')
            self.write(' \n')
            self.write(f"{time_now}", bold_italics_code='b')
            self.new_paragraph(f'{note}')

            self.save



    @property
    def save(self):
        return self.create_md_file() 
    
    @property
    def make_notes_directory(self):
        os.makedirs(NOTES, exist_ok=True)


if __name__ == '__main__':
    m = MarkDownInit()
    m.create_note('note')
