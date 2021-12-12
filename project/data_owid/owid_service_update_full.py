from project.app_bootstrap.database import app
from project.app_bootstrap.database import db
from project.data_all.all_model_date_reported_factory import (
    BlueprintDateReportedFactory,
)
from project.data_all.all_service_update_full_mixins import (
    AllServiceMixinUpdateFull,
)
from project.data_owid.owid_model_data import OwidData
from project.data_owid.owid_model_data import OwidDataFactory
from project.data_owid.owid_model_date_reported import OwidDateReported
from project.data_owid.owid_model_import import OwidImport
from project.data_owid.owid_model_location import OwidCountry
from project.data_owid.owid_model_location import OwidCountryFactory
from project.data_owid.owid_model_location_group import OwidContinent
from project.data_owid.owid_model_location_group import OwidContinentFactory
from project.data_owid.owid_service_update import OwidServiceUpdateBase


class OwidServiceUpdateFull(OwidServiceUpdateBase, AllServiceMixinUpdateFull):
    def __full_update_date_reported(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] full update date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        OwidDateReported.remove_all()
        i = 0
        log_lines = []
        for (i_date_reported,) in OwidImport.get_dates():
            i += 1
            o = BlueprintDateReportedFactory.create_new_object_for_owid(
                my_date_reported=i_date_reported
            )
            db.session.add(o)
            output = (
                " [OWID] date_reported [ " + str(i) + " ] " + i_date_reported + " added"
            )
            log_lines.append(output)
        for log_line in log_lines:
            app.logger.info(log_line)
        db.session.commit()
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] full update date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __full_update_continent(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] full update continent [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info("")
        log_lines = []
        OwidContinent.remove_all()
        i = 0
        for oi in OwidImport.get_all_continents():
            o = OwidContinentFactory.create_new(location_group_str=oi.continent)
            db.session.add(o)
            i += 1
            output = " [OWID] continent :  [ " + str(i) + " ] " + str(o) + " added"
            log_lines.append(output)
        for log_line in log_lines:
            app.logger.info(log_line)
        db.session.commit()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] full update continent [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __full_update_country(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] full update country [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info("")
        OwidData.remove_all()
        OwidCountry.remove_all()
        self.__full_update_continent()
        log_lines = []
        i = 0
        for continent in OwidContinent.find_all():
            log_lines.append("continent.region: " + continent.location_group)
            for oi in OwidImport.get_countries(continent.location_group):
                i += 1
                o = OwidCountryFactory.create_new(oi=oi, location_group=continent)
                db.session.add(o)
                output = " [OWID] country : [ " + str(i) + " ] " + str(o) + " added"
                log_lines.append(output)
        for log_line in log_lines:
            app.logger.info(log_line)
        db.session.commit()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] full update country [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __full_update_fact_table(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] full update fact_table [begin]")
        app.logger.info("------------------------------------------------------------")
        anzahl_db_zeilen_persistent = 0
        anzahl_db_zeilen_transient = 0
        lfd_nr_tage = 0
        OwidData.remove_all()
        for my_owid_date_reported in OwidDateReported.find_all():
            for oi in OwidImport.get_for_one_day(
                my_owid_date_reported.date_reported_import_str
            ):
                pers_owid_country = OwidCountry.find_by_iso_code_and_location(
                    iso_code=oi.iso_code, location=oi.location
                )
                o = OwidDataFactory.create_new(
                    oi=oi,
                    date_reported=my_owid_date_reported,
                    location=pers_owid_country,
                )
                db.session.add(o)
                anzahl_db_zeilen_persistent += 1
                anzahl_db_zeilen_transient += 1
            my_owid_date_reported.set_processed_full_update()
            db.session.add(my_owid_date_reported)
            lfd_nr_tage += 1
            if lfd_nr_tage % 7 == 0:
                db.session.commit()
                app.logger.info(
                    " [OWID] full update fact_table  "
                    + str(my_owid_date_reported)
                    + " ... "
                    + str(anzahl_db_zeilen_persistent)
                    + " rows ( "
                    + str(anzahl_db_zeilen_transient)
                    + " )"
                )
                anzahl_db_zeilen_transient = 0
        db.session.commit()
        app.logger.info(
            " [OWID] full update fact_table  :  "
            + str(anzahl_db_zeilen_persistent)
            + " rows total - for "
            + str(lfd_nr_tage)
            + " days"
        )
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] full update fact_table [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def full_update_dimension_tables(self):
        OwidData.remove_all()
        self.__full_update_date_reported()
        self.__full_update_country()
        return self

    def full_update_fact_table(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] full update fact_table [begin]")
        app.logger.info("------------------------------------------------------------")
        OwidData.remove_all()
        self.__full_update_fact_table()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] full update fact_table [done]")
        app.logger.info("------------------------------------------------------------")
        return self
