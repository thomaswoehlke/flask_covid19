from flask_covid19.blueprints.data_who.who_model_import import WhoFlat, WhoImport


class WhoFlatFactory:

    @classmethod
    def create_new(cls, date_reported, d, row, my_data):
        oo = WhoFlat(
            datum=d.datum,
            year=d.year,
            month=d.month,
            day_of_month=d.day_of_month,
            day_of_week=d.day_of_week,
            week_of_year=d.week_of_year,
            day_of_year=d.day_of_year,
            year_week=d.year_week,
            year_day_of_year=d.year_day_of_year,
            date_reported_import_str=d.date_reported_import_str,
            year_month=d.year_month,
            location_code=row['Country_code'],
            location=row['Country'],
            location_group=row['WHO_region'],
            processed_update=False,
            processed_full_update=False,
            #
            new_cases=my_data['new_cases'],
            cumulative_cases=my_data['cumulative_cases'],
            new_deaths=my_data['new_deaths'],
            cumulative_deaths=my_data['cumulative_deaths'],
            country_code=row['Country_code'],
            country=row['Country'],
            who_region=row['WHO_region'],
            date_reported=date_reported,
        )
        return oo


class WhoImportFactory:

    @classmethod
    def create_new(cls, date_reported, d, row):
        o = WhoImport(
            new_cases=row['New_cases'],
            cumulative_cases=row['Cumulative_cases'],
            new_deaths=row['New_deaths'],
            cumulative_deaths=row['Cumulative_deaths'],
            country_code=row['Country_code'],
            country=row['Country'],
            who_region=row['WHO_region'],
            date_reported=date_reported,
            datum=d.datum,
            date_reported_import_str=date_reported,
            processed_update=False,
            processed_full_update=False,
        )
        return o
