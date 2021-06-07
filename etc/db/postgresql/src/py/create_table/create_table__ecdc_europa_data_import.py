drop_table = "DROP TABLE IF EXISTS ecdc_europa_data_import CASCADE"
create_table = "CREATE TABLE ecdc_europa_data_import (" \
    "id SERIAL PRIMARY KEY," \
    "dateRep VARCHAR(255) NOT NULL," \
    "day VARCHAR(255) NOT NULL," \
    "month VARCHAR(255) NOT NULL," \
    "year VARCHAR(255) NOT NULL," \
    "cases VARCHAR(255) NOT NULL," \
    "deaths VARCHAR(255) NOT NULL," \
    "countriesAndTerritories VARCHAR(255) NOT NULL," \
    "geoId VARCHAR(255) NOT NULL," \
    "countryterritoryCode VARCHAR(255) NOT NULL," \
    "popData2019 VARCHAR(255) NOT NULL," \
    "continentExp VARCHAR(255) NOT NULL," \
    "Cumulative_number_for_14_days_of_COVID-19_cases_per_100000 VARCHAR(255) NOT NULL" \
    ");"
