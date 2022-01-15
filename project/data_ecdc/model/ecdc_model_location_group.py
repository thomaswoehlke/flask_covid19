from project.data_all.model.all_model import AllLocationGroup


class EcdcContinent(AllLocationGroup):
    __mapper_args__ = {"polymorphic_identity": "ecdc_location_group"}
