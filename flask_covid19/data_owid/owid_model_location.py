
from sqlalchemy import and_
from app_config.database import db, items_per_page
from data_all.all_model_location import AllLocation
from data_owid.owid_model_location_group import OwidContinent


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
        return db.session.query(cls).filter(cls.location_group == owid_continent_one).paginate(page, per_page=items_per_page)

    @classmethod
    def get_all_countries_for_continent(cls, owid_continent_one: OwidContinent):
        return db.session.query(cls).filter(cls.location_group == owid_continent_one).all()

    @classmethod
    def find_by_iso_code_and_location(cls, iso_code, location):
        return db.session.query(cls).filter(and_((cls.location_code == iso_code), (cls.location == location))).one_or_none()

    @classmethod
    def get_by_iso_code_and_location(cls, iso_code, location):
        return db.session.query(cls).filter(and_((cls.location_code == iso_code), (cls.location == location))).one()
