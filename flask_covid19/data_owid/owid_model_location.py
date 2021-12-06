from flask_covid19.app_config.database import db
from flask_covid19.app_config.database import items_per_page
from flask_covid19.data_all.all_model_location import AllLocation
from flask_covid19.data_owid.owid_model_import import OwidImport
from flask_covid19.data_owid.owid_model_location_group import OwidContinent
from sqlalchemy import and_


class OwidCountry(AllLocation):
    __mapper_args__ = {"polymorphic_identity": "owid_location"}

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
        db.session.query(cls).filter(cls.continent == owid_continent_one).delete()
        db.session.delete(owid_continent_one)
        db.session.commit()
        return None

    @classmethod
    def get_germany(cls):
        iso_code = "DEU"
        location = "Germany"
        return cls.find_by_location_code_and_location(
            location_code=iso_code, location=location
        )

    @classmethod
    def get_usa(cls):
        iso_code = "USA"
        location = "United States"
        return cls.find_by_location_code_and_location(
            location_code=iso_code, location=location
        )

    @classmethod
    def get_israel(cls):
        iso_code = "ISR"
        location = "Israel"
        return cls.find_by_location_code_and_location(
            location_code=iso_code, location=location
        )

    @classmethod
    def get_china(cls):
        iso_code = "CHN"
        location = "China"
        return cls.find_by_location_code_and_location(
            location_code=iso_code, location=location
        )

    @classmethod
    def get_india(cls):
        iso_code = "IND"
        location = "India"
        return cls.find_by_location_code_and_location(
            location_code=iso_code, location=location
        )

    @classmethod
    def get_brasil(cls):
        iso_code = "BRA"
        location = "Brazil"
        return cls.find_by_location_code_and_location(
            location_code=iso_code, location=location
        )

    @classmethod
    def find_all_for_data_explorer(cls):
        all_for_data_explorer = cls.find_all()
        all_for_data_explorer.insert(0, cls.get_china())
        all_for_data_explorer.insert(0, cls.get_india())
        all_for_data_explorer.insert(0, cls.get_brasil())
        all_for_data_explorer.insert(0, cls.get_usa())
        all_for_data_explorer.insert(0, cls.get_israel())
        all_for_data_explorer.insert(0, cls.get_germany())
        return all_for_data_explorer

    @classmethod
    def get_countries_for_continent(cls, owid_continent_one: OwidContinent, page: int):
        return (
            db.session.query(cls)
            .filter(cls.location_group == owid_continent_one)
            .paginate(page, per_page=items_per_page)
        )

    @classmethod
    def get_all_countries_for_continent(cls, owid_continent_one: OwidContinent):
        return (
            db.session.query(cls).filter(cls.location_group == owid_continent_one).all()
        )

    @classmethod
    def find_by_iso_code_and_location(cls, iso_code, location):
        return (
            db.session.query(cls)
            .filter(and_((cls.location_code == iso_code), (cls.location == location)))
            .one_or_none()
        )

    @classmethod
    def get_by_iso_code_and_location(cls, iso_code, location):
        return (
            db.session.query(cls)
            .filter(and_((cls.location_code == iso_code), (cls.location == location)))
            .one()
        )


class OwidCountryFactory:
    @classmethod
    def create_new(cls, oi: OwidImport, location_group: OwidContinent):
        o = OwidCountry(
            location_group=location_group,
            location=oi.location,
            location_code=oi.iso_code,
            population=0.0 if "" == oi.population else float(oi.population),
            population_density=0.0
            if "" == oi.population_density
            else float(oi.population_density),
            median_age=0.0 if "" == oi.median_age else float(oi.median_age),
            aged_65_older=0.0 if "" == oi.aged_65_older else float(oi.aged_65_older),
            aged_70_older=0.0 if "" == oi.aged_70_older else float(oi.aged_70_older),
            gdp_per_capita=0.0 if "" == oi.gdp_per_capita else float(oi.gdp_per_capita),
            extreme_poverty=0.0
            if "" == oi.extreme_poverty
            else float(oi.extreme_poverty),
            cardiovasc_death_rate=0.0
            if "" == oi.cardiovasc_death_rate
            else float(oi.cardiovasc_death_rate),
            diabetes_prevalence=0.0
            if "" == oi.diabetes_prevalence
            else float(oi.diabetes_prevalence),
            female_smokers=0.0 if "" == oi.female_smokers else float(oi.female_smokers),
            male_smokers=0.0 if "" == oi.male_smokers else float(oi.male_smokers),
            handwashing_facilities=0.0
            if "" == oi.handwashing_facilities
            else float(oi.handwashing_facilities),
            hospital_beds_per_thousand=0.0
            if "" == oi.hospital_beds_per_thousand
            else float(oi.hospital_beds_per_thousand),
            life_expectancy=0.0
            if "" == oi.life_expectancy
            else float(oi.life_expectancy),
            human_development_index=0.0
            if "" == oi.human_development_index
            else float(oi.human_development_index),
            processed_update=False,
            processed_full_update=False,
        )
        return o
