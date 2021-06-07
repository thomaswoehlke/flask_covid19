update_data = "insert into who_region (who_region) " \
                     "select distinct who_region from who_global_data_import " \
                     "group by who_region " \
                     "having who_global_data_import.WHO_region NOT IN ( " \
                     "    select who_region from who_region " \
                     ") order by who_global_data_import.WHO_region"
