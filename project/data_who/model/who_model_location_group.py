import json

from project.data_all.model.all_model import AllLocationGroup


class WhoCountryRegion(AllLocationGroup):
    __mapper_args__ = {"polymorphic_identity": "who_location_group"}

    #def to_json(self):
    #    return json.dumps(self, default=lambda self: self.__dict__)


class WhoCountryRegionFactory:
    @classmethod
    def create_new(cls, location_group_str: str):
        o = WhoCountryRegion(
            location_group=location_group_str,
            processed_update=False,
            processed_full_update=False,
        )
        return o
