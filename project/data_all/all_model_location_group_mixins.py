from project.data_all.all_model_mixins import AllEntityMixin


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
