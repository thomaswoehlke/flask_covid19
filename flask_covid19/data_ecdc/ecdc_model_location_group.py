
from data_all.all_model_location_group import AllLocationGroup


class EcdcContinent(AllLocationGroup):
    __mapper_args__ = {
        'polymorphic_identity': 'ecdc_location_group'
    }
