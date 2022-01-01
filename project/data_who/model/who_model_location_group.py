from project.data_all.all_model import AllLocationGroup


class WhoCountryRegion(AllLocationGroup):
    __mapper_args__ = {"polymorphic_identity": "who_location_group"}


class WhoCountryRegionFactory:
    @classmethod
    def create_new(cls, location_group_str: str):
        o = WhoCountryRegion(
            location_group=location_group_str,
            processed_update=False,
            processed_full_update=False,
        )
        return o
