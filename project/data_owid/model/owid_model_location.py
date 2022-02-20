from sqlalchemy import not_, and_, Sequence
# from sqlalchemy.orm import subqueryload
# from datetime import date

from project.data.database import db
from project.data.database import items_per_page
# from project.data_all.model.all_model import AllLocation
from project.data_all.model.all_model_mixins import AllLocationMixin

from project.data_owid.model.owid_model_import import OwidImport
from project.data_owid.model.owid_model_location_group import OwidContinent
from sqlalchemy import and_


class OwidCountry(db.Model, AllLocationMixin):

    __tablename__ = "owid_location"
    __mapper_args__ = {"concrete": True}
    __table_args__ = (
        db.UniqueConstraint("location", name="owid_location_uix"),
    )

    id_seq = Sequence('owid_location_id_seq')
    id = db.Column(db.Integer,
                   id_seq,
                   server_default=id_seq.next_value(),
                   primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    location_code = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=False)
    location_group_id = db.Column(
        db.Integer, db.ForeignKey("owid_location_group.id"), nullable=False
    )
    location_group = db.relationship(
        "OwidContinent",
        lazy="joined",
        cascade="all",
        order_by="OwidContinent.location_group",
    )
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

    def __repr__(self):
        return "{}({} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {})".format(
            self.__class__.__name__,
            self.location_code,
            self.location,
            self.population,
            self.population_density,
            self.median_age,
            self.aged_65_older,
            self.aged_70_older,
            self.gdp_per_capita,
            self.extreme_poverty,
            self.cardiovasc_death_rate,
            self.diabetes_prevalence,
            self.female_smokers,
            self.male_smokers,
            self.handwashing_facilities,
            self.hospital_beds_per_thousand,
            self.life_expectancy,
            self.human_development_index,
        )

    def __str__(self):
        return "{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}".format(
            self.location_code,
            self.location,
            self.population,
            self.population_density,
            self.median_age,
            self.aged_65_older,
            self.aged_70_older,
            self.gdp_per_capita,
            self.extreme_poverty,
            self.cardiovasc_death_rate,
            self.diabetes_prevalence,
            self.female_smokers,
            self.male_smokers,
            self.handwashing_facilities,
            self.hospital_beds_per_thousand,
            self.life_expectancy,
            self.human_development_index,
        )

    def __init__(self,
                 location: str,
                 location_code: str,
                 location_group: OwidContinent,
                 population: float,
                 population_density: float,
                 median_age: float,
                 aged_65_older: float,
                 aged_70_older: float,
                 gdp_per_capita: float,
                 extreme_poverty: float,
                 cardiovasc_death_rate: float,
                 diabetes_prevalence: float,
                 female_smokers: float,
                 male_smokers: float,
                 handwashing_facilities: float,
                 hospital_beds_per_thousand: float,
                 life_expectancy: float,
                 human_development_index: float):
        self.location = location
        self.location_code = location_code
        self.location_group = location_group
        self.population = population
        self.population_density = population_density
        self.median_age = median_age
        self.aged_65_older = aged_65_older
        self.aged_70_older = aged_70_older
        self.gdp_per_capita = gdp_per_capita
        self.extreme_poverty = extreme_poverty
        self.cardiovasc_death_rate = cardiovasc_death_rate
        self.diabetes_prevalence = diabetes_prevalence
        self.female_smokers = female_smokers
        self.male_smokers = male_smokers
        self.handwashing_facilities = handwashing_facilities
        self.hospital_beds_per_thousand = hospital_beds_per_thousand
        self.life_expectancy = life_expectancy
        self.human_development_index = human_development_index
        self.processed_update = False
        self.processed_full_update = False

    def set_processed_update(self):
        self.processed_update = True
        return self

    def set_processed_full_update(self):
        self.processed_full_update = True
        return self

    def unset_processed_update(self):
        self.processed_update = False
        return self

    def unset_processed_full_update(self):
        self.processed_full_update = False
        return self

    @classmethod
    def delete_all_countries_for_continent(cls, owid_continent_one: OwidContinent):
        db.session.query(cls).filter(cls.location_group == owid_continent_one).delete()
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
    def find_by_iso_code(cls, iso_code):
        return (
            db.session.query(cls)
            .filter(cls.location_code == iso_code)
            .one_or_none()
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

    @classmethod
    def find_by_location_code(cls, location_code: str):
        return (
            db.session.query(cls)
            .filter(cls.location_code == location_code)
            .one_or_none()
        )

    @classmethod
    def get_by_location_code(cls, location_code: str):
        return db.session.query(cls).filter(cls.location_code == location_code).one()

    @classmethod
    def find_by_location(cls, location: str):
        return db.session.query(cls).filter(cls.location == location).one_or_none()

    @classmethod
    def get_by_location(cls, location: str):
        return db.session.query(cls).filter(cls.location == location).one()

    @classmethod
    def find_by_location_group(cls, location_group: OwidContinent):
        return (
            db.session.query(cls)
            .filter(cls.location_group == location_group)
            .order_by(cls.location)
            .all()
        )

    @classmethod
    def get_by_location_group(cls, location_group: OwidContinent, page: int):
        return (
            db.session.query(cls)
            .filter(cls.location_group == location_group)
            .order_by(cls.location)
            .paginate(page, per_page=items_per_page)
        )

    @classmethod
    def find_by_location_code_and_location_and_location_group(
        cls, location_code: str, location: str, location_group: OwidContinent
    ):
        return (
            db.session.query(cls)
            .filter(
                and_(
                    cls.location_code == location_code,
                    cls.location == location,
                    cls.location_group_id == location_group.id,
                )
            )
            .one_or_none()
        )

    @classmethod
    def get_by_location_code_and_location_and_location_group(
        cls, location_code: str, location: str, location_group: OwidContinent
    ):
        return (
            db.session.query(cls)
            .filter(
                and_(
                    cls.location_code == location_code,
                    cls.location == location,
                    cls.location_group_id == location_group.id,
                )
            )
            .one()
        )

    @classmethod
    def find_by_location_code_and_location(cls, location_code: str, location: str):
        return (
            db.session.query(cls)
            .filter(and_(cls.location_code == location_code, cls.location == location))
            .order_by(cls.location)
            .one_or_none()
        )

    @classmethod
    def get_by_location_code_and_location(cls, location_code: str, location: str):
        return (
            db.session.query(cls)
            .filter(and_(cls.location_code == location_code, cls.location == location))
            .one()
        )

    @classmethod
    def __query_all(cls):
        return db.session.query(cls).order_by(cls.location)

    @classmethod
    def find_all(cls):
        return cls.__query_all().all()

    @classmethod
    def find_all_as_str(cls):
        all_str = []
        for my_location in cls.find_all():
            all_str.append(my_location.location)
        return all_str

    @classmethod
    def find_all_as_dict(cls):
        dates_reported = {}
        for my_location in cls.find_all():
            dates_reported[my_location.location] = my_location
        return dates_reported

    @classmethod
    def get_all(cls, page: int):
        return (
            db.session.query(cls)
            .order_by(cls.location)
            .paginate(page, per_page=items_per_page)
        )

    @classmethod
    def remove_all(cls):
        db.session.query(cls).delete()
        db.session.commit()
        return None

    @classmethod
    def get_by_id(cls, other_id):
        return cls.__query_all().filter(cls.id == other_id).one()

    @classmethod
    def find_by_id(cls, other_id):
        return cls.__query_all().filter(cls.id == other_id).one_or_none()

    @classmethod
    def find_by_not_processed_update(cls):
        return cls.__query_all().filter(not_(cls.processed_update)).all()

    @classmethod
    def find_by_not_processed_full_update(cls):
        return cls.__query_all().filter(not_(cls.processed_full_update)).all()

    @classmethod
    def set_all_processed_full_update(cls):
        for o in cls.find_by_not_processed_full_update():
            o.set_processed_full_update()
        db.session.commit()

    @classmethod
    def set_all_processed_update(cls):
        for o in cls.find_by_not_processed_update():
            o.set_processed_update()
        db.session.commit()

    @classmethod
    def count(cls):
        return cls.__query_all().count()


class OwidCountryFactory:
    @classmethod
    def create_new(cls, oi: OwidImport, location_group: OwidContinent):
        o = OwidCountry(
            location_group=location_group,
            location=oi.location,
            location_code=oi.iso_code,
            population=0.0
            if "" == oi.population or oi.population is None
            else float(oi.population),
            population_density=0.0
            if "" == oi.population_density or oi.population_density is None
            else float(oi.population_density),
            median_age=0.0
            if "" == oi.median_age or oi.median_age is None
            else float(oi.median_age),
            aged_65_older=0.0
            if "" == oi.aged_65_older or oi.aged_65_older is None
            else float(oi.aged_65_older),
            aged_70_older=0.0
            if "" == oi.aged_70_older or oi.aged_70_older is None
            else float(oi.aged_70_older),
            gdp_per_capita=0.0
            if "" == oi.gdp_per_capita or oi.gdp_per_capita is None
            else float(oi.gdp_per_capita),
            extreme_poverty=0.0
            if "" == oi.extreme_poverty or oi.extreme_poverty is None
            else float(oi.extreme_poverty),
            cardiovasc_death_rate=0.0
            if "" == oi.cardiovasc_death_rate or oi.cardiovasc_death_rate is None
            else float(oi.cardiovasc_death_rate),
            diabetes_prevalence=0.0
            if "" == oi.diabetes_prevalence or oi.diabetes_prevalence is None
            else float(oi.diabetes_prevalence),
            female_smokers=0.0
            if "" == oi.female_smokers or oi.female_smokers is None
            else float(oi.female_smokers),
            male_smokers=0.0
            if "" == oi.male_smokers or oi.male_smokers is None
            else float(oi.male_smokers),
            handwashing_facilities=0.0
            if "" == oi.handwashing_facilities or oi.handwashing_facilities is None
            else float(oi.handwashing_facilities),
            hospital_beds_per_thousand=0.0
            if "" == oi.hospital_beds_per_thousand or oi.hospital_beds_per_thousand is None
            else float(oi.hospital_beds_per_thousand),
            life_expectancy=0.0
            if "" == oi.life_expectancy or oi.life_expectancy is None
            else float(oi.life_expectancy),
            human_development_index=0.0
            if "" == oi.human_development_index or oi.human_development_index is None
            else float(oi.human_development_index),
            processed_update=False,
            processed_full_update=False,
        )
        return o
