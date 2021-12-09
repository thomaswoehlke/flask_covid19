# PostgreSQL

## create user

````PostgreSQL
    CREATE ROLE flask_covid19 WITH
        LOGIN
        SUPERUSER
        CREATEDB
        CREATEROLE
        INHERIT
        REPLICATION
        CONNECTION LIMIT -1
        PASSWORD 'flask_covid19pwd';
    GRANT pg_execute_server_program, pg_monitor, pg_read_all_settings, pg_read_all_stats, pg_read_server_files, pg_signal_backend TO flask_covid19 WITH ADMIN OPTION;
````

## create tablespace

````PostgreSQL
    CREATE TABLESPACE tablespace_flask_covid19
      OWNER flask_covid19
      LOCATION '/opt/postgresql/tablespace_flask_covid19';

    ALTER TABLESPACE tablespace_flask_covid19
      OWNER TO flask_covid19;
````

## create database

flask_covid19

````PostgreSQL
    CREATE DATABASE flask_covid19
        WITH
        OWNER = flask_covid19
        TEMPLATE = template0
        ENCODING = 'UTF8'
        LC_COLLATE = 'de_DE.UTF-8'
        LC_CTYPE = 'de_DE.UTF-8'
        TABLESPACE = tablespace_flask_covid19
        CONNECTION LIMIT = -1;
````

flask_covid19_dev_branch_01

````PostgreSQL
    CREATE DATABASE flask_covid19_dev_branch_01
        WITH
        OWNER = flask_covid19
        TEMPLATE = flask_covid19
        ENCODING = 'UTF8'
        LC_COLLATE = 'de_DE.UTF-8'
        LC_CTYPE = 'de_DE.UTF-8'
        TABLESPACE = tablespace_flask_covid19
        CONNECTION LIMIT = -1;
````

flask_covid19_dev_branch_02

````PostgreSQL
    CREATE DATABASE flask_covid19_dev_branch_02
        WITH
        OWNER = flask_covid19
        TEMPLATE = flask_covid19
        ENCODING = 'UTF8'
        LC_COLLATE = 'de_DE.UTF-8'
        LC_CTYPE = 'de_DE.UTF-8'
        TABLESPACE = tablespace_flask_covid19
        CONNECTION LIMIT = -1;
````

flask_covid19_db_refactoring

````PostgreSQL
    CREATE DATABASE flask_covid19_db_refactoring
        WITH
        OWNER = flask_covid19
        TEMPLATE = flask_covid19
        ENCODING = 'UTF8'
        LC_COLLATE = 'de_DE.UTF-8'
        LC_CTYPE = 'de_DE.UTF-8'
        TABLESPACE = tablespace_flask_covid19
        CONNECTION LIMIT = -1;
````

flask_covid19_dev_data_import

````PostgreSQL
    CREATE DATABASE flask_covid19_dev_data_import
        WITH
        OWNER = flask_covid19
        TEMPLATE = flask_covid19
        ENCODING = 'UTF8'
        LC_COLLATE = 'de_DE.UTF-8'
        LC_CTYPE = 'de_DE.UTF-8'
        TABLESPACE = tablespace_flask_covid19
        CONNECTION LIMIT = -1;

````

flask_covid19_dev_frontend

````PostgreSQL
    CREATE DATABASE flask_covid19_dev_frontend
        WITH
        OWNER = flask_covid19
        TEMPLATE = flask_covid19
        ENCODING = 'UTF8'
        LC_COLLATE = 'de_DE.UTF-8'
        LC_CTYPE = 'de_DE.UTF-8'
        TABLESPACE = tablespace_flask_covid19
        CONNECTION LIMIT = -1;

````

flask_covid19_master

````PostgreSQL
    CREATE DATABASE flask_covid19_master
        WITH
        OWNER = flask_covid19
        TEMPLATE = flask_covid19
        ENCODING = 'UTF8'
        LC_COLLATE = 'de_DE.UTF-8'
        LC_CTYPE = 'de_DE.UTF-8'
        TABLESPACE = tablespace_flask_covid19
        CONNECTION LIMIT = -1;

````

flask_covid19_qa

````PostgreSQL
    CREATE DATABASE flask_covid19_qa
        WITH
        OWNER = flask_covid19
        TEMPLATE = flask_covid19
        ENCODING = 'UTF8'
        LC_COLLATE = 'de_DE.UTF-8'
        LC_CTYPE = 'de_DE.UTF-8'
        TABLESPACE = tablespace_flask_covid19
        CONNECTION LIMIT = -1;

````
