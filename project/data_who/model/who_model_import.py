from project.app_bootstrap.database import db
from project.data_all.framework.model.all_model_import import AllImport
from project.data_all.framework.interfaces.all_model_import_mixins import AllImportMixin
from sqlalchemy import and_, Sequence
from sqlalchemy.orm import Bundle


class WhoImport(AllImport, AllImportMixin):
    __tablename__ = "who_import"
    __mapper_args__ = {"concrete": True}

    def __repr__(self):
        return "{}({} {} {} {} {})".format(
            self.__class__.__name__,
            self.datum.isoformat(),
            self.date_reported,
            self.country_code,
            self.country,
            self.who_region,
        )

    def __str__(self):
        return "{} {} {} {}".format(
            self.datum.isoformat,
            self.country_code,
            self.country,
            str(self.row_imported),
        )

    id_seq = Sequence('who_import_id_seq')
    id = db.Column(db.Integer,
                   id_seq,
                   server_default=id_seq.next_value(),
                   primary_key=True)
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
        return (
            db.session.query(cls.who_region).order_by(cls.who_region).distinct().all()
        )

    @classmethod
    def get_all_countries(cls):
        return db.session.query(cls.country).order_by(cls.country).distinct().all()

    @classmethod
    def get_dates_reported(cls):
        return (
            db.session.query(cls.date_reported)
            .order_by(cls.date_reported.desc())
            .distinct()
            .all()
        )

    @classmethod
    def get_for_one_day(cls, day: str):
        return (
            db.session.query(cls)
            .filter(cls.date_reported == day)
            .order_by(cls.country.asc())
            .all()
        )

    @classmethod
    def get_dates_reported_as_string_array(cls):
        myresultarray = []
        myresultset = (
            db.session.query(cls.date_reported)
            .order_by(cls.date_reported.desc())
            .group_by(cls.date_reported)
            .distinct()
            .all()
        )
        for my_datum_item in myresultset:
            my_datum = my_datum_item.date_reported
            if my_datum not in myresultarray:
                myresultarray.append(my_datum)
        return myresultarray

    @classmethod
    def countries(cls):
        bu = Bundle("countries", cls.country_code, cls.country, cls.who_region)
        return db.session.query(bu).distinct()

    @classmethod
    def get_datum_of_all_who_import(cls):
        dates_reported = []
        for datum_item in (
            db.session.query(cls.datum).distinct().order_by(cls.datum.desc())
        ):
            item = datum_item[0]
            if item not in dates_reported:
                dates_reported.append(item)
        return dates_reported

    @classmethod
    def find_by_datum_and_country(cls, date_reported: str, country: str):
        db.session.query(cls).filter(
            and_(cls.date_reported == date_reported, cls.country == country)
        ).order_by(cls.date_reported.desc()).one_or_none()

    @classmethod
    def get_by_datum_and_country(cls, date_reported: str, country: str):
        db.session.query(cls).filter(
            and_(cls.date_reported == date_reported, cls.country == country)
        ).order_by(cls.date_reported.desc()).one()


class WhoImportFactory:
    @classmethod
    def create_new(cls, date_reported, d, row):
        o = WhoImport(
            new_cases=row["New_cases"],
            cumulative_cases=row["Cumulative_cases"],
            new_deaths=row["New_deaths"],
            cumulative_deaths=row["Cumulative_deaths"],
            country_code=row["Country_code"],
            country=row["Country"],
            who_region=row["WHO_region"],
            date_reported=date_reported,
            datum=d.datum,
            date_reported_import_str=date_reported,
            processed_update=False,
            processed_full_update=False,
        )
        return o
