from flask_covid19.data_all.all_model_location_group import AllLocationGroup


class EcdcContinent(AllLocationGroup):
    __mapper_args__ = {"polymorphic_identity": "ecdc_location_group"}


class EcdcContinentFactory:
    @classmethod
    def create_new(cls, location_group_str: str):
        o = EcdcContinent(
            location_group=location_group_str,
            processed_update=False,
            processed_full_update=False,
        )
        return o
