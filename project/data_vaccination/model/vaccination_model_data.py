from sqlalchemy import Sequence

from project.app_bootstrap.database import db
from project.data_all.framework.model.all_model_data import AllFactTableTimeSeries
from project.data_vaccination.model.vaccination_model_date_reported import (
    VaccinationDateReported,
)
from project.data_vaccination.model.vaccination_model_import import VaccinationImport


class VaccinationData(AllFactTableTimeSeries):
    __tablename__ = "vaccination"
    __mapper_args__ = {"concrete": True}
    __table_args__ = (db.UniqueConstraint("date_reported_id", name="uix_vaccination"),)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.date_reported.__repr__()})"

    vaccination_id_seq = Sequence('vaccination_id_seq')
    id = db.Column(db.Integer,
                   vaccination_id_seq,
                   server_default=vaccination_id_seq.next_value(),
                   primary_key=True)
    date_reported_id = db.Column(
        db.Integer, db.ForeignKey("all_date_reported.id"), nullable=False
    )
    date_reported = db.relationship(
        "VaccinationDateReported",
        lazy="joined",
        cascade="save-update",
        order_by="desc(VaccinationDateReported.datum)",
    )
    processed_update = db.Column(db.Boolean, nullable=False, index=True)
    processed_full_update = db.Column(db.Boolean, nullable=False, index=True)
    #
    dosen_kumulativ = db.Column(db.Integer, nullable=False, index=True)
    dosen_differenz_zum_vortag = db.Column(db.Integer, nullable=False, index=True)
    dosen_biontech_kumulativ = db.Column(db.Integer, nullable=False, index=True)
    dosen_moderna_kumulativ = db.Column(db.Integer, nullable=False, index=True)
    personen_erst_kumulativ = db.Column(db.Integer, nullable=False, index=True)
    personen_voll_kumulativ = db.Column(db.Integer, nullable=False, index=True)
    impf_quote_erst = db.Column(db.Float, nullable=False, index=True)
    impf_quote_voll = db.Column(db.Float, nullable=False, index=True)
    indikation_alter_dosen = db.Column(db.Integer, nullable=False, index=True)
    indikation_beruf_dosen = db.Column(db.Integer, nullable=False, index=True)
    indikation_medizinisch_dosen = db.Column(db.Integer, nullable=False, index=True)
    indikation_pflegeheim_dosen = db.Column(db.Integer, nullable=False, index=True)
    indikation_alter_erst = db.Column(db.Integer, nullable=False, index=True)
    indikation_beruf_erst = db.Column(db.Integer, nullable=False, index=True)
    indikation_medizinisch_erst = db.Column(db.Integer, nullable=False, index=True)
    indikation_pflegeheim_erst = db.Column(db.Integer, nullable=False, index=True)
    indikation_alter_voll = db.Column(db.Integer, nullable=False, index=True)
    indikation_beruf_voll = db.Column(db.Integer, nullable=False, index=True)
    indikation_medizinisch_voll = db.Column(db.Integer, nullable=False, index=True)
    indikation_pflegeheim_voll = db.Column(db.Integer, nullable=False, index=True)

    @classmethod
    def find_by_date_reported(cls, date_reported: VaccinationDateReported):
        return (
            db.session.query(cls)
            .filter(cls.date_reported_id == date_reported.id)
            .one_or_none()
        )

    @classmethod
    def delete_data_for_one_day(cls, date_reported: VaccinationDateReported):
        for data in cls.find_by_date_reported(date_reported):
            db.session.delete(data)
        db.session.delete(date_reported)
        db.session.commit()


class VaccinationDataFactory:
    @classmethod
    def create_new(
        cls, date_reported: VaccinationDateReported, item_data_import: VaccinationImport
    ):
        o = VaccinationData(
            date_reported=date_reported,
            dosen_kumulativ=item_data_import.dosen_kumulativ,
            dosen_differenz_zum_vortag=item_data_import.dosen_differenz_zum_vortag,
            dosen_biontech_kumulativ=item_data_import.dosen_biontech_kumulativ,
            dosen_moderna_kumulativ=item_data_import.dosen_moderna_kumulativ,
            personen_erst_kumulativ=item_data_import.personen_erst_kumulativ,
            personen_voll_kumulativ=item_data_import.personen_voll_kumulativ,
            impf_quote_erst=item_data_import.impf_quote_erst,
            impf_quote_voll=item_data_import.impf_quote_voll,
            indikation_alter_dosen=item_data_import.indikation_alter_dosen,
            indikation_beruf_dosen=item_data_import.indikation_beruf_dosen,
            indikation_medizinisch_dosen=item_data_import.indikation_medizinisch_dosen,
            indikation_pflegeheim_dosen=item_data_import.indikation_pflegeheim_dosen,
            indikation_alter_erst=item_data_import.indikation_alter_erst,
            indikation_beruf_erst=item_data_import.indikation_beruf_erst,
            indikation_medizinisch_erst=item_data_import.indikation_medizinisch_erst,
            indikation_pflegeheim_erst=item_data_import.indikation_pflegeheim_erst,
            indikation_alter_voll=item_data_import.indikation_alter_voll,
            indikation_beruf_voll=item_data_import.indikation_beruf_voll,
            indikation_medizinisch_voll=item_data_import.indikation_medizinisch_voll,
            indikation_pflegeheim_voll=item_data_import.indikation_pflegeheim_voll,
            processed_update=True,
            processed_full_update=False,
        )
        return o
