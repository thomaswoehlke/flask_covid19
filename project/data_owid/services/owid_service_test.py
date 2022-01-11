from project.data_all.data_all_notifications.notifications_model import Task
from project.app_bootstrap.database import app
from project.app_bootstrap.database import db
from project.data_all.all_config import BlueprintConfig
from project.data_owid.model.owid_model_data import OwidData
from project.data_owid.model.owid_model_import import OwidImport
from project.data_owid.model.owid_model_location import OwidCountry
from project.data_owid.model.owid_model_location_group import OwidContinent


class OwidTestService:
    def __init__(self, database, owid_service):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" OWID Test Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.__owid_service = owid_service
        self.cfg = BlueprintConfig.create_config_for_owid()
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ready: [OWID] Test Service ")
        app.logger.debug("------------------------------------------------------------")

    def full_update_dimension_tables(self):
        task = Task.create(sector="OWID", task_name='full_update_dimension_tables')
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" OwidTestService.full_update_dimension_tables() [START]")
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug("")
        OwidData.remove_all()
        OwidCountry.remove_all()
        for continent in OwidContinent.get_all():
            app.logger.info("continent.region: " + continent.region)
            for oi in OwidImport.get_countries_for_continent(continent.region):
                app.logger.info(
                    "continent.region: "
                    + continent.region
                    + " - oi.location: "
                    + oi.location
                )
                o = OwidCountry(
                    continent_id=continent.id,
                    continent=continent,
                    location=oi.location,
                    iso_code=oi.iso_code,
                    population=oi.population,
                    population_density=oi.population_density,
                    median_age=oi.median_age,
                    aged_65_older=oi.aged_65_older,
                    aged_70_older=oi.aged_70_older,
                    gdp_per_capita=oi.gdp_per_capita,
                    extreme_poverty=oi.extreme_poverty,
                    cardiovasc_death_rate=oi.cardiovasc_death_rate,
                    diabetes_prevalence=oi.diabetes_prevalence,
                    female_smokers=oi.female_smokers,
                    male_smokers=oi.male_smokers,
                    handwashing_facilities=oi.handwashing_facilities,
                    hospital_beds_per_thousand=oi.hospital_beds_per_thousand,
                    life_expectancy=oi.life_expectancy,
                    human_development_index=oi.human_development_index,
                )
                db.session.add(o)
        db.session.commit()
        app.logger.debug("")
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" OwidTestService.full_update_dimension_tables() [DONE]")
        app.logger.debug("------------------------------------------------------------")
        Task.finish(task_id=task.id)
        return self
