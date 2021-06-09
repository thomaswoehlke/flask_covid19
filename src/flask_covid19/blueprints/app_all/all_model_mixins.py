from datetime import date


class BlueprintEntityMixin:

    @classmethod
    def get_by_id(cls, other_id: int):
        pass

    @classmethod
    def find_by_id(cls, other_id: int):
        pass

    @classmethod
    def __query_all(cls):
        pass

    @classmethod
    def remove_all(cls):
        return None

    #TODO: deprecated, use get_all instead
    @classmethod
    def get_all_as_page(cls, page: int):
        pass

    @classmethod
    def get_all(cls, page: int):
        pass

    @classmethod
    def find_all(cls):
        pass

    @classmethod
    def find_all_as_dict(cls):
        pass

    @classmethod
    def find_all_as_array(cls):
        pass

    @classmethod
    def find_all_as_str_array(cls):
        pass

    @classmethod
    def set_all_processed_full_update(cls):
        pass

    def set_processed_update(self):
        pass

    def set_processed_full_update(self):
        pass

    def unset_processed_update(self):
        pass

    def unset_processed_full_update(self):
        pass

    @classmethod
    def find_by_not_processed_update(cls):
        pass

    @classmethod
    def find_by_not_processed_full_update(cls):
        pass


class BlueprintDateReportedMixin(BlueprintEntityMixin):

    @classmethod
    def __query_all(cls):
        pass

    def get_name_for_weekday(self):
        pass

    @classmethod
    def get_names_for_weekday(cls):
        pass

    def get_name_for_month(self):
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

    @classmethod
    def get_all_str(cls):
        pass
