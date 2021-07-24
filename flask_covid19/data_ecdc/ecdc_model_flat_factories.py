
from data_ecdc.ecdc_model_flat import EcdcFlat


class EcdcFlatFactory:

    @classmethod
    def create_new(cls, d, row):
        oo = EcdcFlat(
            date_reported_import_str=d.date_reported_import_str,
            datum=d.datum,
            year=d.year,
            month=d.month,
            day_of_month=d.day_of_month,
            day_of_week=d.day_of_week,
            week_of_year=d.week_of_year,
            day_of_year=d.day_of_year,
            year_week=d.year_week,
            year_day_of_year=d.year_day_of_year,
            year_month=d.year_month,
            location=row['countriesAndTerritories'],
            location_group=row['continentExp'],
            location_code=row['countryterritoryCode'],
            processed_update=False,
            processed_full_update=False,
            #
            cases=int(row['cases']),
            deaths=int(row['deaths']),
            geo_id=row['geoId'],
            pop_data_2019=row['popData2019'],
            cumulative_number_for_14_days_of_covid19_cases_per_100000
            =0.0 if '' == row['Cumulative_number_for_14_days_of_COVID-19_cases_per_100000'] else float(row['Cumulative_number_for_14_days_of_COVID-19_cases_per_100000']),
        )
        return oo
