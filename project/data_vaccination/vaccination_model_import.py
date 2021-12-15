from project.app_bootstrap.database import db
from project.app_bootstrap.database import items_per_page
from project.data_all.all_model_import import AllImport
from sqlalchemy.orm import Bundle


class VaccinationImport(AllImport):
    __tablename__ = "vaccination_import"
    __mapper_args__ = {"concrete": True}

    def __repr__(self):
        return "{}({} {})".format(
            self.__class__.__name__,
            self.date_reported_import_str,
            self.datum.isoformat(),
        )

    id = db.Column(db.Integer, primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    datum = db.Column(db.Date, nullable=False)
    date_reported_import_str = db.Column(db.String(255), nullable=False)
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

    @classmethod
    def get_all(cls, page: int):
        return (
            db.session.query(cls)
            .order_by(cls.datum.desc())
            .paginate(page, per_page=items_per_page)
        )

    @classmethod
    def find_all(cls):
        return db.session.query(cls).order_by(cls.datum).all()

    @classmethod
    def get_date_rep(cls):
        return (
            db.session.query(cls.datum)
            .group_by(cls.datum)
            .distinct()
            .order_by(cls.datum)
            .all()
        )

    @classmethod
    def get_date_reported_as_array(cls):
        resultarray = []
        resultset = db.session.query(cls.datum).group_by(cls.datum).distinct().all()
        for (resultitem,) in resultset:
            o = str(resultitem)
            resultarray.append(o)
        return resultarray

    @classmethod
    def get_date_reported_import_str_list(cls):
        date_reported_import_str_list = []
        bu = Bundle("date_reported_import_str", cls.date_reported_import_str)
        oi_list = (
            db.session.query(bu)
            .distinct()
            .order_by(cls.date_reported_import_str.desc())
        )
        for date_reported_import_str_row in oi_list:
            item = date_reported_import_str_row[0]
            if item not in date_reported_import_str_list:
                date_reported_import_str_list.append(item)
        return date_reported_import_str_list


class VaccinationImportFactory:
    @classmethod
    def __int(cls, input_string: str):
        if input_string == "#REF!":
            return 0
        else:
            return int(input_string)

    @classmethod
    def create_new(cls, date_reported, d, row):
        o = VaccinationImport(
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
            date_reported_import_str=date_reported,
            datum=d.datum,
            processed_update=False,
            processed_full_update=False,
        )
        return o
