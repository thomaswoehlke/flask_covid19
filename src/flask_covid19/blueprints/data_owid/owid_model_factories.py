from flask_covid19 import OwidImport
from flask_covid19.blueprints.data_owid.owid_model import OwidContinent, OwidCountry, OwidDateReported, OwidData


class OwidContinentFactory:

    @classmethod
    def create_new(cls, location_group_str: str):
        o = OwidContinent(
            location_group=location_group_str,
            processed_update=False,
            processed_full_update=False,
        )
        return o


class OwidCountryFactory:

    @classmethod
    def create_new(cls, oi: OwidImport, location_group: OwidContinent):
        o = OwidCountry(
            location_group=location_group,
            location=oi.location,
            location_code=oi.iso_code,
            population=0.0 if '' == oi.population else float(oi.population),
            population_density=0.0 if '' == oi.population_density else float(oi.population_density),
            median_age=0.0 if '' == oi.median_age else float(oi.median_age),
            aged_65_older=0.0 if '' == oi.aged_65_older else float(oi.aged_65_older),
            aged_70_older=0.0 if '' == oi.aged_70_older else float(oi.aged_70_older),
            gdp_per_capita=0.0 if '' == oi.gdp_per_capita else float(oi.gdp_per_capita),
            extreme_poverty=0.0 if '' == oi.extreme_poverty else float(oi.extreme_poverty),
            cardiovasc_death_rate=0.0 if '' == oi.cardiovasc_death_rate else float(oi.cardiovasc_death_rate),
            diabetes_prevalence=0.0 if '' == oi.diabetes_prevalence else float(oi.diabetes_prevalence),
            female_smokers=0.0 if '' == oi.female_smokers else float(oi.female_smokers),
            male_smokers=0.0 if '' == oi.male_smokers else float(oi.male_smokers),
            handwashing_facilities=0.0 if '' == oi.handwashing_facilities else float(oi.handwashing_facilities),
            hospital_beds_per_thousand=0.0 if '' == oi.hospital_beds_per_thousand else float(oi.hospital_beds_per_thousand),
            life_expectancy=0.0 if '' == oi.life_expectancy else float(oi.life_expectancy),
            human_development_index=0.0 if '' == oi.human_development_index else float(oi.human_development_index),
            processed_update=False,
            processed_full_update=False,
        )
        return o


class OwidDataFactory:

    @classmethod
    def create_new(cls, oi: OwidImport, date_reported: OwidDateReported, location: OwidCountry):
        o = OwidData(
            date_reported=date_reported,
            location=location,
            total_cases=0.0 if '' == oi.total_cases else float(oi.total_cases),
            new_cases=0.0 if '' == oi.new_cases else float(oi.new_cases),
            new_cases_smoothed=0.0 if '' == oi.new_cases_smoothed else float(oi.new_cases_smoothed),
            total_deaths=0.0 if '' == oi.total_deaths else float(oi.total_deaths),
            new_deaths=0.0 if '' == oi.new_deaths else float(oi.new_deaths),
            new_deaths_smoothed=0.0 if '' == oi.new_deaths_smoothed else float(oi.new_deaths_smoothed),
            total_cases_per_million=0.0 if '' == oi.total_cases_per_million else float(oi.total_cases_per_million),
            new_cases_per_million=0.0 if '' == oi.new_cases_per_million else float(oi.new_cases_per_million),
            new_cases_smoothed_per_million=0.0 if '' == oi.new_cases_smoothed_per_million else float(oi.new_cases_smoothed_per_million),
            total_deaths_per_million=0.0 if '' == oi.total_deaths_per_million else float(oi.total_deaths_per_million),
            new_deaths_per_million=0.0 if '' == oi.new_deaths_per_million else float(oi.new_deaths_per_million),
            new_deaths_smoothed_per_million=0.0 if '' == oi.new_deaths_smoothed_per_million else float(oi.new_deaths_smoothed_per_million),
            reproduction_rate=0.0 if '' == oi.reproduction_rate else float(oi.reproduction_rate),
            icu_patients=0.0 if '' == oi.icu_patients else float(oi.icu_patients),
            icu_patients_per_million=0.0 if '' == oi.icu_patients_per_million else float(oi.icu_patients_per_million),
            hosp_patients=0.0 if '' == oi.hosp_patients else float(oi.hosp_patients),
            hosp_patients_per_million=0.0 if '' == oi.hosp_patients_per_million else float(oi.hosp_patients_per_million),
            weekly_icu_admissions=0.0 if '' == oi.weekly_icu_admissions else float(oi.weekly_icu_admissions),
            weekly_icu_admissions_per_million=0.0 if '' == oi.weekly_icu_admissions_per_million else float(oi.weekly_icu_admissions_per_million),
            weekly_hosp_admissions=0.0 if '' == oi.weekly_hosp_admissions else float(oi.weekly_hosp_admissions),
            weekly_hosp_admissions_per_million=0.0 if '' == oi.weekly_hosp_admissions_per_million else float(oi.weekly_hosp_admissions_per_million),
            new_tests=0.0 if '' == oi.new_tests else float(oi.new_tests),
            total_tests=0.0 if '' == oi.total_tests else float(oi.total_tests),
            total_tests_per_thousand=0.0 if '' == oi.total_tests_per_thousand else float(oi.total_tests_per_thousand),
            new_tests_per_thousand=0.0 if '' == oi.new_tests_per_thousand else float(oi.new_tests_per_thousand),
            new_tests_smoothed=0.0 if '' == oi.new_tests_smoothed else float(oi.new_tests_smoothed),
            new_tests_smoothed_per_thousand=0.0 if '' == oi.new_tests_smoothed_per_thousand else float(oi.new_tests_smoothed_per_thousand),
            positive_rate=0.0 if '' == oi.positive_rate else float(oi.positive_rate),
            tests_per_case=0.0 if '' == oi.tests_per_case else float(oi.tests_per_case),
            tests_units=oi.tests_units,
            total_vaccinations=0.0 if '' == oi.total_vaccinations else float(oi.total_vaccinations),
            people_vaccinated=0.0 if '' == oi.people_vaccinated else float(oi.people_vaccinated),
            people_fully_vaccinated=0.0 if '' == oi.people_fully_vaccinated else float(oi.people_fully_vaccinated),
            new_vaccinations=0.0 if '' == oi.new_vaccinations else float(oi.new_vaccinations),
            new_vaccinations_smoothed=0.0 if '' == oi.new_vaccinations_smoothed else float(oi.new_vaccinations_smoothed),
            total_vaccinations_per_hundred=0.0 if '' == oi.total_vaccinations_per_hundred else float(oi.total_vaccinations_per_hundred),
            people_vaccinated_per_hundred=0.0 if '' == oi.people_vaccinated_per_hundred else float(oi.people_vaccinated_per_hundred),
            people_fully_vaccinated_per_hundred=0.0 if '' == oi.people_fully_vaccinated_per_hundred else float(oi.people_fully_vaccinated_per_hundred),
            new_vaccinations_smoothed_per_million=0.0 if '' == oi.new_vaccinations_smoothed_per_million else float(oi.new_vaccinations_smoothed_per_million),
            stringency_index=0.0 if '' == oi.stringency_index else float(oi.stringency_index),
            processed_update=False,
            processed_full_update=False,
        )
        return o