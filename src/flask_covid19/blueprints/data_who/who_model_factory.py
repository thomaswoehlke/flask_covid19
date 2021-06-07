from flask_covid19.blueprints.data_who.who_model_import import WhoImport
from flask_covid19.blueprints.data_who.who_model import WhoCountryRegion, WhoCountry, WhoDateReported, WhoData


class WhoCountryRegionFactory:

    @classmethod
    def create_new(cls, location_group_str: str):
        o = WhoCountryRegion(
            location_group=location_group_str,
            processed_update=False,
            processed_full_update=False,
        )
        return o


class WhoCountryFactory:

    @classmethod
    def create_new(cls, location: str, location_code: str, location_group: WhoCountryRegion):
        o = WhoCountry(
            location=location,
            location_code=location_code,
            location_group=location_group,
            processed_update=False,
            processed_full_update=False)
        return o


class WhoDataFactory:

    @classmethod
    def create_new(cls, my_who_import: WhoImport, my_date: WhoDateReported, my_country: WhoCountry):
        o = WhoData(
            cases_new=int(my_who_import.new_cases),
            cases_cumulative=int(my_who_import.cumulative_cases),
            deaths_new=int(my_who_import.new_deaths),
            deaths_cumulative=int(my_who_import.cumulative_deaths),
            date_reported=my_date,
            location=my_country,
            processed_update=False,
            processed_full_update=False
        )
        return o


