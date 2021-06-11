from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from flask_covid19_conf.database import db, ITEMS_PER_PAGE # , cache
from flask_covid19_app.blueprints.app_all.all_model import AllDateReported, AllLocationGroup
from flask_covid19_app.blueprints.app_all.all_model import AllLocation, BlueprintFactTable


class OwidDateReported(AllDateReported):
    __mapper_args__ = {
        'polymorphic_identity': 'owid_date_reported'
    }


class OwidContinent(AllLocationGroup):
    __mapper_args__ = {
        'polymorphic_identity': 'owid_location_group'
    }


class OwidCountry(AllLocation):
    __mapper_args__ = {
        'polymorphic_identity': 'owid_location'
    }

    population = db.Column(db.Float)
    population_density = db.Column(db.Float)
    median_age = db.Column(db.Float)
    aged_65_older = db.Column(db.Float)
    aged_70_older = db.Column(db.Float)
    gdp_per_capita = db.Column(db.Float)
    extreme_poverty = db.Column(db.Float)
    cardiovasc_death_rate = db.Column(db.Float)
    diabetes_prevalence = db.Column(db.Float)
    female_smokers = db.Column(db.Float)
    male_smokers = db.Column(db.Float)
    handwashing_facilities = db.Column(db.Float)
    hospital_beds_per_thousand = db.Column(db.Float)
    life_expectancy = db.Column(db.Float)
    human_development_index = db.Column(db.Float)

    @classmethod
    def delete_all_countries_for_continent(cls, owid_continent_one):
        db.session.query(cls)\
            .filter(cls.continent == owid_continent_one)\
            .delete()
        db.session.delete(owid_continent_one)
        db.session.commit()
        return None

    @classmethod
    def get_germany(cls):
        iso_code = 'DEU'
        location = 'Germany'
        return cls.find_by_location_code_and_location(location_code=iso_code, location=location)

    @classmethod
    def get_countries_for_continent(cls, owid_continent_one: OwidContinent, page: int):
        return db.session.query(cls).filter(cls.location_group == owid_continent_one).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_all_countries_for_continent(cls, owid_continent_one: OwidContinent):
        return db.session.query(cls).filter(cls.location_group == owid_continent_one).all()

    @classmethod
    def find_by_iso_code_and_location(cls, iso_code, location):
        return db.session.query(cls).filter(and_((cls.location_code == iso_code), (cls.location == location))).one_or_none()

    @classmethod
    def get_by_iso_code_and_location(cls, iso_code, location):
        return db.session.query(cls).filter(and_((cls.location_code == iso_code), (cls.location == location))).one()


class OwidData(BlueprintFactTable):
    __tablename__ = 'owid'
    __mapper_args__ = {'concrete': True}
    __table_args__ = (
        db.UniqueConstraint('date_reported_id', 'location_id', name="uix_owid"),
    )

    def __repr__(self):
        return "%s(%s %s)" % (self.__class__.__name__, self.date_reported.__repr__(), self.location.__repr__())

    id = db.Column(db.Integer, primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False, index=True)
    processed_full_update = db.Column(db.Boolean, nullable=False, index=True)
    #
    date_reported_id = db.Column(db.Integer, db.ForeignKey('all_date_reported.id'), nullable=False, index=True)
    date_reported = db.relationship(
        'OwidDateReported',
        lazy='joined',
        cascade='save-update',
        order_by='desc(OwidDateReported.datum)')
    location_id = db.Column(db.Integer, db.ForeignKey('all_location.id'), nullable=False, index=True)
    location = db.relationship(
        'OwidCountry',
        lazy='joined',
        cascade='save-update',
        order_by='asc(OwidCountry.location)')
    #
    total_cases = db.Column(db.Float, nullable=False, index=True)
    new_cases = db.Column(db.Float, nullable=False, index=True)
    new_cases_smoothed = db.Column(db.Float, nullable=False)
    total_deaths = db.Column(db.Float, nullable=False, index=True)
    new_deaths = db.Column(db.Float, nullable=False, index=True)
    new_deaths_smoothed = db.Column(db.Float, nullable=False)
    total_cases_per_million = db.Column(db.Float, nullable=False, index=True)
    new_cases_per_million = db.Column(db.Float, nullable=False, index=True)
    new_cases_smoothed_per_million = db.Column(db.Float, nullable=False, index=True)
    total_deaths_per_million = db.Column(db.Float, nullable=False, index=True)
    new_deaths_per_million = db.Column(db.Float, nullable=False, index=True)
    new_deaths_smoothed_per_million = db.Column(db.Float, nullable=False)
    reproduction_rate = db.Column(db.Float, nullable=False)
    icu_patients = db.Column(db.Float, nullable=False)
    icu_patients_per_million = db.Column(db.Float, nullable=False)
    hosp_patients = db.Column(db.Float, nullable=False)
    hosp_patients_per_million = db.Column(db.Float, nullable=False)
    weekly_icu_admissions = db.Column(db.Float, nullable=False)
    weekly_icu_admissions_per_million = db.Column(db.Float, nullable=False)
    weekly_hosp_admissions = db.Column(db.Float, nullable=False)
    weekly_hosp_admissions_per_million = db.Column(db.Float, nullable=False)
    new_tests = db.Column(db.Float, nullable=False)
    total_tests = db.Column(db.Float, nullable=False)
    total_tests_per_thousand = db.Column(db.Float, nullable=False)
    new_tests_per_thousand = db.Column(db.Float, nullable=False)
    new_tests_smoothed = db.Column(db.Float, nullable=False)
    new_tests_smoothed_per_thousand = db.Column(db.Float, nullable=False)
    positive_rate = db.Column(db.Float, nullable=False)
    tests_per_case = db.Column(db.Float, nullable=False)
    tests_units = db.Column(db.String(255), nullable=False)
    total_vaccinations = db.Column(db.Float, nullable=False)
    people_vaccinated = db.Column(db.Float, nullable=False)
    people_fully_vaccinated = db.Column(db.Float, nullable=False)
    new_vaccinations = db.Column(db.Float, nullable=False)
    new_vaccinations_smoothed = db.Column(db.Float, nullable=False)
    total_vaccinations_per_hundred = db.Column(db.Float, nullable=False)
    people_vaccinated_per_hundred = db.Column(db.Float, nullable=False)
    people_fully_vaccinated_per_hundred = db.Column(db.Float, nullable=False)
    new_vaccinations_smoothed_per_million = db.Column(db.Float, nullable=False)
    stringency_index = db.Column(db.Float, nullable=False)

    @classmethod
    def __query_by_location(cls, location: OwidCountry):
        return db.session.query(cls).filter(
            cls.location_id == location.id
        ).populate_existing().options(
            joinedload(cls.location).joinedload(OwidCountry.location_group),
            joinedload(cls.date_reported)
        )

    @classmethod
    def __query_by_date_reported(cls, date_reported: OwidDateReported):
        return db.session.query(cls).filter(
            cls.date_reported_id == date_reported.id
        ).populate_existing().options(
            joinedload(cls.location).joinedload(OwidCountry.location_group),
            joinedload(cls.date_reported)
        )

    @classmethod
    def find_by_location(cls, location: OwidCountry):
        return cls.__query_by_location(location)\
            .order_by(cls.date_reported.datum.desc())\
            .all()

    @classmethod
    def get_by_location(cls, location: OwidCountry, page: int):
        return cls.__query_by_location(location) \
            .paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def delete_by_location(cls, location: OwidCountry):
        cls.__query_by_location(location).delete()
        db.session.commit()
        return None

    @classmethod
    def find_by_date_reported(cls, date_reported: OwidDateReported):
        return cls.__query_by_date_reported(date_reported).order_by(
                cls.new_deaths_per_million.desc(),
                cls.new_cases_per_million.desc(),
                cls.new_deaths.desc(),
                cls.new_cases.desc(),
            ).all()

    @classmethod
    def get_by_date_reported(cls, date_reported: OwidDateReported, page: int):
        return cls.__query_by_date_reported(date_reported).order_by(
                cls.new_deaths_per_million.desc(),
                cls.new_cases_per_million.desc(),
                cls.new_deaths.desc(),
                cls.new_cases.desc(),
            ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_date_reported_order_by_deaths_new(cls, date_reported: OwidDateReported, page: int):
        return cls.__query_by_date_reported(date_reported).order_by(
            cls.new_deaths.desc(),
            cls.new_deaths_per_million.desc(),
            cls.new_cases.desc(),
            cls.new_cases_per_million.desc(),
        ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_date_reported_order_by_deaths_cumulative(cls, date_reported: OwidDateReported, page: int):
        return cls.__query_by_date_reported(date_reported).order_by(
            cls.new_deaths_per_million.desc(),
            cls.new_deaths.desc(),
            cls.new_cases_per_million.desc(),
            cls.new_cases.desc(),
        ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_date_reported_order_by_cases_new(cls, date_reported: OwidDateReported, page: int):
        return cls.__query_by_date_reported(date_reported).order_by(
            cls.new_cases.desc(),
            cls.new_cases_per_million.desc(),
            cls.new_deaths.desc(),
            cls.new_deaths_per_million.desc(),
        ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_date_reported_order_by_cases_cumulative(cls, date_reported: OwidDateReported, page: int):
        return cls.__query_by_date_reported(date_reported).order_by(
            cls.new_cases_per_million.desc(),
            cls.new_cases.desc(),
            cls.new_deaths_per_million.desc(),
            cls.new_deaths.desc(),
        ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def delete_data_for_one_day(cls, date_reported: OwidDateReported):
        for data in cls.find_by_date_reported(date_reported):
            db.session.delete(data)
        db.session.delete(date_reported)
        db.session.commit()

