from project.data.database import app
from project.data.database import db
from project.data_all.model.all_model import AllDateReportedFactory
from project.data_all.services.all_service import AllServiceBase
from project.data_all.services.all_service_config import AllServiceConfig
from project.data_all.services.all_service_mixins import (
    AllServiceMixinUpdateFull,
)
from project.data_all_notifications.notifications_model import Notification
from project.data_who.model.who_model_data import WhoData
from project.data_who.model.who_model_data import WhoDataFactory
from project.data_who.model.who_model_date_reported import WhoDateReported
from project.data_who.model.who_model_import import WhoImport
from project.data_who.model.who_model_location import WhoCountry
from project.data_who.model.who_model_location import WhoCountryFactory
from project.data_who.model.who_model_location_group import WhoCountryRegion
from project.data_who.model.who_model_location_group import WhoCountryRegionFactory


class WhoServiceUpdateFull(AllServiceBase, AllServiceMixinUpdateFull):

    def __init__(self, database, config: AllServiceConfig):
        super().__init__(database, config)
        app.logger.info(" ready [{}] {} ".format(
            self.cfg, self.__class__.__name__
        ))

    def __full_update_date_reported(self):
        task = Notification.create(sector="WHO", task_name="__full_update_date_reported")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [WHO] full update date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        WhoDateReported.remove_all()
        log_lines = []
        i = 0
        for s_date_reported in WhoImport.get_dates_reported_as_string_array():
            i += 1
            o = AllDateReportedFactory.create_new_object_for_who(
                my_date_reported=s_date_reported
            )
            db.session.add(o)
            output = (
                " [WHO] full update date_reported ... "
                + str(i)
                + " rows ... ("
                + str(o)
                + ")"
            )
            log_lines.append(output)
        db.session.commit()
        for log_line in log_lines:
            app.logger.info(log_line)
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [WHO] full update date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        Notification.finish(task_id=task.id)
        return self

    def __full_update_region(self):
        task = Notification.create(sector="WHO", task_name="__full_update_region")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [WHO] full update region [begin]")
        app.logger.info("------------------------------------------------------------")
        WhoCountryRegion.remove_all()
        log_lines = []
        i = 0
        for (region_str,) in WhoImport.get_regions():
            i += 1
            o = WhoCountryRegionFactory.create_new(location_group_str=region_str)
            db.session.add(o)
            output = (
                " [WHO] full update region ... " + str(i) + " rows ... (" + str(o) + ")"
            )
            log_lines.append(output)
        db.session.commit()
        for log_line in log_lines:
            app.logger.info(log_line)
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [WHO] full update region [done]")
        app.logger.info("------------------------------------------------------------")
        Notification.finish(task_id=task.id)
        return self

    def __full_update_country(self):
        task = Notification.create(sector="WHO", task_name="__full_update_country")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [WHO] full update country [begin]")
        app.logger.info("------------------------------------------------------------")
        WhoCountry.remove_all()
        self.__full_update_region()
        log_lines = []
        i = 0
        for country_item in WhoImport.countries():
            i += 1
            str_country_code = country_item.countries.country_code
            str_country = country_item.countries.country
            str_who_region = country_item.countries.who_region
            location_group = WhoCountryRegion.find_by_location_group(
                location_group=str_who_region
            )
            o = WhoCountryFactory.create_new(
                location=str_country,
                location_code=str_country_code,
                location_group=location_group,
            )
            db.session.add(o)
            output = (
                " [WHO] full update country ... "
                + str(i)
                + " rows ... ("
                + str(o)
                + ")"
            )
            log_lines.append(output)
        db.session.commit()
        for log_line in log_lines:
            app.logger.info(log_line)
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [WHO] full update country [done]")
        app.logger.info("------------------------------------------------------------")
        Notification.finish(task_id=task.id)
        return self

    def __full_update_data(self):
        task = Notification.create(sector="WHO", task_name="__full_update_data")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [WHO] full update [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [WHO] WhoData.remove_all() [begin]")
        WhoData.remove_all()
        # with app.app_context():
        #     cache.clear()
        app.logger.info(" [WHO] WhoData.remove_all() [done]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        d = 0
        k = 0
        who_country_dict = WhoCountry.find_all_as_dict()
        for who_date_reported in WhoDateReported.find_all():
            # app.logger.info(" my_date: " + str(my_date))
            for who_import in WhoImport.find_by_datum(who_date_reported.datum):
                # app.logger.info("who_country: " + str(who_country))
                who_country = who_country_dict[who_import.country]
                o = WhoDataFactory.create_new(
                    my_who_import=who_import,
                    my_date=who_date_reported,
                    my_country=who_country,
                )
                db.session.add(o)
                i += 1
                k += 1
                who_import.processed_full_update = True
            who_date_reported.processed_full_update = True
            d += 1
            if d % 7 == 0:
                db.session.commit()
                s2 = str(who_date_reported)
                app.logger.info(
                    " [WHO] full update ... "
                    + str(i)
                    + " rows ... "
                    + s2
                    + " ("
                    + str(k)
                    + ")"
                )
                k = 0
        db.session.commit()
        app.logger.info(" [WHO] full update:  " + str(i) + " total rows")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [WHO] full update [done]")
        app.logger.info("------------------------------------------------------------")
        Notification.finish(task_id=task.id)
        return self

    def full_update_dimension_tables(self):
        task = Notification.create(sector="WHO", task_name="full_update_dimension_tables")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [WHO] full update dimension_tables [begin]")
        app.logger.info("------------------------------------------------------------")
        WhoData.remove_all()
        self.__full_update_date_reported()
        self.__full_update_country()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [WHO] full update dimension_tables [done]")
        app.logger.info("------------------------------------------------------------")
        Notification.finish(task_id=task.id)
        return self

    def full_update_fact_table(self):
        task = Notification.create(sector="WHO", task_name="full_update_fact_table")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [WHO] full update fact table [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__full_update_data()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [WHO] full update fact table [done]")
        app.logger.info("------------------------------------------------------------")
        Notification.finish(task_id=task.id)
        return self
