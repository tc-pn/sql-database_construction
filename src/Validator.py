"""
Module used to validate the shape and content of the data at several key steps. 
Protocols and duck typing are used to facilitate reading comprehension and lighten management burdens when trying to scale
"""

from typing import Iterable, Iterator, Protocol

import pandas as pd

class Validator(Protocol):
    def __init__(self, data : pd.DataFrame):
        self.data = data

    def __call__(self, *args, **kwds):
        pass

class Rejector(Protocol):
    def __init__(self, data : pd.DataFrame):
        self.data = data

    def __call__(self, *args, **kwds):
        pass