#!/usr/bin/env python3

from datetime import time
from .tool import color_messages, table_gen, time_stamps, PATH

stamps = time_stamps()
messages = color_messages()
tables = table_gen()

__all__ = ['messages', 'tables', 'stamps', 'PATH',]
