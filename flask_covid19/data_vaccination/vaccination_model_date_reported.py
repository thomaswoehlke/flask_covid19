
from app_config.database import db
from data_all.all_model_date_reported import AllDateReported


class VaccinationDateReported(AllDateReported):
    __mapper_args__ = {
        'polymorphic_identity': 'vaccination_date_reported'
    }