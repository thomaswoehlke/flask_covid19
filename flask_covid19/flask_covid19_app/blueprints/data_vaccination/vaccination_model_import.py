from flask_covid19_conf.database import db, ITEMS_PER_PAGE #, cache
from flask_covid19_app.blueprints.app_all.all_model_import import AllImport, AllFlat


class VaccinationImport(AllImport):
    __tablename__ = 'vaccination_import'
    __mapper_args__ = {'concrete': True}

    def __repr__(self):
        return "%s(%s %s)" % (self.__class__.__name__,
                              self.date_reported_import_str,
                              self.datum.isoformat())

    id = db.Column(db.Integer, primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False, index=True)
    processed_full_update = db.Column(db.Boolean, nullable=False, index=True)
    datum = db.Column(db.Date, nullable=False, index=True)
    date_reported_import_str = db.Column(db.String(255), nullable=False, index=True)
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
    def get_all(cls, page: int):
        return db.session.query(cls)\
            .order_by(cls.datum.desc())\
            .paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_all(cls):
        return db.session.query(cls)\
            .order_by(cls.datum)\
            .all()

    @classmethod
    def get_date_rep(cls):
        return db.session.query(cls.datum)\
            .group_by(cls.datum)\
            .distinct()\
            .order_by(cls.datum)\
            .all()

    @classmethod
    def get_date_reported_as_array(cls):
        resultarray = []
        resultset = db.session.query(cls.datum)\
            .group_by(cls.datum)\
            .distinct()\
            .all()
        for resultitem, in resultset:
            o = str(resultitem)
            resultarray.append(o)
        return resultarray

    @classmethod
    def get_date_reported_import_str_list(cls):
        date_reported_import_str_list = []
        bu = Bundle('date_reported_import_str', cls.date_reported_import_str)
        oi_list = db.session.query(bu).distinct().order_by(cls.date_reported_import_str.desc())
        for date_reported_import_str_row in oi_list:
            item = date_reported_import_str_row[0]
            if item not in date_reported_import_str_list:
                date_reported_import_str_list.append(item)
        return date_reported_import_str_list


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
