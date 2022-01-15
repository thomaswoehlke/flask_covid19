from project.data_ecdc.model.ecdc_model_date_reported import EcdcDateReported
from project.data_ecdc.model.ecdc_model_data import EcdcData
from project.data_ecdc.model.ecdc_model_import import EcdcImport
from project.data_ecdc.model.ecdc_model_location import EcdcCountry
from project.data_ecdc.model.ecdc_model_location_group import EcdcContinent


class EcdcImportFactory:
    @classmethod
    def create_new(cls, date_reported, d, row):
        o = EcdcImport(
            date_reported_import_str=d.date_reported_import_str,
            datum=d.datum,
            processed_update=False,
            processed_full_update=False,
            date_rep=date_reported,
            day=row["day"],
            month=row["month"],
            year=row["year"],
            cases=row["cases"],
            deaths=row["deaths"],
            countries_and_territories=row["countriesAndTerritories"],
            geo_id=row["geoId"],
            country_territory_code=row["countryterritoryCode"],
            pop_data_2019=row["popData2019"],
            continent_exp=row["continentExp"],
            cumulative_number_for_14_days_of_covid19_cases_per_100000=row[
                "Cumulative_number_for_14_days_of_COVID-19_cases_per_100000"
            ],
        )
        return o


class EcdcDataFactory:
    @classmethod
    def create_new(
        cls,
        my_deaths: int,
        my_cases: int,
        my_cumulative_number: float,
        date_reported: EcdcDateReported,
        location: EcdcCountry,
    ):
        o = EcdcData(
            location=location,
            date_reported=date_reported,
            deaths=int(my_deaths),
            cases=int(my_cases),
            cumulative_number_for_14_days_of_covid19_cases_per_100000=0.0
            if "" == my_cumulative_number
            else float(my_cumulative_number),
            processed_update=False,
            processed_full_update=False,
        )
        return o
