#!/usr/bin/env python

import os
import pandas


class Owid:
  def __init__(self):
    print("owid")
    self.root_dir = os.getcwd()
    print("owid - root_dir: "+ self.root_dir)
    self.csv_file_path = self.root_dir + os.sep + 'data/owid/OWID.csv'
    print("owid - csv_file_path: "+ self.csv_file_path)

  def prepare(self):
    os.system("pip install pandas")
    os.system("pip install scipy")
    os.system("pip install matplotlib")
    return self
  
  def daten_einlesen(self):
    # csv-Datei direkt in einen DataFrame einlesen
    self.data = pandas.read_csv(self.csv_file_path, sep=',')
    self.data.info()        # grundlegende Informationen über den Datensatz
    list(self.data.keys())
    self.data.value_counts()
    self.data.index
    self.data.head()
    self.data
    return self
    

oo = Owid()
oo.prepare()
oo.daten_einlesen()
