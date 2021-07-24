
from data_all.all_model_location_group import AllLocationGroup


class WhoCountryRegion(AllLocationGroup):
    __mapper_args__ = {
        'polymorphic_identity': 'who_location_group'
    }
