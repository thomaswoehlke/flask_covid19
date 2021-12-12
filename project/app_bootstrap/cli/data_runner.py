#!/usr/bin/env python
import os

import matplotlib as mpl
import numpy as np
import pandas as pd
import scipy as sp
import statsmodels as sm
from project.data_all.all_config import BlueprintConfig


class Runner:
    def __init__(self, cfg: BlueprintConfig):
        self.config = cfg
        print(self.config.category)
        print(self.config.category + " - csv_file_path: " + self.config.cvsfile_path)

    def prepare(self):
        os.system("pip install pandas")
        os.system("pip install scipy")
        os.system("pip install matplotlib")
        return self

    def daten_einlesen(self):
        # csv-Datei direkt in einen DataFrame einlesen
        self.data = pd.read_csv(
            self.config.cvsfile_path,
            sep=self.config.separator,
            index_col=0,
            parse_dates=True,
        )
        # grundlegende Informationen über den Datensatz
        print(self.data.info())
        print(list(self.data.keys()))
        print(self.data.value_counts())
        print(self.data.index)
        print(self.data.head())
        print(self.data)
        return self
