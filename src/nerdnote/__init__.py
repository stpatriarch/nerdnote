#!/usr/bin/env python3

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version('nerdnote')
except PackageNotFoundError:
    __version__ = "\"_\""

__title__ = "nerdnote"
__description__ = "Note taking tool from console."
__url__ = "https://github.com/stpatriarch/nerdnote"

__author__ = "stpatriarch"
__author_email__ = "chinaryannarek@gmail.com"
__license__ = "MIT"
