from data_all.all_model_date_reported_mixins import AllDateReportedMixin
from data_all.all_model_location_mixins import AllLocationMixin


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

