#!/usr/bin/env python

import os
import pandas


class Vaccination:
  def __init__(self):
    print("vaccination")
    self.root_dir = os.getcwd()
    print("vaccination - root dir: " + self.root_dir)
    self.tsv_file_path = self.root_dir + os.sep + 'data/vaccination/Vaccination.tsv'
    print("vaccination - tsv_file_path: " + self.tsv_file_path)
    
  def prepare(self):
    os.system("pip install pandas")
    os.system("pip install scipy")
    os.system("pip install matplotlib")
    return self
  
  def daten_einlesen(self):
    # csv-Datei direkt in einen DataFrame einlesen
    self.data = pandas.read_csv(self.tsv_file_path, sep='\t')
    self.data.info()         # grundlegende Informationen über den Datensatz
    list(self.data.keys())
    self.data.value_counts()
    self.data.index
    self.data.head()
    self.data
    return self
    

oo = Vaccination()
oo.prepare()
oo.daten_einlesen()

