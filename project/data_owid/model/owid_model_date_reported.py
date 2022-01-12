from project.data_all.model.all_model import AllDateReported


class OwidDateReported(AllDateReported):
    __mapper_args__ = {"polymorphic_identity": "owid_date_reported"}
