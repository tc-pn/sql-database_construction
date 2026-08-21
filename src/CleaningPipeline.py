"""
Ce module sert d'orchestrateur de l'ensemble des travaux de nettoyage de la donnée
Il fonctionne par composition des objets du module Cleaner.py
"""
# numerics
import pandas as pd

from Context import Context
from Cleaner import Cleaner

class CleaningPipeline:
    def __init__(self, context : Context, steps : list[Cleaner]):
        self.context = context
        self.steps = steps

    def __call__(self):
        for step in self.steps:
            context = step()
        return context