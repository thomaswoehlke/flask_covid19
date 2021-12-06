from flask_covid19.app_config.database import db
from flask_covid19.app_config.database import items_per_page
from flask_covid19.data_all.all_model_date_reported import AllDateReported


class RkiMeldedatum(AllDateReported):
    __mapper_args__ = {"polymorphic_identity": "rki_date_reported"}
