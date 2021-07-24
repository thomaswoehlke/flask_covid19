from data_ecdc.ecdc_model_import import EcdcImport


class EcdcImportFactory:

    @classmethod
    def create_new(cls, date_reported, d, row):
        o = EcdcImport(
            date_reported_import_str=d.date_reported_import_str,
            datum=d.datum,
            processed_update=False,
            processed_full_update=False,
            date_rep=date_reported,
            day=row['day'],
            month=row['month'],
            year=row['year'],
            cases=row['cases'],
            deaths=row['deaths'],
            countries_and_territories=row['countriesAndTerritories'],
            geo_id=row['geoId'],
            country_territory_code=row['countryterritoryCode'],
            pop_data_2019=row['popData2019'],
            continent_exp=row['continentExp'],
            cumulative_number_for_14_days_of_covid19_cases_per_100000
            =row['Cumulative_number_for_14_days_of_COVID-19_cases_per_100000'],
        )
        return o
