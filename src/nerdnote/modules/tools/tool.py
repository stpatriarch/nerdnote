#!/usr/bin/env python3

import os
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import box
from datetime import datetime

PATH = os.path.join(Path.home(),"Documents/CNotes")

class DecoMixin:
    """
    Class contains date and time stamps,
    informative and warning messages and
    generates table body.
    """

    def __init__(self) -> None:
        
    
        now:object = datetime.now()

        self.date_now = now.strftime("%Y-%m-%d")
        self.date_now_undercored = now.strftime("%Y_%m_%d")
        self.time_now = now.strftime("%H:%M:%S")
        self.message_warn = Console(style='red bold')
        self.message_info = Console(style='green bold')

    @staticmethod
    def table_gen() -> Table:
        """
        The fucntion generate a table by ginven attributes.
        """
        table = Table(title='Notes List', box=box.HORIZONTALS, caption='END OF LIST', show_lines=False, header_style='red')

        table.add_column("ID", justify="right", style="red", no_wrap=True)
        table.add_column("NAME", justify="right", style="cyan", no_wrap=True)
        table.add_column("CREATED", justify="right", style="cyan", no_wrap=True)                
     
        return table
