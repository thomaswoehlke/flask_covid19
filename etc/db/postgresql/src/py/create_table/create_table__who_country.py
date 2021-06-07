drop_table = "DROP TABLE IF EXISTS who_country CASCADE"
create_table = "CREATE TABLE who_country (" \
                            "id SERIAL PRIMARY KEY," \
                            "country_code VARCHAR(255) NOT NULL," \
                            "country VARCHAR(255) NOT NULL," \
                            "who_region_id integer REFERENCES who_region," \
                            "UNIQUE (country_code,country)" \
                            ");"
