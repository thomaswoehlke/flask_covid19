
from app_config.database import db
from data_all.all_model_flat import AllFlat


class VaccinationFlat(AllFlat):
    __tablename__ = 'vaccination_import_flat'
    __mapper_args__ = {'concrete': True}

    def __repr__(self):
        return "%s(%s %s)" % (self.__class__.__name__,
                              self.date_reported_import_str,
                              self.datum.isoformat())

    id = db.Column(db.Integer, primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False, index=True)
    processed_full_update = db.Column(db.Boolean, nullable=False, index=True)
    date_reported_import_str = db.Column(db.String(255), nullable=False, index=True)
    datum = db.Column(db.Date, nullable=False, index=True)
    location = db.Column(db.String(255), nullable=False, index=True)
    location_group = db.Column(db.String(255), nullable=False, index=True)
    location_code = db.Column(db.String(255), nullable=False, index=True)
    #
    year = db.Column(db.Integer, nullable=False, index=True)
    year_month = db.Column(db.String(255), nullable=False, index=True)
    year_week = db.Column(db.String(255), nullable=False, index=True)
    year_day_of_year = db.Column(db.String(255), nullable=False, index=True)
    #
    month = db.Column(db.Integer, nullable=False, index=True)
    day_of_month = db.Column(db.Integer, nullable=False, index=True)
    day_of_week = db.Column(db.Integer, nullable=False, index=True)
    week_of_year = db.Column(db.Integer, nullable=False, index=True)
    day_of_year = db.Column(db.Integer, nullable=False, index=True)
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
