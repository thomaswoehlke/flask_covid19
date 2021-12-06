drop_table = "DROP TABLE IF EXISTS who_region CASCADE"
create_table = (
    "CREATE TABLE who_region ("
    "id SERIAL PRIMARY KEY,"
    "who_region VARCHAR(255) NOT NULL,"
    "UNIQUE (who_region)"
    ");"
)
