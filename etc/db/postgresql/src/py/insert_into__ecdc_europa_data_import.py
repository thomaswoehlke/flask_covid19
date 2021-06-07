update_data = "INSERT INTO ecdc_europa_data_import (" \
"dateRep," \
"day," \
"month," \
"year," \
"cases," \
"deaths," \
"countriesAndTerritories," \
"geoId," \
"countryterritoryCode," \
"popData2019," \
"continentExp," \
"Cumulative_number_for_14_days_of_COVID19_cases_per_100000" \
") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" \
"RETURNING idRETURNING id"
