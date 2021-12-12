from project.data_all.all_model_location_group import AllLocationGroup


class OwidContinent(AllLocationGroup):
    __mapper_args__ = {"polymorphic_identity": "owid_location_group"}


class OwidContinentFactory:
    @classmethod
    def create_new(cls, location_group_str: str):
        o = OwidContinent(
            location_group=location_group_str,
            processed_update=False,
            processed_full_update=False,
        )
        return o
