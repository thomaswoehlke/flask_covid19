import os
import logging
import pandas as pd
os.getcwd()

#os.system("pip install pandas")
#os.system("pip install scipy")
#os.system("pip install matplotlib")

### Daten einlesen #############################################################################
# csv-Datei direkt in einen DataFrame einlesen
who = pd.read_csv('../data/who/WHO.csv', sep=',')
who.info()         # grundlegende Informationen über den Datensatz
b = list(who.keys())
print(b)
print(who.value_counts())
print(who.index)
print(who.head())
print(who)

