import os
import logging
import pandas as pd
os.getcwd()

#os.system("pip install pandas")
#os.system("pip install scipy")
#os.system("pip install matplotlib")

### Daten einlesen #############################################################################
# csv-Datei direkt in einen DataFrame einlesen
who = pd.read_csv('flask_covid19/data/who/WHO.csv', sep=',')
who.info()         # grundlegende Informationen über den Datensatz
list(who.keys())
who.value_counts()
who.index
who.head()
who

library(DBI)
