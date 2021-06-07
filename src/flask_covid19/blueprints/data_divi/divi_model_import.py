from sqlalchemy.orm import Bundle
from database import db, ITEMS_PER_PAGE
from flask_covid19.blueprints.app_all.all_model_import import AllImport, AllFlat


class DiviImport(AllImport):
    __tablename__ = 'divi_import'
    __mapper_args__ = {'concrete': True}

    id = db.Column(db.Integer, primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    date_reported_import_str = db.Column(db.String(255), nullable=False)
    datum = db.Column(db.Date, nullable=False)
    #
    date_reported = db.Column(db.String(255), nullable=False)
    country_code = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    divi_region = db.Column(db.String(255), nullable=False)
    new_cases = db.Column(db.String(255), nullable=False)
    cumulative_cases = db.Column(db.String(255), nullable=False)
    new_deaths = db.Column(db.String(255), nullable=False)
    cumulative_deaths = db.Column(db.String(255), nullable=False)

    @classmethod
    def get_regions(cls):
        return db.session.query(cls.divi_region)\
            .order_by(cls.divi_region)\
            .distinct().all()

    @classmethod
    def get_dates_reported(cls):
        return db.session.query(cls.date_reported)\
            .order_by(cls.date_reported.desc())\
            .distinct().all()

    @classmethod
    def get_for_one_day(cls, day):
        return db.session.query(cls)\
            .filter(cls.date_reported == day)\
            .order_by(cls.country.asc())\
            .all()

    @classmethod
    def get_dates_reported_as_array(cls):
        myresultarray = []
        myresultset = db.session.query(cls.date_reported)\
            .order_by(cls.date_reported.desc())\
            .group_by(cls.date_reported)\
            .distinct()
        for item, in myresultset:
            pass
        return myresultarray

    @classmethod
    def countries(cls):
        bu = Bundle('countries', cls.country_code, cls.country, cls.divi_region)
        return db.session.query(bu).distinct()

    @classmethod
    def get_datum_of_all_divi_import(cls):
        dates_reported = []
        bu = Bundle('dates_reported', cls.date_reported)
        for date_reported in db.session.query(bu).distinct().order_by(cls.date_reported):
            item = date_reported[0][0]
            if not item in dates_reported:
                dates_reported.append(item)
        return dates_reported
