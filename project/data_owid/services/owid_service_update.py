from project.app_bootstrap.database import app
from project.app_bootstrap.database import db
from project.data_all.all_config import BlueprintConfig
from project.data_all.all_model_date_reported_factory import (
    BlueprintDateReportedFactory,
)
from project.data_all.framework.services.all_service_update_mixins import AllServiceMixinUpdate
from project.data_all.task.all_task_model import Task
from project.data_owid.model.owid_model_data import OwidData
from project.data_owid.model.owid_model_data import OwidDataFactory
from project.data_owid.model.owid_model_date_reported import OwidDateReported
from project.data_owid.model.owid_model_import import OwidImport
from project.data_owid.model.owid_model_location import OwidCountry
from project.data_owid.model.owid_model_location import OwidCountryFactory
from project.data_owid.model.owid_model_location_group import OwidContinent
from project.data_owid.model.owid_model_location_group import OwidContinentFactory


class OwidServiceUpdateBase:
    def __init__(self, database, config: BlueprintConfig):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.debug(" OWID Service Update [init]")
        app.logger.debug("-----------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("-----------------------------------------------------------")
        app.logger.debug(" ready: [OWID] Service Update ")
        app.logger.debug("-----------------------------------------------------------")


class OwidServiceUpdate(OwidServiceUpdateBase, AllServiceMixinUpdate):
    def __owid_import_get_new_dates(self):
        todo = []
        odr_list = OwidDateReported.find_all_as_str()
        for datum_list in OwidImport.get_datum_list():
            o = datum_list["date_reported_import_str"]
            # app.logger.info("o: " + str(o))
            if o not in odr_list:
                todo.append(o)
        return todo

    def __get_new_continents(self):
        todo = []
        owid_continent_all = OwidContinent.find_all_as_str()
        for oi in OwidImport.get_all_continents():
            item = oi.continent
            if item not in owid_continent_all:
                todo.append(item)
        return todo

    def __get_new_countries_from_import(self):
        todo = []
        owid_countries = []
        for oc in OwidCountry.find_all():
            oc_key = (oc.location_code, oc.location, oc.location_group.location_group)
            owid_countries.append(oc_key)
        for oi in OwidImport.get_all_countries():
            country = (oi.iso_code, oi.location, oi.continent)
            if country not in owid_countries:
                todo.append(country)
        return todo

    def __update_date_reported(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] update date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        log_lines = []
        OwidDateReported.set_all_processed_update()
        for i_date_reported in self.__owid_import_get_new_dates():
            # app.logger.info(i_date_reported)
            i += 1
            o = BlueprintDateReportedFactory.create_new_object_for_owid(
                my_date_reported=i_date_reported
            )
            db.session.add(o)
            output = " [OWID] date_reported [ " + str(i) + " ] " + str(o) + " added"
            log_lines.append(output)
        for log_line in log_lines:
            app.logger.info(log_line)
        db.session.commit()
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] update date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_continent(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] update continent [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info("")
        i = 0
        log_lines = []
        for continent in self.__get_new_continents():
            i += 1
            o = OwidContinentFactory.create_new(location_group_str=continent)
            db.session.add(o)
            output = " [OWID] continent [ " + str(i) + " ] " + str(o) + " added"
            log_lines.append(output)
        for log_line in log_lines:
            app.logger.info(log_line)
        db.session.commit()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] update continent [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_country(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] update country [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info("")
        self.__update_continent()
        for ci in self.__get_new_countries_from_import():
            iso_code = ci[0]
            location = ci[1]
            continent = ci[2]
            # log_msg = "iso_code: " + iso_code \
            #          + " - location: " + location \
            #          + " - continent: " + continent
            # app.logger.info(log_msg)
            oi = OwidImport.get_country_for(iso_code=iso_code, location=location)
            owid_continent = OwidContinent.find_by_location_group(
                location_group=continent
            )
            o = OwidCountryFactory.create_new(oi=oi, location_group=owid_continent)
            db.session.add(o)
            app.logger.info(" [OWID] added country: " + str(o) + " ")
        db.session.commit()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] update country [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_fact_table(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] update [begin]")
        app.logger.info("------------------------------------------------------------")
        anzahl_db_zeilen_persistent = 0
        anzahl_db_zeilen_transient = 0
        lfd_nr_tage = 0
        for (
            unprocessed_owid_date_reported
        ) in OwidDateReported.find_by_not_processed_update():
            unprocessed_owid_date_reported.set_processed_update()
            app.logger.info(
                " [OWID] unprocessed_date: " + str(unprocessed_owid_date_reported)
            )
            for oi in OwidImport.get_for_one_day(
                unprocessed_owid_date_reported.date_reported_import_str
            ):
                owid_country = OwidCountry.find_by_iso_code_and_location(
                    iso_code=oi.iso_code, location=oi.location
                )
                o = OwidDataFactory.create_new(
                    oi=oi,
                    date_reported=unprocessed_owid_date_reported,
                    location=owid_country,
                )
                db.session.add(o)
                anzahl_db_zeilen_persistent += 1
                anzahl_db_zeilen_transient += 1
            lfd_nr_tage += 1
            if lfd_nr_tage % 7 == 0:
                db.session.commit()
                app.logger.info(
                    " [OWID] update  :  added data "
                    + str(unprocessed_owid_date_reported)
                    + " ... "
                    + str(anzahl_db_zeilen_persistent)
                    + " rows ( "
                    + str(anzahl_db_zeilen_transient)
                    + " )"
                )
                anzahl_db_zeilen_transient = 0
        db.session.commit()
        app.logger.info(
            " [OWID] update  :  added data "
            + str(anzahl_db_zeilen_persistent)
            + " rows total - for "
            + str(lfd_nr_tage)
            + " days"
        )
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] update [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_dimension_tables(self):
        task = Task.create(sector="OWID", task_name="update_dimension_tables").read()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] update dimension_tables [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__update_date_reported()
        self.__update_country()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] update dimension_tables [done]")
        app.logger.info("------------------------------------------------------------")
        Task.finish(task_id=task.id)
        return self

    def update_fact_table(self):
        task = Task.create(sector="OWID", task_name="update_fact_table").read()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] update fact_table [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__update_fact_table()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] update fact_table [done]")
        app.logger.info("------------------------------------------------------------")
        Task.finish(task_id=task.id)
        return self

    def delete_last_day(self):
        task = Task.create(sector="OWID", task_name="delete_last_day").read()
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" [OWID] delete last_day [START]")
        app.logger.debug("------------------------------------------------------------")
        joungest_datum = OwidDateReported.get_joungest_datum()
        app.logger.info(" [OWID] joungest_datum:" + str(joungest_datum))
        app.logger.info(" [OWID] OwidData.find_by_date_reported(joungest_datum):")
        i = 0
        for data in OwidData.find_by_date_reported(joungest_datum):
            i += 1
            line = " [OWID] to be deleted [ " + str(i) + " ] " + str(data)
            app.logger.info(line)
        app.logger.info(" [OWID] OwidData.delete_data_for_one_day(joungest_datum)")
        OwidData.delete_data_for_one_day(joungest_datum)
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" [OWID] delete last_day [DONE]")
        app.logger.debug("------------------------------------------------------------")
        Task.finish(task_id=task.id)
        return self
