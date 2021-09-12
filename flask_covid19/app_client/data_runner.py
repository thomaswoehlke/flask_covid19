#!/usr/bin/env python

import os
import pandas

from flask_covid19.data_all.all_config import BlueprintConfig


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
        self.data = pandas.read_csv(self.config.cvsfile_path, sep=self.config.separator)
        # grundlegende Informationen über den Datensatz
        self.data.info()
        list(self.data.keys())
        self.data.value_counts()
        self.data.index
        self.data.head()
        self.data
        return self
