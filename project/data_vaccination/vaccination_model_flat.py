from sqlalchemy import Sequence

from project.app_bootstrap.database import db
from project.data_all.all_model_flat import AllFlat


class VaccinationFlat(AllFlat):
    __tablename__ = "vaccination_import_flat"
    __mapper_args__ = {"concrete": True}

    def __repr__(self):
        return "{}({} {})".format(
            self.__class__.__name__,
            self.date_reported_import_str,
            self.datum.isoformat(),
        )

    id_seq = Sequence('id_seq')
    id = db.Column(db.Integer,
                   id_seq,
                   server_default=id_seq.next_value(),
                   primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    date_reported_import_str = db.Column(db.String(255), nullable=False)
    datum = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    location_group = db.Column(db.String(255), nullable=False)
    location_code = db.Column(db.String(255), nullable=False)
    #
    year = db.Column(db.Integer, nullable=False)
    year_month = db.Column(db.String(255), nullable=False)
    year_week = db.Column(db.String(255), nullable=False)
    year_day_of_year = db.Column(db.String(255), nullable=False)
    #
    month = db.Column(db.Integer, nullable=False)
    day_of_month = db.Column(db.Integer, nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)
    week_of_year = db.Column(db.Integer, nullable=False)
    day_of_year = db.Column(db.Integer, nullable=False)
    #
    dosen_kumulativ = db.Column(db.Integer, nullable=False)
    dosen_differenz_zum_vortag = db.Column(db.Integer, nullable=False)
    dosen_biontech_kumulativ = db.Column(db.Integer, nullable=False)
    dosen_moderna_kumulativ = db.Column(db.Integer, nullable=False)
    personen_erst_kumulativ = db.Column(db.Integer, nullable=False)
    personen_voll_kumulativ = db.Column(db.Integer, nullable=False)
    impf_quote_erst = db.Column(db.Float, nullable=False)
    impf_quote_voll = db.Column(db.Float, nullable=False)
    indikation_alter_dosen = db.Column(db.Integer, nullable=False)
    indikation_beruf_dosen = db.Column(db.Integer, nullable=False)
    indikation_medizinisch_dosen = db.Column(db.Integer, nullable=False)
    indikation_pflegeheim_dosen = db.Column(db.Integer, nullable=False)
    indikation_alter_erst = db.Column(db.Integer, nullable=False)
    indikation_beruf_erst = db.Column(db.Integer, nullable=False)
    indikation_medizinisch_erst = db.Column(db.Integer, nullable=False)
    indikation_pflegeheim_erst = db.Column(db.Integer, nullable=False)
    indikation_alter_voll = db.Column(db.Integer, nullable=False)
    indikation_beruf_voll = db.Column(db.Integer, nullable=False)
    indikation_medizinisch_voll = db.Column(db.Integer, nullable=False)
    indikation_pflegeheim_voll = db.Column(db.Integer, nullable=False)


class VaccinationFlatFactory:
    @classmethod
    def __int(cls, input_string: str):
        if input_string == "#REF!":
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
            dosen_kumulativ=cls.__int(row["dosen_kumulativ"]),
            dosen_differenz_zum_vortag=cls.__int(row["dosen_differenz_zum_vortag"]),
            dosen_biontech_kumulativ=cls.__int(row["dosen_biontech_kumulativ"]),
            dosen_moderna_kumulativ=cls.__int(row["dosen_moderna_kumulativ"]),
            personen_erst_kumulativ=cls.__int(row["personen_erst_kumulativ"]),
            personen_voll_kumulativ=cls.__int(row["personen_voll_kumulativ"]),
            impf_quote_erst=float(row["impf_quote_erst"]),
            impf_quote_voll=float(row["impf_quote_voll"]),
            indikation_alter_dosen=cls.__int(row["indikation_alter_dosen"]),
            indikation_beruf_dosen=cls.__int(row["indikation_beruf_dosen"]),
            indikation_medizinisch_dosen=cls.__int(row["indikation_medizinisch_dosen"]),
            indikation_pflegeheim_dosen=cls.__int(row["indikation_pflegeheim_dosen"]),
            indikation_alter_erst=cls.__int(row["indikation_alter_erst"]),
            indikation_beruf_erst=cls.__int(row["indikation_beruf_erst"]),
            indikation_medizinisch_erst=cls.__int(row["indikation_medizinisch_erst"]),
            indikation_pflegeheim_erst=cls.__int(row["indikation_pflegeheim_erst"]),
            indikation_alter_voll=cls.__int(row["indikation_alter_voll"]),
            indikation_beruf_voll=cls.__int(row["indikation_beruf_voll"]),
            indikation_medizinisch_voll=cls.__int(row["indikation_medizinisch_voll"]),
            indikation_pflegeheim_voll=cls.__int(row["indikation_pflegeheim_voll"]),
        )
        return oo
