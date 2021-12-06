from flask_covid19.data_all.all_model_date_reported import AllDateReported


class WhoDateReported(AllDateReported):
    __mapper_args__ = {"polymorphic_identity": "who_date_reported"}
