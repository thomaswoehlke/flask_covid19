from database import db, app
from flask_covid19.blueprints.app_all.all_config import BlueprintConfig
from flask_covid19.blueprints.app_all.all_service_mixins import AllServiceMixinUpdate, AllServiceMixinUpdateFull
from flask_covid19.blueprints.app_web.web_model_factory import BlueprintDateReportedFactory
from flask_covid19.blueprints.data_owid.owid_model import OwidDateReported, OwidData, OwidContinent, OwidCountry
from flask_covid19.blueprints.data_owid.owid_model_factories import OwidContinentFactory, OwidCountryFactory, \
    OwidDataFactory
from flask_covid19.blueprints.data_owid.owid_model_import import OwidImport


class OwidServiceUpdateBase:
    def __init__(self, database, config: BlueprintConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" OWID Service Update [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" OWID Service Update [ready]")
        app.logger.debug("------------------------------------------------------------")


class OwidServiceUpdateFull(OwidServiceUpdateBase, AllServiceMixinUpdateFull):

    def __full_update_date_reported(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" OwidServiceUpdateFull.__full_update_date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        OwidDateReported.remove_all()
        i = 0
        log_lines = []
        for i_date_reported, in OwidImport.get_dates():
            i += 1
            o = BlueprintDateReportedFactory.create_new_object_for_owid(my_date_reported=i_date_reported)
            db.session.add(o)
            output = " full update  OWID date_reported [ " + str(i) + " ] " + i_date_reported + " added"
            log_lines.append(output)
        for log_line in log_lines:
            app.logger.info(log_line)
        db.session.commit()
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" OwidServiceUpdateFull.__full_update_date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __full_update_continent(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" OwidServiceUpdate.__full_update_continent [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info("")
        log_lines = []
        OwidContinent.remove_all()
        i = 0
        for oi in OwidImport.get_all_continents():
            o = OwidContinentFactory.create_new(location_group_str=oi.continent)
            db.session.add(o)
            i += 1
            output = " full update OWID continent:  [ " + str(i) + " ] " + str(o) + " added"
            log_lines.append(output)
        for log_line in log_lines:
            app.logger.info(log_line)
        db.session.commit()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" OwidServiceUpdate.__full_update_continent [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __full_update_country(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" OwidServiceUpdate.__full_update_country [begin]")
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
                output = " full update OWID country: [ " + str(i) + " ] " + str(o) + " added"
                log_lines.append(output)
        for log_line in log_lines:
            app.logger.info(log_line)
        db.session.commit()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" OwidServiceUpdate.__full_update_country [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __full_update_fact_table(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" OwidServiceUpdate.__full_update_fact_table [begin]")
        app.logger.info("------------------------------------------------------------")
        anzahl_db_zeilen_persistent = 0
        anzahl_db_zeilen_transient = 0
        lfd_nr_tage = 0
        OwidData.remove_all()
        for my_owid_date_reported in OwidDateReported.find_all():
            for oi in OwidImport.get_for_one_day(my_owid_date_reported.date_reported_import_str):
                pers_owid_country = OwidCountry.find_by_iso_code_and_location(
                    iso_code=oi.iso_code,
                    location=oi.location
                )
                o = OwidDataFactory.create_new(oi=oi, date_reported=my_owid_date_reported, location=pers_owid_country)
                db.session.add(o)
                anzahl_db_zeilen_persistent += 1
                anzahl_db_zeilen_transient += 1
            my_owid_date_reported.set_processed_full_update()
            db.session.add(my_owid_date_reported)
            lfd_nr_tage += 1
            if lfd_nr_tage % 7 == 0:
                db.session.commit()
                app.logger.info(" full update OWID  "
                                + str(my_owid_date_reported) + " ... "
                                + str(anzahl_db_zeilen_persistent)
                                + " rows ( " + str(anzahl_db_zeilen_transient) + " )")
                anzahl_db_zeilen_transient = 0
        db.session.commit()
        app.logger.info(" full update OWID  :  "+str(anzahl_db_zeilen_persistent) +" rows total - for "+str(lfd_nr_tage)+" days")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" OwidServiceUpdate.__full_update_fact_table [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def full_update_dimension_tables(self):
        OwidData.remove_all()
        self.__full_update_date_reported()
        self.__full_update_country()
        return self

    def full_update_fact_table(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" OwidServiceUpdateFull.update_fact_table_initial_only [begin]")
        app.logger.info("------------------------------------------------------------")
        OwidData.remove_all()
        self.__full_update_fact_table()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" OwidServiceUpdateFull.update_fact_table_initial_only [done]")
        app.logger.info("------------------------------------------------------------")
        return self


class OwidServiceUpdate(OwidServiceUpdateBase, AllServiceMixinUpdate):

    def __owid_import_get_new_dates(self):
        todo = []
        odr_list = OwidDateReported.get_all_str()
        for datum_list in OwidImport.get_datum_list():
            o = datum_list['date_reported_import_str']
            app.logger.info("o: " + str(o))
            if o not in odr_list:
                todo.append(o)
        return todo

    def __get_new_continents(self):
        todo = []
        owid_continent_all = OwidContinent.get_all_str()
        for oi in OwidImport.get_all_continents():
            item = oi.continent
            if item not in owid_continent_all:
                todo.append(item)
        return todo

    def __get_new_countries_from_import(self):
        todo = []
        owid_countries = []
        for oc in OwidCountry.find_all():
            oc_key = (
                oc.location_code,
                oc.location,
                oc.location_group.location_group
            )
            owid_countries.append(oc_key)
        for oi in OwidImport.get_all_countries():
            country = (
                oi.iso_code,
                oi.location,
                oi.continent
            )
            if country not in owid_countries:
                todo.append(country)
        return todo

    def __update_date_reported(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" OwidServiceUpdate.__update_date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        log_lines = []
        OwidDateReported.set_all_processed_update()
        for i_date_reported in self.__owid_import_get_new_dates():
            # app.logger.info(i_date_reported)
            i += 1
            o = BlueprintDateReportedFactory.create_new_object_for_owid(my_date_reported=i_date_reported)
            db.session.add(o)
            output = " added OwidDateReported: [ " + str(i) + " ] " + str(o) + " "
            log_lines.append(output)
        for log_line in log_lines:
            app.logger.info(log_line)
        db.session.commit()
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" OwidServiceUpdate.__update_date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_continent(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" OwidServiceUpdate.__update_continent [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info("")
        i = 0
        log_lines = []
        for continent in self.__get_new_continents():
            i += 1
            o = OwidContinentFactory.create_new(location_group_str=continent)
            db.session.add(o)
            output = " added OwidContinent: [ " + str(i) + " ] " + str(o) + " "
            log_lines.append(output)
        for log_line in log_lines:
            app.logger.info(log_line)
        db.session.commit()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" OwidServiceUpdate.__update_continent [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_country(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" OwidServiceUpdate.__update_country [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info("")
        self.__update_continent()
        for ci in self.__get_new_countries_from_import():
            iso_code = ci[0]
            location = ci[1]
            continent = ci[2]
            # app.logger.info("iso_code: " + iso_code + " - location: " + location + " - continent: " + continent)
            oi = OwidImport.get_country_for(iso_code=iso_code, location=location)
            owid_continent = OwidContinent.find_by_location_group(location_group=continent)
            o = OwidCountryFactory.create_new(oi=oi, location_group=owid_continent)
            db.session.add(o)
            app.logger.info("added OwidCountry: " + str(o) + " ")
        db.session.commit()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" OwidServiceUpdate.__update_country [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_fact_table(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" OwidServiceUpdate.__update_fact_table [begin]")
        app.logger.info("------------------------------------------------------------")
        anzahl_db_zeilen_persistent = 0
        anzahl_db_zeilen_transient = 0
        lfd_nr_tage = 0
        for unprocessed_owid_date_reported in OwidDateReported.find_by_not_processed_update():
            unprocessed_owid_date_reported.set_processed_update()
            app.logger.info("unprocessed_date: " + str(unprocessed_owid_date_reported))
            for oi in OwidImport.get_for_one_day(unprocessed_owid_date_reported.date_reported_import_str):
                owid_country = OwidCountry.find_by_iso_code_and_location(
                    iso_code=oi.iso_code,
                    location=oi.location
                )
                o = OwidDataFactory.create_new(
                    oi=oi,
                    date_reported=unprocessed_owid_date_reported,
                    location=owid_country)
                db.session.add(o)
                anzahl_db_zeilen_persistent += 1
                anzahl_db_zeilen_transient += 1
            lfd_nr_tage += 1
            if lfd_nr_tage % 7 == 0:
                db.session.commit()
                app.logger.info(
                    " update OWID  :  added OwidData " + str(unprocessed_owid_date_reported)
                    + " ... " + str(anzahl_db_zeilen_persistent)
                    + " rows ( " + str(anzahl_db_zeilen_transient)
                    + " )")
                anzahl_db_zeilen_transient = 0
        db.session.commit()
        app.logger.info(" update OWID  :  added OwidData "
                        + str(anzahl_db_zeilen_persistent)
                        + " rows total - for "+str(lfd_nr_tage)+" days")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" OwidServiceUpdate.__update_fact_table [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_dimension_tables(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" OwidServiceUpdate.update_dimension_tables [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__update_date_reported()
        self.__update_country()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" OwidServiceUpdate.update_dimension_tables [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_fact_table(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" OwidServiceUpdate.update_fact_table_incremental_only [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__update_fact_table()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" OwidServiceUpdate.update_fact_table_incremental_only [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def delete_last_day(self):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" OwidTestService.delete_last_day() [START]")
        app.logger.debug("------------------------------------------------------------")
        joungest_datum = OwidDateReported.get_joungest_datum()
        app.logger.info("joungest_datum:")
        app.logger.info(joungest_datum)
        app.logger.info("OwidData.get_data_for_one_day(joungest_datum):")
        i = 0
        for data in OwidData.find_by_date_reported(joungest_datum):
            i += 1
            line = "Owid: to be deleted | " + str(i) + " | " + str(data.date_reported) + " | " + str(data.location) + " | "
            app.logger.info(line)
        app.logger.info("OwidData.delete_data_for_one_day(joungest_datum)")
        OwidData.delete_data_for_one_day(joungest_datum)
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" OwidTestService.delete_last_day() [DONE]")
        app.logger.debug("------------------------------------------------------------")
        return self
