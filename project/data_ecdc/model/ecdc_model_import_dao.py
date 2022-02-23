from datetime import date
from sqlalchemy.sql import text

from project.data.database import db, items_per_page
from project.data_all.model.all_model_mixins import AllImportMixin


class EcdcImportDao(AllImportMixin):

    @classmethod
    def count(cls):
        s = text(
            'select count(*) as number from ecdc_import_pandas'
        )
        return db.session.execute(s).first()

    @classmethod
    def find_by_datum(cls, datum: date):
        return cls.find_by_datum_str(datum)

    @classmethod
    def find_by_datum_str(cls, datum: date):
        s = text(
            'select * from ecdc_import_pandas where Date_reported = :day'
        )
        return db.session.execute(s, {"day": datum.isoformat()}).fetchall()

    @classmethod
    def find_by_datum_reported(cls, datum: date):
        return cls.find_by_datum(datum)

    @classmethod
    def get_datum_list(cls):
        s = text(
            'select "Date_reported" from ecdc_import_pandas'
            + ' group by "Date_reported" order by "Date_reported"'
        )
        return db.session.execute(s).fetchall()

    @classmethod
    def get_regions(cls):
        s = text(
            'select "WHO_region" from who_import_pandas '
            + 'group by "WHO_region" order by "WHO_region"'
        )
        return db.session.execute(s).fetchall()

    @classmethod
    def get_all_countries(cls):
        s = text(
            'select "Country","Country_code","WHO_region" from ecdc_import_pandas '
            + 'group by "Country","Country_code","WHO_region" '
            + 'order by "Country"'
        )
        return db.session.execute(s).fetchall()

    @classmethod
    def get_dates_reported(cls):
        return cls.get_datum_list()

    @classmethod
    def get_for_one_day(cls, day: str):
        s = text(
            'select * from ecdc_import_pandas where Date_reported = :day'
        )
        return db.session.execute(s, {"day": day}).fetchall()

    @classmethod
    def get_dates_reported_as_string_array(cls):
        return cls.get_datum_list()

    @classmethod
    def countries(cls):
        return cls.get_all_countries()

    @classmethod
    def get_datum_of_all_who_import(cls):
        return cls.get_datum_list()

    @classmethod
    def find_by_datum_and_country(cls, date_reported: str, country: str):
        s = text(
            'select * from ecdc_import_pandas '
            + 'where Date_reported = :day and Country = :country'
        )
        return db.session.execute(
            s, {"day": date_reported, "country": country}
        ).fetchall()

    @classmethod
    def get_by_datum_and_country(cls, date_reported: str, country: str):
        return cls.find_by_datum_and_country(date_reported, country)
