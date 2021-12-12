from project.data_all.all_model_date_reported import AllDateReported


class OwidDateReported(AllDateReported):
    __mapper_args__ = {"polymorphic_identity": "owid_date_reported"}
