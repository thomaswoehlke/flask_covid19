from project.data.database import app
from project.data.database import db
from project.data_all import AllDateReportedFactory
from project.data_all.services.all_service import AllServiceBase
from project.data_all.services.all_service_config import AllServiceConfig
from project.data_all.services.all_service_mixins import AllServiceMixinUpdateFull

from project.data_all_notifications.notifications_model import Notification
from project.data_owid.model.owid_model_data import OwidData
from project.data_owid.model.owid_model_data import OwidDataFactory
from project.data_owid.model.owid_model_date_reported import OwidDateReported
from project.data_owid.model.owid_model_import import OwidImport
from project.data_owid.model.owid_model_location import OwidCountry
from project.data_owid.model.owid_model_location import OwidCountryFactory
from project.data_owid.model.owid_model_location_group import OwidContinent
from project.data_owid.model.owid_model_location_group import OwidContinentFactory


class OwidServiceUpdateFull(AllServiceBase, AllServiceMixinUpdateFull):

    def __init__(self, database, config: AllServiceConfig):
        super().__init__(database, config)
        app.logger.info(
            " ready [{}] {} ".format(
                self.cfg.category,
                self.__class__.__name__
            )
        )

    def __full_update_date_reported(self):
        task = Notification.create(
            self.cfg.category,
            task_name="__full_update_date_reported"
        )
        self.__log_line()
        app.logger.info(" [OWID] full update date_reported [begin]")
        self.__log_line()
        OwidDateReported.remove_all()
        i = 0
        log_lines = []
        for (i_date_reported,) in OwidImport.get_dates():
            i += 1
            o = AllDateReportedFactory.create_new_object_for_owid(
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
        self.__log_line()
        app.logger.info(" [OWID] full update date_reported [done]")
        self.__log_line()
        Notification.finish(task_id=task.id)
        return self

    def __full_update_continent(self):
        task = Notification.create(
            self.cfg.category,
            task_name="__full_update_continent"
        )
        self.__log_line()
        app.logger.info(" [OWID] full update continent [begin]")
        self.__log_line()
        app.logger.info("")
        log_lines = []
        OwidContinent.remove_all()
        i = 0
        for oi in OwidImport.get_all_continents():
            if oi.continent is None:
                location_group_str = " "
            else:
                location_group_str = oi.continent
            o = OwidContinentFactory.create_new(location_group_str=location_group_str)
            db.session.add(o)
            i += 1
            output = " [OWID] continent :  [ " + str(i) + " ] " + str(o) + " added"
            log_lines.append(output)
        for log_line in log_lines:
            app.logger.info(log_line)
        db.session.commit()
        self.__log_line()
        app.logger.info(" [OWID] full update continent [done]")
        self.__log_line()
        Notification.finish(task_id=task.id)
        return self

    def __full_update_country(self):
        task = Notification.create(
            self.cfg.category,
            task_name="__full_update_country"
        )
        self.__log_line()
        app.logger.info(" [OWID] full update country [begin]")
        self.__log_line()
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
                output = " [OWID] country : [ " + str(i) + " ] " + str(o) + " "
                log_lines.append(output)
        for log_line in log_lines:
            app.logger.info(log_line)
        db.session.commit()
        self.__log_line()
        app.logger.info(" [OWID] full update country [done]")
        self.__log_line()
        Notification.finish(task_id=task.id)
        return self

    def __full_update_fact_table(self):
        task = Notification.create(
            self.cfg.category,
            task_name="__full_update_fact_table"
        )
        self.__log_line()
        app.logger.info(" [OWID] __full_update_fact_table [begin]")
        self.__log_line()
        anzahl_db_zeilen_persistent = 0
        anzahl_db_zeilen_transient = 0
        lfd_nr_tage = 0
        OwidData.remove_all()
        db.session.commit()
        for my_owid_date_reported in OwidDateReported.find_all():
            for oi in OwidImport.get_for_one_day(
                my_owid_date_reported.date_reported_import_str
            ):
                # app.logger.debug(" * | iso_code = "+oi.iso_code+" | location = "+oi.location+" | ")
                pers_owid_country = OwidCountry.find_by_iso_code_and_location(
                    iso_code=oi.iso_code, location=oi.location
                )
                if pers_owid_country is None:
                    pers_owid_country = OwidCountry.find_by_iso_code(
                        iso_code=oi.iso_code
                    )
                    if pers_owid_country is None:
                        pers_owid_country = OwidCountry.find_by_location(
                            location=oi.location
                        )
                        if pers_owid_country is None:
                            if oi.continent is None:
                                location_group = " "
                            else:
                                location_group = oi.continent
                            continent = OwidContinent.find_by_location_group(
                                location_group=location_group
                            )
                            pers_owid_country = OwidCountryFactory.create_new(
                                oi=oi,
                                location_group=continent
                            )
                # app.logger.debug(pers_owid_country)
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
                    " [OWID] full update "
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
            " [OWID] full update :  "
            + str(anzahl_db_zeilen_persistent)
            + " rows total - for "
            + str(lfd_nr_tage)
            + " days"
        )
        self.__log_line()
        app.logger.info(" [OWID] __full_update_fact_table [done]")
        self.__log_line()
        Notification.finish(task_id=task.id)
        return self

    def full_update_dimension_tables(self):
        task = Notification.create(
            self.cfg.category,
            task_name="full_update_dimension_tables"
        )
        OwidData.remove_all()
        self.__full_update_date_reported()
        self.__full_update_country()
        Notification.finish(task_id=task.id)
        return self

    def full_update_fact_table(self):
        task = Notification.create(
            self.cfg.category,
            task_name="full_update_fact_table"
        )
        self.__log_line()
        app.logger.info(" [OWID] full update [begin]")
        self.__log_line()
        OwidData.remove_all()
        self.__full_update_fact_table()
        self.__log_line()
        app.logger.info(" [OWID] full update [done]")
        self.__log_line()
        Notification.finish(task_id=task.id)
        return self
