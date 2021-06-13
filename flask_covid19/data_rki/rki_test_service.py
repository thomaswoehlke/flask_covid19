from flask_covid19_conf.database import db, app
from flask_covid19_app_all.all_config import BlueprintConfig
from data_rki.rki_model import RkiData, RkiBundesland, RkiLandkreis
from data_rki.rki_model_import import RkiImport


class RkiTestService:
    def __init__(self, database, rki_service):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Test Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.__rki_service = rki_service
        self.cfg = BlueprintConfig.create_config_for_owid()
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" RKI Test Service [ready]")

    def full_update_dimension_tables(self):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RkiTestService.full_update_dimension_tables() [START]")
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug("")
        RkiData.remove_all()
        RkiLandkreis.remove_all()
        for continent in RkiBundesland.get_all():
            app.logger.info("continent.region: " + continent.region)
            for oi in RkiImport.get_countries_for_continent(continent.region):
                app.logger.info("continent.region: " + continent.region +" - oi.location: " + oi.location)
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
                    human_development_index=oi.human_development_index
                )
                db.session.add(o)
        db.session.commit()
        app.logger.debug("")
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RkiTestService.full_update_dimension_tables() [DONE]")
        app.logger.debug("------------------------------------------------------------")
