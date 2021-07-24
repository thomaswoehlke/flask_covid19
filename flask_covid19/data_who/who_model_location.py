
from data_all.all_model_location import AllLocation


class WhoCountry(AllLocation):
    __mapper_args__ = {
        'polymorphic_identity': 'who_location'
    }
