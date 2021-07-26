from data_all.all_model_location_group_mixins import AllLocationGroupMixin
from data_all.all_model_mixins import AllEntityMixin


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