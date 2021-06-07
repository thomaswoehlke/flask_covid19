update_data = "insert into who_global_data ( " \
                          "date_reported_id, " \
                          "country_id, " \
                          "new_cases, " \
                          "cumulative_cases, " \
                          "new_deaths, " \
                          "cumulative_deaths " \
                          ") " \
                          "select " \
                          "who_date_reported.id as date_reported_id, " \
                          "who_country.id as country_id, " \
                          "CAST (who_global_data_import.New_cases as integer) AS new_cases , " \
                          "CAST (who_global_data_import.Cumulative_cases as integer) as cumulative_cases, " \
                          "CAST (who_global_data_import.New_deaths as integer) as new_deaths, " \
                          "CAST (who_global_data_import.Cumulative_deaths as integer) as cumulative_deaths " \
                          "from " \
                          "who_global_data_import, " \
                          "who_date_reported, " \
                          "who_country " \
                          "where " \
                          "who_global_data_import.Country=who_country.country " \
                          "and " \
                          "who_global_data_import.Country_code = who_country.country_code " \
                          "and " \
                          "who_global_data_import.Date_reported = who_date_reported.date_reported "
