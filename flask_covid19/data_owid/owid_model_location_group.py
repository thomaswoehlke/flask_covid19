
from data_all.all_model_location_group import AllLocationGroup


class OwidContinent(AllLocationGroup):
    __mapper_args__ = {
        'polymorphic_identity': 'owid_location_group'
    }
