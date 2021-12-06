update_data = (
    "insert into who_country(country_code, country,who_region_id) "
    "select distinct "
    "country_code, "
    "country, "
    "who_region.id as who_region_id "
    "from "
    "who_global_data_import, "
    "who_region "
    "group by country_code,country,who_region.id "
    "having (country_code) NOT IN ( "
    "    select country_code from who_country "
    ")"
)
