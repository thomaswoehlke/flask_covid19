# install.packages("DBI")
# install.packages('RODBCDBI')
# install.packages("dbplyr")
# install.packages('tibble')
# install.packages('shiny')
# install.packages('pool')
# install.packages('RMySQL')
# install.packages('RPostgreSQL')
# install.packages('RSQLite')
# install.packages('RMySQL')
# install.packages("RMariaDB")


library(DBI)
library(RODBCDBI)
library(tibble)

library(shiny)
library(dplyr)
library(pool)

library(odbc)
library(RMariaDB)

# sort(unique(odbcListDrivers()[[1]]))

con <- dbConnect(odbc::odbc(), .connection_string = "Driver={MariaDB Unicode};DB={flask_covid19_rki},Server={localhost},UID={flask_covid19},PWD={flask_covid19pwd},Port=3306",timeout=10)

q = dbGetQuery(con,"select * from rki_import_flat where landkreis = 'SK Bochum' order by meldedatum__datum desc")

