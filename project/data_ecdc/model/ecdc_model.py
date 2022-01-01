from project.data_all.all_model import AllDateReported


class EcdcDateReported(AllDateReported):
    __mapper_args__ = {"polymorphic_identity": "ecdc_date_reported"}
