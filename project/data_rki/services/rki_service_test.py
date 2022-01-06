
from sqlalchemy.orm import Bundle

from project.app_bootstrap.database import app
from project.app_bootstrap.database import db
from project.data_all.all_config import BlueprintConfig
from project.data_rki.model.rki_model_data import RkiData
from project.data_rki.model.rki_model_data_location import RkiLandkreis
from project.data_rki.model.rki_model_data_location_group import RkiBundesland
from project.data_rki.model.rki_model_import import RkiImport


class RkiTestService:
    def __init__(self, database, rki_service):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Test Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.__rki_service = rki_service
        self.cfg = BlueprintConfig.create_config_for_owid()
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ready: [RKI] Test Service ")
        app.logger.debug("------------------------------------------------------------")

    def full_update_dimension_tables(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" RkiTestService.full_update_dimension_tables() [START]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info("")
        RkiData.remove_all()
        RkiLandkreis.remove_all()
        for continent in RkiBundesland.get_all():
            app.logger.info("continent.region: " + continent.region)
            for oi in RkiImport.get_countries_for_continent(continent.region):
                app.logger.info(
                    "continent.region: "
                    + continent.region
                    + " - oi.location: "
                    + oi.location
                )
                o = RkiLandkreis(
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
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" RkiTestService.full_update_dimension_tables() [DONE]")
        app.logger.info("------------------------------------------------------------")

    def get_altersgruppe_list(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" RkiTestService.get_altersgruppe_list() [START]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info("")
        altersgruppe_list = []
        bu = Bundle("altersgruppe", RkiImport.altersgruppe)
        for altersgruppe_row in db.session.query(bu).distinct():
            item = altersgruppe_row[0][0]
            if item not in altersgruppe_list:
                altersgruppe_list.append(item)
                app.logger.info("NEW altersgruppe: " + str(item))
            else:
                app.logger.info("OLD altersgruppe: " + str(item))
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info("")
        for item in RkiImport.get_altersgruppe_list():
            app.logger.info("altersgruppe: " + str(item))
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info("")
        for item in RkiImport.get_datum_of_all_import():
            app.logger.info("get_datum_of_all_import: " + str(item))
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info("")
        for item in RkiImport.get_bundesland_list():
            app.logger.info("get_bundesland_list: " + str(item))
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info("")
        for bundesland in RkiImport.get_bundesland_list():
            app.logger.info("bundesland: " + str(bundesland))
            my_bundesland = bundesland[0]
            app.logger.info("my_bundesland: " + str(my_bundesland))
            for item in RkiImport.get_landkreis_for_bundesland(
                bundesland=my_bundesland
            ):
                app.logger.info("get_landkreis_for_bundesland: " + str(item))
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" RkiTestService.get_altersgruppe_list() [DONE]")
        app.logger.info("------------------------------------------------------------")