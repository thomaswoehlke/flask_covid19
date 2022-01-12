from project.data_all.model.all_model import AllDateReported


class RkiMeldedatum(AllDateReported):
    __mapper_args__ = {"polymorphic_identity": "rki_date_reported"}



