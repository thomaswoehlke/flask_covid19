from sqlalchemy import Sequence

from project.app_bootstrap.database import db
from project.data_all.all_model_flat import AllFlat
from project.data_all.all_model_flat_mixins import AllImportFlatMixin


class WhoFlat(AllFlat, AllImportFlatMixin):
    __tablename__ = "who_import_flat"
    __mapper_args__ = {"concrete": True}

    def __repr__(self):
        return "{}({} {} {} {} {})".format(
            self.__class__.__name__,
            self.datum.isoformat(),
            self.date_reported_import_str,
            self.location_code,
            self.location,
            self.location_group,
        )

    def __str__(self):
        return (
            self.datum.isoformat()
            + " "
            + self.location_code
            + " "
            + self.location
            + " "
            + str(self.location_group)
        )

    id_seq = Sequence('who_import_flat_id_seq')
    id = db.Column(db.Integer,
                   id_seq,
                   server_default=id_seq.next_value(),
                   primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    #
    date_reported_import_str = db.Column(db.String(255), nullable=False)
    datum = db.Column(db.Date, nullable=False)
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
    location = db.Column(db.String(255), nullable=False)
    location_group = db.Column(db.String(255), nullable=False)
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


class WhoFlatFactory:
    @classmethod
    def create_new(cls, date_reported, d, row, my_data):
        oo = WhoFlat(
            datum=d.datum,
            year=d.year,
            month=d.month,
            day_of_month=d.day_of_month,
            day_of_week=d.day_of_week,
            week_of_year=d.week_of_year,
            day_of_year=d.day_of_year,
            year_week=d.year_week,
            year_day_of_year=d.year_day_of_year,
            date_reported_import_str=d.date_reported_import_str,
            year_month=d.year_month,
            location_code=row["Country_code"],
            location=row["Country"],
            location_group=row["WHO_region"],
            processed_update=False,
            processed_full_update=False,
            #
            new_cases=my_data["new_cases"],
            cumulative_cases=my_data["cumulative_cases"],
            new_deaths=my_data["new_deaths"],
            cumulative_deaths=my_data["cumulative_deaths"],
            country_code=row["Country_code"],
            country=row["Country"],
            who_region=row["WHO_region"],
            date_reported=date_reported,
        )
        return oo
