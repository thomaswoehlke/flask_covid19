from data_all.framework.model.interfaces.all_model_date_reported_mixins import AllDateReportedMixin
from data_all.framework.model.interfaces.all_model_location_mixins import AllLocationMixin
from data_all.framework.model.interfaces.all_model_mixins import AllEntityMixin


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
    def find_by_date_reported_and_location(
        cls, date_reported: AllDateReportedMixin, location: AllLocationMixin
    ):
        pass

    @classmethod
    def get_by_date_reported_and_location(
        cls, date_reported: AllDateReportedMixin, location: AllLocationMixin, page: int
    ):
        pass
