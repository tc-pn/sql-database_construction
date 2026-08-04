"""
Module used to load csv files, with some internal validation steps
"""

from typing import Iterable, Iterator

from abc import ABC, abstractmethod

import pathlib

import pandas as pd

class Loader(ABC):
    def __init__(self, path_rep : pathlib.Path, filename : str, sep : str=";"):
        super().__init__()
        self.path_rep = path_rep.absolute()
        self.filename = filename
        self.sep = sep

    @abstractmethod
    def __call__(self, *args, **kwds):
        pass

class CSVLoader(Loader):
    def __call__(self) -> pd.DataFrame:
        path = self.path_rep / self.filename

        self.err_management(path)

        data = pd.read_csv(path, sep=self.sep)
        return data

    def err_management(self, path : pathlib.Path):
        if path.suffix.lower() != ".csv":
            err_msg = f"File {path.name} is not a csv file"
            raise ValueError(err_msg)

        if not path.exists():
            err_msg = f"This file does not exist : {str(path)}"
            raise FileNotFoundError(err_msg)

# might be interesting as an exercise to introduce an abstraction of CSVFilesLoader, and then on top of it construct an object able to load a list of mixed files extensions 

class CSVFilesLoader():
    def __init__(self, path_rep, filenames : Iterable[str], seps : Iterable[str]):
        self.path_rep = path_rep.absolute()
        self.filenames = filenames
        self.seps = seps

    def __call__(self) -> Iterator[pd.DataFrame]:
        return (CSVLoader(path_rep=self.path_rep, filename=filename, sep=sep)() 
                for filename, sep in zip(self.filenames, self.seps))

