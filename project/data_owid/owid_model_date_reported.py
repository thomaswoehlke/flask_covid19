from project.data_all.framework.model.all_model_date_reported import AllDateReported


class OwidDateReported(AllDateReported):
    __mapper_args__ = {"polymorphic_identity": "owid_date_reported"}
