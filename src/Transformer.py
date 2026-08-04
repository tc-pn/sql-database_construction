"""
Module used to normalize cleaned data, e.g., ensure that all numerical variables are float or int, and that all str are lowercase
Protocols and duck typing are used to facilitate reading comprehension and lighten management burdens when trying to scale
"""

from typing import Iterable, Iterator, Protocol

import pandas as pd

class Transformer(Protocol):
    def __init__(self, data : pd.DataFrame):
        self.data = data

    def __call__(self, *args, **kwds):
        pass