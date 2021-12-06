drop_table = "DROP TABLE IF EXISTS who_date_reported CASCADE"
create_table = (
    "CREATE TABLE who_date_reported ("
    "id SERIAL PRIMARY KEY,"
    "Date_reported VARCHAR(255) NOT NULL,"
    "UNIQUE (Date_reported)"
    ");"
)
