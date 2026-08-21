"""
Module used to clean data and quarantine problematic rows, files (e.g., incomplete data, rows, columns, mispelling)...
each class implements a rule that the data must follow for maximum normalization of format
they are a duck type of the Cleaner class
"""

from typing import Iterable, Iterator, Protocol

import pandas as pd

from Context import Context

class Cleaner(Protocol):
    """Cleaning model"""
    def __init__(self, context : Context):
        self.context = context

    def __call__(self, *args, **kwds) -> Context:
        pass

class LowercaseColumns:
    """
    This class converts all columns into strings 
    and forces the resulting values into lowercase
    """
    def __init__(self, context : Context):
        self.context = context

    def __call__(self) -> Context:
        df = self.context.data.copy()
        for column in df.columns:
            df[column] = df[column].astype(str).str.lower()
        self.context.data = df
        return self.context

class TrimWhiteSpace:
    """
    This class converts all columns into strings 
    and trims the resulting values of any spurious whitespace
    """
    def __init__(self, context : Context):
        self.context = context

    def __call__(self) -> Context:
        df = self.context.data.copy()
        for column in df.columns:
            df[column] = df[column].astype(str).str.strip()
        self.context.data = df
        return self.context

class ConvertDateToTimeStamp:
    """
    This class converts all indicated columns upon instanciation into 
    a datetime object, forcing the format to be YYYY-MM-DD
    If a value can't be read like this it produces a NaT
    """
    def __init__(self, context : Context, columns : list[str]):
        self.context = context
        self.columns = columns

    def __call__(self):
        df = self.context.data.copy()
        df[self.columns] = pd.to_datetime(df[self.columns], format="%Y-%m-%d", 
                                          errors="coerce")
        self.context.data = df
        return self.context

class RejectDuplicates:
    def __init__(self, context : Context):
        self.context = context

    def __call__(self) -> Context:
        df = self.context.data.copy()
        df = df[~df.astype(str).duplicated()]
        self.context.data = df

        #TODO : développer l'idée d'un objet contenant les informations, 
        # volumes par rapport au total, types etc des rows dupliquées

        return self.context


    

    



        