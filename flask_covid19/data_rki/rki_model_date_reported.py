
from app_config.database import db, items_per_page
from data_all.all_model_date_reported import AllDateReported


class RkiMeldedatum(AllDateReported):
    __mapper_args__ = {
        'polymorphic_identity': 'rki_date_reported'
    }
