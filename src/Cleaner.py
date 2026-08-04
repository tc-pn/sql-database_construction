"""
Module used to clean data and quarantine problematic rows, files (e.g., incomplete data, rows, columns, mispelling)...
"""

from typing import Iterable, Iterator, Protocol

import pandas as pd

class Cleaner(Protocol):
    def __init__(self, data : pd.DataFrame):
        self.data = data

    def __call__(self, *args, **kwds):
        pass

