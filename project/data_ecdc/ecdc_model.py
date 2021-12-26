from data_all.framework.model.all_model_date_reported import AllDateReported


class EcdcDateReported(AllDateReported):
    __mapper_args__ = {"polymorphic_identity": "ecdc_date_reported"}
