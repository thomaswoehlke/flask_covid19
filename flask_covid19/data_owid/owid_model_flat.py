
from app_config.database import db
from data_all.all_model_import import AllFlat


class OwidFlat(AllFlat):
    __tablename__ = 'owid_import_flat'
    __mapper_args__ = {'concrete': True}

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)

    def __str__(self):
        return self.datum.isoformat() + " " + self.location_code + " " + self.location + " " + str(self.location_group)

    id = db.Column(db.Integer, primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    date_reported_import_str = db.Column(db.String(255), nullable=False, index=True)
    datum = db.Column(db.Date, nullable=False, index=True)
    location = db.Column(db.String(255), nullable=False, index=True)
    location_group = db.Column(db.String(255), nullable=False, index=True)
    location_code = db.Column(db.String(255), nullable=False)
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
    total_cases = db.Column(db.Float, nullable=False)
    new_cases = db.Column(db.Float, nullable=False)
    new_cases_smoothed = db.Column(db.Float, nullable=False)
    total_deaths = db.Column(db.Float, nullable=False)
    new_deaths = db.Column(db.Float, nullable=False)
    new_deaths_smoothed = db.Column(db.Float, nullable=False)
    total_cases_per_million = db.Column(db.Float, nullable=False)
    new_cases_per_million = db.Column(db.Float, nullable=False)
    new_cases_smoothed_per_million = db.Column(db.Float, nullable=False)
    total_deaths_per_million = db.Column(db.Float, nullable=False)
    new_deaths_per_million = db.Column(db.Float, nullable=False)
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
    population = db.Column(db.Float, nullable=False)
    population_density = db.Column(db.Float, nullable=False)
    median_age = db.Column(db.Float, nullable=False)
    aged_65_older = db.Column(db.Float, nullable=False)
    aged_70_older = db.Column(db.Float, nullable=False)
    gdp_per_capita = db.Column(db.Float, nullable=False)
    extreme_poverty = db.Column(db.Float, nullable=False)
    cardiovasc_death_rate = db.Column(db.Float, nullable=False)
    diabetes_prevalence = db.Column(db.Float, nullable=False)
    female_smokers = db.Column(db.Float, nullable=False)
    male_smokers = db.Column(db.Float, nullable=False)
    handwashing_facilities = db.Column(db.Float, nullable=False)
    hospital_beds_per_thousand = db.Column(db.Float, nullable=False)
    life_expectancy = db.Column(db.Float, nullable=False)
    human_development_index = db.Column(db.Float, nullable=False)