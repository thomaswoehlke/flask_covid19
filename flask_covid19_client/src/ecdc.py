#!/usr/bin/env python

import os
import pandas


class Ecdc:
  def __init__(self):
    print("ecdc")
    self.root_dir = os.getcwd()
    print("ecdc - root_dir: "+ self.root_dir)
    self.csv_file_path = self.root_dir + os.sep + 'data/ecdc/ECDC.csv'
    print("ecdc - csv_file_path: "+ self.csv_file_path)

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
    

oo = Ecdc()
oo.prepare()
oo.daten_einlesen()

