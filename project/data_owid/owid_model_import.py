from project.app_config.database import db
from project.app_config.database import items_per_page
from project.data_all.all_model_import import AllImport
from sqlalchemy import and_
from sqlalchemy.orm import Bundle


class OwidImport(AllImport):
    __tablename__ = "owid_import"
    __mapper_args__ = {"concrete": True}

    def __repr__(self):
        return "{}({} {} {} {})".format(
            self.__class__.__name__,
            self.datum.isoformat(),
            self.date_reported_import_str,
            self.location,
            self.continent,
        )

    def __str__(self):
        return (
            self.datum.isoformat()
            + " "
            + self.iso_code
            + " "
            + self.location
            + " "
            + str(self.continent)
        )

    id = db.Column(db.Integer, primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    date_reported_import_str = db.Column(db.String(255), nullable=False, index=True)
    datum = db.Column(db.Date, nullable=False, index=True)
    #
    iso_code = db.Column(db.String(255), nullable=False)
    continent = db.Column(db.String(255), nullable=False, index=True)
    location = db.Column(db.String(255), nullable=False, index=True)
    date = db.Column(db.String(255), nullable=False)
    total_cases = db.Column(db.String(255), nullable=False)
    new_cases = db.Column(db.String(255), nullable=False)
    new_cases_smoothed = db.Column(db.String(255), nullable=False)
    total_deaths = db.Column(db.String(255), nullable=False)
    new_deaths = db.Column(db.String(255), nullable=False)
    new_deaths_smoothed = db.Column(db.String(255), nullable=False)
    total_cases_per_million = db.Column(db.String(255), nullable=False)
    new_cases_per_million = db.Column(db.String(255), nullable=False)
    new_cases_smoothed_per_million = db.Column(db.String(255), nullable=False)
    total_deaths_per_million = db.Column(db.String(255), nullable=False)
    new_deaths_per_million = db.Column(db.String(255), nullable=False)
    new_deaths_smoothed_per_million = db.Column(db.String(255), nullable=False)
    reproduction_rate = db.Column(db.String(255), nullable=False)
    icu_patients = db.Column(db.String(255), nullable=False)
    icu_patients_per_million = db.Column(db.String(255), nullable=False)
    hosp_patients = db.Column(db.String(255), nullable=False)
    hosp_patients_per_million = db.Column(db.String(255), nullable=False)
    weekly_icu_admissions = db.Column(db.String(255), nullable=False)
    weekly_icu_admissions_per_million = db.Column(db.String(255), nullable=False)
    weekly_hosp_admissions = db.Column(db.String(255), nullable=False)
    weekly_hosp_admissions_per_million = db.Column(db.String(255), nullable=False)
    new_tests = db.Column(db.String(255), nullable=False)
    total_tests = db.Column(db.String(255), nullable=False)
    total_tests_per_thousand = db.Column(db.String(255), nullable=False)
    new_tests_per_thousand = db.Column(db.String(255), nullable=False)
    new_tests_smoothed = db.Column(db.String(255), nullable=False)
    new_tests_smoothed_per_thousand = db.Column(db.String(255), nullable=False)
    positive_rate = db.Column(db.String(255), nullable=False)
    tests_per_case = db.Column(db.String(255), nullable=False)
    tests_units = db.Column(db.String(255), nullable=False)
    total_vaccinations = db.Column(db.String(255), nullable=False)
    people_vaccinated = db.Column(db.String(255), nullable=False)
    people_fully_vaccinated = db.Column(db.String(255), nullable=False)
    new_vaccinations = db.Column(db.String(255), nullable=False)
    new_vaccinations_smoothed = db.Column(db.String(255), nullable=False)
    total_vaccinations_per_hundred = db.Column(db.String(255), nullable=False)
    people_vaccinated_per_hundred = db.Column(db.String(255), nullable=False)
    people_fully_vaccinated_per_hundred = db.Column(db.String(255), nullable=False)
    new_vaccinations_smoothed_per_million = db.Column(db.String(255), nullable=False)
    stringency_index = db.Column(db.String(255), nullable=False)
    population = db.Column(db.String(255), nullable=False)
    population_density = db.Column(db.String(255), nullable=False)
    median_age = db.Column(db.String(255), nullable=False)
    aged_65_older = db.Column(db.String(255), nullable=False)
    aged_70_older = db.Column(db.String(255), nullable=False)
    gdp_per_capita = db.Column(db.String(255), nullable=False)
    extreme_poverty = db.Column(db.String(255), nullable=False)
    cardiovasc_death_rate = db.Column(db.String(255), nullable=False)
    diabetes_prevalence = db.Column(db.String(255), nullable=False)
    female_smokers = db.Column(db.String(255), nullable=False)
    male_smokers = db.Column(db.String(255), nullable=False)
    handwashing_facilities = db.Column(db.String(255), nullable=False)
    hospital_beds_per_thousand = db.Column(db.String(255), nullable=False)
    life_expectancy = db.Column(db.String(255), nullable=False)
    human_development_index = db.Column(db.String(255), nullable=False)

    @classmethod
    def get_dates(cls):
        return db.session.query(cls.date).order_by(cls.date.desc()).distinct().all()

    @classmethod
    def get_for_one_day(cls, day: str):
        return db.session.query(cls).filter(cls.date == day).all()

    @classmethod
    def get_dates_reported_as_array(cls):
        myresultarray = []
        myresultset = (
            db.session.query(cls.date)
            .order_by(cls.date.desc())
            .group_by(cls.date)
            .distinct()
        )
        for (item,) in myresultset:
            myresultarray.append(item)
        return myresultarray

    # TODO: #196 OwidImport.get_new_dates_reported_as_array() needs implementation
    @classmethod
    def get_new_dates_reported_as_array(cls):
        return cls.get_dates_reported_as_array()

    # TODO: deprecated
    @classmethod
    def get_datum_of_all_import(cls):
        return (
            db.session.query(cls.date)
            .order_by(cls.date.desc())
            .group_by(cls.date)
            .distinct()
            .all()
        )

    @classmethod
    def get_all_continents(cls):
        return (
            db.session.query(cls.continent)
            .group_by(cls.continent)
            .distinct()
            .order_by(cls.continent.asc())
            .all()
        )

    @classmethod
    def get_continents(cls, page):
        return (
            db.session.query(cls.continent)
            .group_by(cls.continent)
            .distinct()
            .order_by(cls.continent.asc())
            .paginate(page, per_page=items_per_page)
        )

    @classmethod
    def countries(cls):
        bu = Bundle("countries", cls.iso_code, cls.location, cls.continent)
        return db.session.query(bu).distinct()

    @classmethod
    def get_all_countries(cls):
        return (
            db.session.query(
                cls.location,
                cls.iso_code,
                cls.continent,
                cls.population,
                cls.population_density,
                cls.median_age,
                cls.aged_65_older,
                cls.aged_70_older,
                cls.gdp_per_capita,
                cls.extreme_poverty,
                cls.cardiovasc_death_rate,
                cls.diabetes_prevalence,
                cls.female_smokers,
                cls.male_smokers,
                cls.handwashing_facilities,
                cls.hospital_beds_per_thousand,
                cls.life_expectancy,
                cls.human_development_index,
            )
            .group_by(
                cls.location,
                cls.iso_code,
                cls.continent,
                cls.population,
                cls.population_density,
                cls.median_age,
                cls.aged_65_older,
                cls.aged_70_older,
                cls.gdp_per_capita,
                cls.extreme_poverty,
                cls.cardiovasc_death_rate,
                cls.diabetes_prevalence,
                cls.female_smokers,
                cls.male_smokers,
                cls.handwashing_facilities,
                cls.hospital_beds_per_thousand,
                cls.life_expectancy,
                cls.human_development_index,
            )
            .distinct()
            .order_by(cls.location.asc())
            .all()
        )

    @classmethod
    def get_countries(cls, continent_str):
        return (
            db.session.query(
                cls.location,
                cls.iso_code,
                cls.population,
                cls.population_density,
                cls.median_age,
                cls.aged_65_older,
                cls.aged_70_older,
                cls.gdp_per_capita,
                cls.extreme_poverty,
                cls.cardiovasc_death_rate,
                cls.diabetes_prevalence,
                cls.female_smokers,
                cls.male_smokers,
                cls.handwashing_facilities,
                cls.hospital_beds_per_thousand,
                cls.life_expectancy,
                cls.human_development_index,
            )
            .filter(cls.continent == continent_str)
            .group_by(
                cls.location,
                cls.iso_code,
                cls.population,
                cls.population_density,
                cls.median_age,
                cls.aged_65_older,
                cls.aged_70_older,
                cls.gdp_per_capita,
                cls.extreme_poverty,
                cls.cardiovasc_death_rate,
                cls.diabetes_prevalence,
                cls.female_smokers,
                cls.male_smokers,
                cls.handwashing_facilities,
                cls.hospital_beds_per_thousand,
                cls.life_expectancy,
                cls.human_development_index,
            )
            .distinct()
            .order_by(cls.location.asc())
            .all()
        )

    @classmethod
    def get_country_for(cls, iso_code, location):
        return (
            db.session.query(
                cls.location,
                cls.continent,
                cls.iso_code,
                cls.population,
                cls.population_density,
                cls.median_age,
                cls.aged_65_older,
                cls.aged_70_older,
                cls.gdp_per_capita,
                cls.extreme_poverty,
                cls.cardiovasc_death_rate,
                cls.diabetes_prevalence,
                cls.female_smokers,
                cls.male_smokers,
                cls.handwashing_facilities,
                cls.hospital_beds_per_thousand,
                cls.life_expectancy,
                cls.human_development_index,
            )
            .filter(and_((cls.iso_code == iso_code), (cls.location == location)))
            .group_by(
                cls.location,
                cls.continent,
                cls.iso_code,
                cls.population,
                cls.population_density,
                cls.median_age,
                cls.aged_65_older,
                cls.aged_70_older,
                cls.gdp_per_capita,
                cls.extreme_poverty,
                cls.cardiovasc_death_rate,
                cls.diabetes_prevalence,
                cls.female_smokers,
                cls.male_smokers,
                cls.handwashing_facilities,
                cls.hospital_beds_per_thousand,
                cls.life_expectancy,
                cls.human_development_index,
            )
            .distinct()
            .one()
        )


class OwidImportFactory:
    @classmethod
    def create_new(cls, date_reported, d, row):
        o = OwidImport(
            date_reported_import_str=date_reported,
            iso_code=row["iso_code"],
            date=date_reported,
            continent=row["continent"],
            location=row["location"],
            total_cases=row["total_cases"],
            new_cases=row["new_cases"],
            new_cases_smoothed=row["new_cases_smoothed"],
            total_deaths=row["total_deaths"],
            new_deaths=row["new_deaths"],
            new_deaths_smoothed=row["new_deaths_smoothed"],
            total_cases_per_million=row["total_cases_per_million"],
            new_cases_per_million=row["new_cases_per_million"],
            new_cases_smoothed_per_million=row["new_cases_smoothed_per_million"],
            total_deaths_per_million=row["total_deaths_per_million"],
            new_deaths_per_million=row["new_deaths_per_million"],
            new_deaths_smoothed_per_million=row["new_deaths_smoothed_per_million"],
            reproduction_rate=row["reproduction_rate"],
            icu_patients=row["icu_patients"],
            icu_patients_per_million=row["icu_patients_per_million"],
            hosp_patients=row["hosp_patients"],
            hosp_patients_per_million=row["hosp_patients_per_million"],
            weekly_icu_admissions=row["weekly_icu_admissions"],
            weekly_icu_admissions_per_million=row["weekly_icu_admissions_per_million"],
            weekly_hosp_admissions=row["weekly_hosp_admissions"],
            weekly_hosp_admissions_per_million=row[
                "weekly_hosp_admissions_per_million"
            ],
            new_tests=row["new_tests"],
            total_tests=row["total_tests"],
            total_tests_per_thousand=row["total_tests_per_thousand"],
            new_tests_per_thousand=row["new_tests_per_thousand"],
            new_tests_smoothed=row["new_tests_smoothed"],
            new_tests_smoothed_per_thousand=row["new_tests_smoothed_per_thousand"],
            positive_rate=row["positive_rate"],
            tests_per_case=row["tests_per_case"],
            tests_units=row["tests_units"],
            total_vaccinations=row["total_vaccinations"],
            people_vaccinated=row["people_vaccinated"],
            people_fully_vaccinated=row["people_fully_vaccinated"],
            new_vaccinations=row["new_vaccinations"],
            new_vaccinations_smoothed=row["new_vaccinations_smoothed"],
            total_vaccinations_per_hundred=row["total_vaccinations_per_hundred"],
            people_vaccinated_per_hundred=row["people_vaccinated_per_hundred"],
            people_fully_vaccinated_per_hundred=row[
                "people_fully_vaccinated_per_hundred"
            ],
            new_vaccinations_smoothed_per_million=row[
                "new_vaccinations_smoothed_per_million"
            ],
            stringency_index=row["stringency_index"],
            population=row["population"],
            population_density=row["population_density"],
            median_age=row["median_age"],
            aged_65_older=row["aged_65_older"],
            aged_70_older=row["aged_70_older"],
            gdp_per_capita=row["gdp_per_capita"],
            extreme_poverty=row["extreme_poverty"],
            cardiovasc_death_rate=row["cardiovasc_death_rate"],
            diabetes_prevalence=row["diabetes_prevalence"],
            female_smokers=row["female_smokers"],
            male_smokers=row["male_smokers"],
            handwashing_facilities=row["handwashing_facilities"],
            hospital_beds_per_thousand=row["hospital_beds_per_thousand"],
            life_expectancy=row["life_expectancy"],
            human_development_index=row["human_development_index"],
            datum=d.datum,
            processed_update=False,
            processed_full_update=False,
        )
        return o
