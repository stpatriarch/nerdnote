#!/usr/bin/env python3

from mdutils import MdUtils
from datetime import datetime, date

now:object = datetime.now()

# time only in two formats
tnow:str = now.strftime("%H:%M:%S")
tnow_undercored:str = now.strftime("%H_%M_%S")

# date only in two formats
dnow:str = now.strftime("%Y-%m-%d")
dnow_undercored:str = now.strftime("%Y_%m_%d")



class MarkDownInit(MdUtils):
    def __init__(self, file_name:str=dnow_undercored, title:str=tnow_undercored) -> None:
        super().__init__(file_name=file_name, title=title)


    def create(self) -> None:
        self.new_header(level=1, title=f'{dnow}')
        self.write(' \n')
        self.save



    @property
    def save(self):
        return self.create_md_file() 

