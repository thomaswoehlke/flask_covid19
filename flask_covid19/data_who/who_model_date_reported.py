
from data_all.all_model import AllDateReported


class WhoDateReported(AllDateReported):
    __mapper_args__ = {
        'polymorphic_identity': 'who_date_reported'
    }
