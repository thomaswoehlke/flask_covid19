from project.app_config.database import db
from project.data_all.all_model_flat import AllFlat


class OwidFlat(AllFlat):
    __tablename__ = "owid_import_flat"
    __mapper_args__ = {"concrete": True}

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id})"

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


class OwidFlatFactory:
    @classmethod
    def create_new(cls, d, row):
        f = OwidFlat(
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
            location=row["location"],
            location_group=row["continent"],
            location_code=row["iso_code"],
            processed_update=False,
            processed_full_update=False,
            #
            total_cases=0.0 if "" == row["total_cases"] else float(row["total_cases"]),
            new_cases=0.0 if "" == row["new_cases"] else float(row["new_cases"]),
            new_cases_smoothed=0.0
            if "" == row["new_cases_smoothed"]
            else float(row["new_cases_smoothed"]),
            total_deaths=0.0
            if "" == row["total_deaths"]
            else float(row["total_deaths"]),
            new_deaths=0.0 if "" == row["new_deaths"] else float(row["new_deaths"]),
            new_deaths_smoothed=0.0
            if "" == row["new_deaths_smoothed"]
            else float(row["new_deaths_smoothed"]),
            total_cases_per_million=0.0
            if "" == row["total_cases_per_million"]
            else float(row["total_cases_per_million"]),
            new_cases_per_million=0.0
            if "" == row["new_cases_per_million"]
            else float(row["new_cases_per_million"]),
            new_cases_smoothed_per_million=0.0
            if "" == row["new_cases_smoothed_per_million"]
            else float(row["new_cases_smoothed_per_million"]),
            total_deaths_per_million=0.0
            if "" == row["total_deaths_per_million"]
            else float(row["total_deaths_per_million"]),
            new_deaths_per_million=0.0
            if "" == row["new_deaths_per_million"]
            else float(row["new_deaths_per_million"]),
            new_deaths_smoothed_per_million=0.0
            if "" == row["new_deaths_smoothed_per_million"]
            else float(row["new_deaths_smoothed_per_million"]),
            reproduction_rate=0.0
            if "" == row["reproduction_rate"]
            else float(row["reproduction_rate"]),
            icu_patients=0.0
            if "" == row["icu_patients"]
            else float(row["icu_patients"]),
            icu_patients_per_million=0.0
            if "" == row["icu_patients_per_million"]
            else float(row["icu_patients_per_million"]),
            hosp_patients=0.0
            if "" == row["hosp_patients"]
            else float(row["hosp_patients"]),
            hosp_patients_per_million=0.0
            if "" == row["hosp_patients_per_million"]
            else float(row["hosp_patients_per_million"]),
            weekly_icu_admissions=0.0
            if "" == row["weekly_icu_admissions"]
            else float(row["weekly_icu_admissions"]),
            weekly_icu_admissions_per_million=0.0
            if "" == row["weekly_icu_admissions_per_million"]
            else float(row["weekly_icu_admissions_per_million"]),
            weekly_hosp_admissions=0.0
            if "" == row["weekly_hosp_admissions"]
            else float(row["weekly_hosp_admissions"]),
            weekly_hosp_admissions_per_million=0.0
            if "" == row["weekly_hosp_admissions_per_million"]
            else float(row["weekly_hosp_admissions_per_million"]),
            new_tests=0.0 if "" == row["new_tests"] else float(row["new_tests"]),
            total_tests=0.0 if "" == row["total_tests"] else float(row["total_tests"]),
            total_tests_per_thousand=0.0
            if "" == row["total_tests_per_thousand"]
            else float(row["total_tests_per_thousand"]),
            new_tests_per_thousand=0.0
            if "" == row["new_tests_per_thousand"]
            else float(row["new_tests_per_thousand"]),
            new_tests_smoothed=0.0
            if "" == row["new_tests_smoothed"]
            else float(row["new_tests_smoothed"]),
            new_tests_smoothed_per_thousand=0.0
            if "" == row["new_tests_smoothed_per_thousand"]
            else float(row["new_tests_smoothed_per_thousand"]),
            positive_rate=0.0
            if "" == row["positive_rate"]
            else float(row["positive_rate"]),
            tests_per_case=0.0
            if "" == row["tests_per_case"]
            else float(row["tests_per_case"]),
            tests_units=row["tests_units"],
            total_vaccinations=0.0
            if "" == row["total_vaccinations"]
            else float(row["total_vaccinations"]),
            people_vaccinated=0.0
            if "" == row["people_vaccinated"]
            else float(row["people_vaccinated"]),
            people_fully_vaccinated=0.0
            if "" == row["people_fully_vaccinated"]
            else float(row["people_fully_vaccinated"]),
            new_vaccinations=0.0
            if "" == row["new_vaccinations"]
            else float(row["new_vaccinations"]),
            new_vaccinations_smoothed=0.0
            if "" == row["new_vaccinations_smoothed"]
            else float(row["new_vaccinations_smoothed"]),
            total_vaccinations_per_hundred=0.0
            if "" == row["total_vaccinations_per_hundred"]
            else float(row["total_vaccinations_per_hundred"]),
            people_vaccinated_per_hundred=0.0
            if "" == row["people_vaccinated_per_hundred"]
            else float(row["people_vaccinated_per_hundred"]),
            people_fully_vaccinated_per_hundred=0.0
            if "" == row["people_vaccinated_per_hundred"]
            else float(row["people_vaccinated_per_hundred"]),
            new_vaccinations_smoothed_per_million=0.0
            if "" == row["new_vaccinations_smoothed_per_million"]
            else float(row["new_vaccinations_smoothed_per_million"]),
            stringency_index=0.0
            if "" == row["stringency_index"]
            else float(row["stringency_index"]),
            population=0.0 if "" == row["population"] else float(row["population"]),
            population_density=0.0
            if "" == row["population_density"]
            else float(row["population_density"]),
            median_age=0.0 if "" == row["median_age"] else float(row["median_age"]),
            aged_65_older=0.0
            if "" == row["aged_65_older"]
            else float(row["aged_65_older"]),
            aged_70_older=0.0
            if "" == row["aged_70_older"]
            else float(row["aged_70_older"]),
            gdp_per_capita=0.0
            if "" == row["gdp_per_capita"]
            else float(row["gdp_per_capita"]),
            extreme_poverty=0.0
            if "" == row["extreme_poverty"]
            else float(row["extreme_poverty"]),
            cardiovasc_death_rate=0.0
            if "" == row["cardiovasc_death_rate"]
            else float(row["cardiovasc_death_rate"]),
            diabetes_prevalence=0.0
            if "" == row["diabetes_prevalence"]
            else float(row["diabetes_prevalence"]),
            female_smokers=0.0
            if "" == row["female_smokers"]
            else float(row["female_smokers"]),
            male_smokers=0.0
            if "" == row["male_smokers"]
            else float(row["male_smokers"]),
            handwashing_facilities=0.0
            if "" == row["handwashing_facilities"]
            else float(row["handwashing_facilities"]),
            hospital_beds_per_thousand=0.0
            if "" == row["hospital_beds_per_thousand"]
            else float(row["hospital_beds_per_thousand"]),
            life_expectancy=0.0
            if "" == row["life_expectancy"]
            else float(row["life_expectancy"]),
            human_development_index=0.0
            if "" == row["human_development_index"]
            else float(row["human_development_index"]),
        )
        return f
