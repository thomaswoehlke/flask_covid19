from data_who.who_model_import import WhoImport


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
