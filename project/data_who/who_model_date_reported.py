from data_all.framework.model.all_model_date_reported import AllDateReported


class WhoDateReported(AllDateReported):
    __mapper_args__ = {"polymorphic_identity": "who_date_reported"}
