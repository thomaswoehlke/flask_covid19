
from app_config.database import db
from data_all.all_model import AllFactTableTimeSeries
from data_vaccination.vaccination_model import VaccinationDateReported


class VaccinationData(AllFactTableTimeSeries):
    __tablename__ = 'vaccination'
    __mapper_args__ = {'concrete': True}
    __table_args__ = (
        db.UniqueConstraint('date_reported_id', name="uix_vaccination"),
    )

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.date_reported.__repr__())

    id = db.Column(db.Integer, primary_key=True)
    date_reported_id = db.Column(db.Integer, db.ForeignKey('all_date_reported.id'), nullable=False)
    date_reported = db.relationship(
        'VaccinationDateReported',
        lazy='joined',
        cascade='save-update',
        order_by='desc(VaccinationDateReported.datum)')
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
        return db.session.query(cls) \
            .filter(cls.date_reported_id == date_reported.id) \
            .one_or_none()

    @classmethod
    def delete_data_for_one_day(cls, date_reported: VaccinationDateReported):
        for data in cls.find_by_date_reported(date_reported):
            db.session.delete(data)
        db.session.delete(date_reported)
        db.session.commit()
