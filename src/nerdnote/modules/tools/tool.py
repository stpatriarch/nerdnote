#!/usr/bin/env python3

import os
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import box
from datetime import datetime
from collections import namedtuple

PATH = os.path.join(Path.home(),"Documents/CNotes")

def time_stamps():

    now:object = datetime.now()
 
    time_stp = namedtuple('time_stp', ['date_now', 'date_now_undercored', 'time_now'])
    
    stamps = time_stp(
            now.strftime("%Y-%m-%d"), 
            now.strftime("%Y_%m_%d"), 
            now.strftime("%H:%M:%S"))

    return stamps

def table_gen():

    table = Table(title='Notes List', box=box.HORIZONTALS, caption='END OF LIST', show_lines=False, header_style='red')

    table.add_column("ID", justify="right", style="red", no_wrap=True)
    table.add_column("NAME", justify="right", style="cyan", no_wrap=True)
    table.add_column("CREATED", justify="right", style="cyan", no_wrap=True)                
     
    return table


def color_messages():
    

    message = namedtuple('message', ['confirm', 'info',])
    messages = message(
            Console(style='red bold'), 
            Console(style='green bold'))

    return messages

if __name__ == '__main__':
    t = time_stamps()
    print(t.date_now)
    print(t.date_now_undercored)
    print(t.time_now)
