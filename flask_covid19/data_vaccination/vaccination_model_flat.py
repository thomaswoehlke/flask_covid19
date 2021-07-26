
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


class VaccinationFlatFactory:

    @classmethod
    def __int(cls, input_string: str):
        if input_string == '#REF!':
            return 0
        else:
            return int(input_string)

    @classmethod
    def create_new(cls, date_reported, d, row):
        oo = VaccinationFlat(
            datum=d.datum,
            year=d.year,
            month=d.month,
            day_of_month=d.day_of_month,
            day_of_week=d.day_of_week,
            week_of_year=d.week_of_year,
            day_of_year=d.day_of_year,
            year_week=d.year_week,
            year_day_of_year=d.year_day_of_year,
            date_reported_import_str=date_reported,
            year_month=d.year_month,
            location_code="",
            location="",
            location_group="",
            processed_update=False,
            processed_full_update=False,
            #
            dosen_kumulativ=cls.__int(row['dosen_kumulativ']),
            dosen_differenz_zum_vortag=cls.__int(row['dosen_differenz_zum_vortag']),
            dosen_biontech_kumulativ=cls.__int(row['dosen_biontech_kumulativ']),
            dosen_moderna_kumulativ=cls.__int(row['dosen_moderna_kumulativ']),
            personen_erst_kumulativ=cls.__int(row['personen_erst_kumulativ']),
            personen_voll_kumulativ=cls.__int(row['personen_voll_kumulativ']),
            impf_quote_erst=float(row['impf_quote_erst']),
            impf_quote_voll=float(row['impf_quote_voll']),
            indikation_alter_dosen=cls.__int(row['indikation_alter_dosen']),
            indikation_beruf_dosen=cls.__int(row['indikation_beruf_dosen']),
            indikation_medizinisch_dosen=cls.__int(row['indikation_medizinisch_dosen']),
            indikation_pflegeheim_dosen=cls.__int(row['indikation_pflegeheim_dosen']),
            indikation_alter_erst=cls.__int(row['indikation_alter_erst']),
            indikation_beruf_erst=cls.__int(row['indikation_beruf_erst']),
            indikation_medizinisch_erst=cls.__int(row['indikation_medizinisch_erst']),
            indikation_pflegeheim_erst=cls.__int(row['indikation_pflegeheim_erst']),
            indikation_alter_voll=cls.__int(row['indikation_alter_voll']),
            indikation_beruf_voll=cls.__int(row['indikation_beruf_voll']),
            indikation_medizinisch_voll=cls.__int(row['indikation_medizinisch_voll']),
            indikation_pflegeheim_voll=cls.__int(row['indikation_pflegeheim_voll']),
        )
        return oo