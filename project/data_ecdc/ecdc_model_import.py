from sqlalchemy import Sequence

from project.app_bootstrap.database import db
from project.app_bootstrap.database import items_per_page
from project.data_all.all_model_import import AllImport


class EcdcImport(AllImport):
    __tablename__ = "ecdc_import"
    __mapper_args__ = {"concrete": True}

    def __repr__(self):
        return "{}({} {} {} {})".format(
            self.__class__.__name__,
            self.date_reported_import_str,
            self.datum.isoformat(),
            self.countries_and_territories,
            self.continent_exp,
        )

    id_seq = Sequence('ecdc_import_id_seq')
    id = db.Column(db.Integer,
                   id_seq,
                   server_default=id_seq.next_value(),
                   primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    date_reported_import_str = db.Column(db.String(255), nullable=False)
    datum = db.Column(db.Date, nullable=False)
    #
    date_rep = db.Column(db.String(255), nullable=False)
    day = db.Column(db.String(255), nullable=False)
    month = db.Column(db.String(255), nullable=False)
    year = db.Column(db.String(255), nullable=False)
    #
    cases = db.Column(db.String(255), nullable=False)
    deaths = db.Column(db.String(255), nullable=False)
    pop_data_2019 = db.Column(db.String(255), nullable=False)
    #
    countries_and_territories = db.Column(db.String(255), nullable=False)
    geo_id = db.Column(db.String(255), nullable=False)
    country_territory_code = db.Column(db.String(255), nullable=False)
    continent_exp = db.Column(db.String(255), nullable=False)
    #
    cumulative_number_for_14_days_of_covid19_cases_per_100000 = db.Column(
        db.String(255), nullable=False
    )

    @classmethod
    def get_all(cls, page: int):
        return (
            db.session.query(cls)
            .order_by(cls.year, cls.month, cls.day, cls.countries_and_territories)
            .paginate(page, per_page=items_per_page)
        )

    @classmethod
    def get_date_rep(cls):
        return (
            db.session.query(cls.date_rep)
            .group_by(cls.date_rep)
            .distinct()
            .order_by(cls.date_rep.desc())
            .all()
        )

    @classmethod
    def get_continent(cls):
        return (
            db.session.query(cls.continent_exp)
            .group_by(cls.continent_exp)
            .distinct()
            .order_by(cls.continent_exp.asc())
            .all()
        )

    @classmethod
    def get_countries_of_continent(cls, my_continent):
        my_continent_exp = my_continent.location_group
        my_params = {}
        my_params["my_continent_param"] = my_continent_exp
        return (
            db.session.query(
                cls.countries_and_territories,
                cls.pop_data_2019,
                cls.geo_id,
                cls.country_territory_code,
                cls.continent_exp,
            )
            .filter(cls.continent_exp == my_continent_exp)
            .distinct()
            .group_by(
                cls.countries_and_territories,
                cls.pop_data_2019,
                cls.geo_id,
                cls.country_territory_code,
                cls.continent_exp,
            )
            .order_by(cls.countries_and_territories.asc())
            .all()
        )

    @classmethod
    def find_by_date_reported(cls, p_edcd_date_reported_str: str = ""):
        return (
            db.session.query(cls).filter(cls.date_rep == p_edcd_date_reported_str).all()
        )


class EcdcImportFactory:
    @classmethod
    def create_new(cls, date_reported, d, row):
        o = EcdcImport(
            date_reported_import_str=d.date_reported_import_str,
            datum=d.datum,
            processed_update=False,
            processed_full_update=False,
            date_rep=date_reported,
            day=row["day"],
            month=row["month"],
            year=row["year"],
            cases=row["cases"],
            deaths=row["deaths"],
            countries_and_territories=row["countriesAndTerritories"],
            geo_id=row["geoId"],
            country_territory_code=row["countryterritoryCode"],
            pop_data_2019=row["popData2019"],
            continent_exp=row["continentExp"],
            cumulative_number_for_14_days_of_covid19_cases_per_100000=row[
                "Cumulative_number_for_14_days_of_COVID-19_cases_per_100000"
            ],
        )
        return o
