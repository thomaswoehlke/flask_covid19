from datetime import date

from project.data_all.all_model_mixins import AllEntityMixin


class AllImportMixin(AllEntityMixin):
    @classmethod
    def find_by_datum(cls, datum: date):
        pass

    @classmethod
    def find_by_datum_str(cls, datum: date):
        pass

    @classmethod
    def find_by_datum_reported(cls, datum: date):
        pass

    @classmethod
    def get_datum_list(cls):
        pass