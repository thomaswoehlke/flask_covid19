import json

from project.data_all.model.all_model import AllLocation
from project.data_who.model.who_model_location_group import WhoCountryRegion


class WhoCountry(AllLocation):
    __mapper_args__ = {"polymorphic_identity": "who_location"}

    def to_json(self):
        return json.dumps(self, default=lambda self: self.__dict__)

class WhoCountryFactory:
    @classmethod
    def create_new(
        cls, location: str, location_code: str, location_group: WhoCountryRegion
    ):
        o = WhoCountry(
            location=location,
            location_code=location_code,
            location_group=location_group,
            processed_update=False,
            processed_full_update=False,
        )
        return o
