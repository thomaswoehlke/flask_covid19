from datetime import date


class AllEntityMixinBase:

    @classmethod
    def get_by_id(cls, other_id: int):
        pass

    @classmethod
    def find_by_id(cls, other_id: int):
        pass

    @classmethod
    def remove_all(cls):
        return None

    @classmethod
    def __query_all(cls):
        pass

    @classmethod
    def find_all(cls):
        pass

    @classmethod
    def get_all(cls, page: int):
        pass

    @classmethod
    def find_all_as_dict(cls):
        pass

    @classmethod
    def find_all_as_str(cls):
        pass


class AllEntityWorkerProgressMixin:

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

    @classmethod
    def set_all_processed_full_update(cls):
        pass

    @classmethod
    def set_all_processed_update(cls):
        pass


class AllEntityMixin(AllEntityMixinBase, AllEntityWorkerProgressMixin):
    pass


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


class AllLocationGroupMixin(AllEntityMixin):

    @classmethod
    def get_last(cls):
        pass

    @classmethod
    def get_by_location_group(cls, location_group: str):
        pass

    @classmethod
    def find_by_location_group(cls, location_group: str):
        pass


class AllLocationMixin(AllEntityMixin):

    @classmethod
    def find_by_location_code(cls, location_code: str):
        pass

    @classmethod
    def get_by_location_code(cls, location_code: str):
        pass

    @classmethod
    def find_by_location(cls, location: str):
        pass

    @classmethod
    def get_by_location(cls, location: str):
        pass

    @classmethod
    def find_by_location_group(cls, location_group: AllLocationGroupMixin):
        pass

    @classmethod
    def get_by_location_group(cls, location_group: AllLocationGroupMixin, page: int):
        pass

    @classmethod
    def find_by_location_code_and_location_and_location_group(cls, location_code: str, location: str,
                                                              location_group: AllLocationGroupMixin):
        pass

    @classmethod
    def get_by_location_code_and_location_and_location_group(cls, location_code: str, location: str,
                                                             location_group: AllLocationGroupMixin):
        pass

    @classmethod
    def find_by_location_code_and_location(cls, location_code: str, location: str):
        pass

    @classmethod
    def get_by_location_code_and_location(cls, location_code: str, location: str):
        pass


class AllFactTableTimeSeriesMixin(AllEntityMixin):

    @classmethod
    def get_datum_list(cls):
        pass

    @classmethod
    def get_date_reported_list(cls):
        pass

    @classmethod
    def get_joungest_date_reported(cls):
        pass

    @classmethod
    def find_by_date_reported(cls, date_reported: AllDateReportedMixin):
        pass

    @classmethod
    def get_by_date_reported(cls, date_reported: AllDateReportedMixin, page: int):
        pass

    @classmethod
    def delete_data_for_one_day(cls, date_reported: AllDateReportedMixin):
        pass


class AllFactTableMixin(AllFactTableTimeSeriesMixin):

    @classmethod
    def get_by_location(cls, location: AllLocationMixin, page: int):
        pass

    @classmethod
    def find_by_location(cls, location: AllLocationMixin):
        pass

    @classmethod
    def find_by_date_reported_and_location(cls, date_reported: AllDateReportedMixin, location: AllLocationMixin):
        pass

    @classmethod
    def get_by_date_reported_and_location(cls, date_reported: AllDateReportedMixin, location: AllLocationMixin, page: int):
        pass

