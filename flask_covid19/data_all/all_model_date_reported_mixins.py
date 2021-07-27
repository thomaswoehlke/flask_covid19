from datetime import date

from data_all.all_model_mixins import AllEntityMixin


class AllDateReportedMixin(AllEntityMixin):

    def get_name_for_weekday(self):
        pass

    def get_name_for_month(self):
        pass

    @classmethod
    def get_names_for_weekday(cls):
        pass

    @classmethod
    def get_names_for_months(cls):
        pass

    @classmethod
    def get_by_datum(cls, datum: date):
        pass

    @classmethod
    def get_by_date_reported(cls, date_reported_import_str: str):
        pass

    @classmethod
    def find_by_date_reported(cls, date_reported_import_str: str):
        pass

    @classmethod
    def find_by_year_week(cls, year_week: str):
        pass

    @classmethod
    def get_joungest_datum(cls):
        pass

    @classmethod
    def set_all_processed_update(cls):
        pass
