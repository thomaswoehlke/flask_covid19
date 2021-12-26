# Database

## Oracle DB

### Documentation
* https://docs.oracle.com/en/database/oracle/oracle-database/19/administration.html
* https://localhost:5500/em

### create user

```sql
-- sqlplus '/ as sysdba'
create user flask_covid19 identified by flask_covid10tmp;
grant sysdba to flask_covid19;
grant all privileges to flask_covid19;
```
