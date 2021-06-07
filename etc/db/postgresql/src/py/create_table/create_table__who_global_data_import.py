drop_table = "DROP TABLE IF EXISTS who_global_data_import CASCADE"
create_table = "CREATE TABLE who_global_data_import (" \
                                       "id SERIAL PRIMARY KEY," \
                                       "Date_reported VARCHAR(255) NOT NULL," \
                                       "Country_code VARCHAR(255) NOT NULL," \
                                       "Country VARCHAR(255) NOT NULL," \
                                       "WHO_region VARCHAR(255) NOT NULL," \
                                       "New_cases VARCHAR(255) NOT NULL," \
                                       "Cumulative_cases VARCHAR(255) NOT NULL," \
                                       "New_deaths VARCHAR(255) NOT NULL," \
                                       "Cumulative_deaths VARCHAR(255) NOT NULL" \
                                       ");"
