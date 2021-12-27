from sqlalchemy import Sequence

from project.app_bootstrap.database import db
from project.data_all.framework.model.all_model_flat import AllFlat


class EcdcFlat(AllFlat):
    __tablename__ = "ecdc_import_flat"
    __mapper_args__ = {"concrete": True}

    def __repr__(self):
        return "{}({} {} {} {})".format(
            self.__class__.__name__,
            self.date_reported_import_str,
            self.datum.isoformat(),
            self.location,
            self.location_group.__repr__(),
        )

    id_seq = Sequence('ecdc_import_flat_id_seq')
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
    location_code = db.Column(db.String(255), nullable=True)
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
    geo_id = db.Column(db.String(255), nullable=False)
    pop_data_2019 = db.Column(db.String(255), nullable=True)
    cases = db.Column(db.Integer, nullable=False)
    deaths = db.Column(db.Integer, nullable=False)
    cumulative_number_for_14_days_of_covid19_cases_per_100000 = db.Column(
        db.Float, nullable=True
    )


class EcdcFlatFactory:
    @classmethod
    def create_new(cls, d, row):
        oo = EcdcFlat(
            date_reported_import_str=d.date_reported_import_str,
            datum=d.datum,
            year=d.year,
            month=d.month,
            day_of_month=d.day_of_month,
            day_of_week=d.day_of_week,
            week_of_year=d.week_of_year,
            day_of_year=d.day_of_year,
            year_week=d.year_week,
            year_day_of_year=d.year_day_of_year,
            year_month=d.year_month,
            location=row["countriesAndTerritories"],
            location_group=row["continentExp"],
            location_code=row["countryterritoryCode"],
            processed_update=False,
            processed_full_update=False,
            #
            cases=int(row["cases"]),
            deaths=int(row["deaths"]),
            geo_id=row["geoId"],
            pop_data_2019=row["popData2019"],
            cumulative_number_for_14_days_of_covid19_cases_per_100000=0.0
            if "" == row["Cumulative_number_for_14_days_of_COVID-19_cases_per_100000"]
            else float(
                row["Cumulative_number_for_14_days_of_COVID-19_cases_per_100000"]
            ),
        )
        return oo
