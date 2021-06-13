from sqlalchemy.orm import Bundle
from sqlalchemy import and_
from flask_covid19_conf.database import db # , cache
from flask_covid19_app.blueprints.app_all.all_model_import import AllImport, AllFlat
from flask_covid19_app.blueprints.app_all.all_model_import_mixins import AllImportMixin, AllImportFlatMixin


class WhoImport(AllImport, AllImportMixin):
    __tablename__ = 'who_import'
    __mapper_args__ = {'concrete': True}

    def __repr__(self):
        return "%s(%s %s %s %s %s)" % (self.__class__.__name__,
                                       self.datum.isoformat(),
                                       self.date_reported,
                                       self.country_code,
                                       self.country,
                                       self.who_region)

    def __str__(self):
        return "%s %s %s %s" % (self.datum.isoformat, self.country_code, self.country, str(self.row_imported))

    id = db.Column(db.Integer, primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    date_reported_import_str = db.Column(db.String(255), nullable=False)
    datum = db.Column(db.Date, nullable=False)
    #
    new_cases = db.Column(db.String(255), nullable=False)
    cumulative_cases = db.Column(db.String(255), nullable=False)
    new_deaths = db.Column(db.String(255), nullable=False)
    cumulative_deaths = db.Column(db.String(255), nullable=False)
    country_code = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    who_region = db.Column(db.String(255), nullable=False)
    date_reported = db.Column(db.String(255), nullable=False)

    @classmethod
    def get_regions(cls):
        return db.session.query(cls.who_region)\
            .order_by(cls.who_region)\
            .distinct().all()

    @classmethod
    def get_all_countries(cls):
        return db.session.query(cls.country) \
            .order_by(cls.country) \
            .distinct().all()

    @classmethod
    def get_dates_reported(cls):
        return db.session.query(cls.date_reported)\
            .order_by(cls.date_reported.desc())\
            .distinct().all()

    @classmethod
    def get_for_one_day(cls, day: str):
        return db.session.query(cls)\
            .filter(cls.date_reported == day)\
            .order_by(cls.country.asc())\
            .all()

    @classmethod
    def get_dates_reported_as_string_array(cls):
        myresultarray = []
        myresultset = db.session.query(cls.date_reported)\
            .order_by(cls.date_reported.desc())\
            .group_by(cls.date_reported)\
            .distinct()\
            .all()
        for my_datum_item in myresultset:
            my_datum = my_datum_item.date_reported
            if my_datum not in myresultarray:
                myresultarray.append(my_datum)
        return myresultarray

    @classmethod
    def countries(cls):
        bu = Bundle('countries', cls.country_code, cls.country, cls.who_region)
        return db.session.query(bu).distinct()

    @classmethod
    def get_datum_of_all_who_import(cls):
        dates_reported = []
        for datum_item in db.session.query(cls.datum).distinct().order_by(cls.datum.desc()):
            item = datum_item[0]
            if item not in dates_reported:
                dates_reported.append(item)
        return dates_reported

    @classmethod
    def find_by_datum_and_country(cls, date_reported: str, country: str):
        db.session.query(cls)\
            .filter(and_(cls.date_reported == date_reported, cls.country == country))\
            .order_by(cls.date_reported.desc())\
            .one_or_none()

    @classmethod
    def get_by_datum_and_country(cls, date_reported: str, country: str):
        db.session.query(cls)\
            .filter(and_(cls.date_reported == date_reported, cls.country == country))\
            .order_by(cls.date_reported.desc())\
            .one()


class WhoFlat(AllFlat, AllImportFlatMixin):
    __tablename__ = 'who_import_flat'
    __mapper_args__ = {'concrete': True}

    def __repr__(self):
        return "%s(%s %s %s %s %s)" % (self.__class__.__name__,
                                       self.datum.isoformat(), self.date_reported_import_str,
                                       self.location_code, self.location, self.location_group)

    def __str__(self):
        return self.datum.isoformat() + " " + self.location_code + " " + self.location + " " + str(self.location_group)

    id = db.Column(db.Integer, primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    #
    date_reported_import_str = db.Column(db.String(255), nullable=False, index=True)
    datum = db.Column(db.Date, nullable=False, index=True)
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
    location = db.Column(db.String(255), nullable=False, index=True)
    location_group = db.Column(db.String(255), nullable=False, index=True)
    location_code = db.Column(db.String(255), nullable=False)
    #
    new_cases = db.Column(db.Integer, nullable=False)
    cumulative_cases = db.Column(db.Integer, nullable=False)
    new_deaths = db.Column(db.Integer, nullable=False)
    cumulative_deaths = db.Column(db.Integer, nullable=False)
    country_code = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    who_region = db.Column(db.String(255), nullable=False)
    date_reported = db.Column(db.String(255), nullable=False)
