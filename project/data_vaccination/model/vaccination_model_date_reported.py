from project.data_all.all_model import AllDateReported


class VaccinationDateReported(AllDateReported):
    __mapper_args__ = {"polymorphic_identity": "vaccination_date_reported"}
