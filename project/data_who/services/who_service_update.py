from project.data.database import app
from project.data.database import db
from project.data_all.services.all_service import AllServiceBase
from project.data_all.services.all_service_config import AllServiceConfig
from project.data_all import AllDateReportedFactory
from project.data_all.services.all_service_mixins import AllServiceMixinUpdate
from project.data_all_notifications.notifications_model import Notification
from project.data_who.model.who_model_data import WhoData
from project.data_who.model.who_model_data import WhoDataFactory
from project.data_who.model.who_model_date_reported import WhoDateReported
from project.data_who.model.who_import_pandas import WhoImportPandas
from project.data_who.model.who_model_location import WhoCountry
from project.data_who.model.who_model_location import WhoCountryFactory
from project.data_who.model.who_model_location_group import WhoCountryRegion
from project.data_who.model.who_model_location_group import WhoCountryRegionFactory


class WhoServiceUpdate(AllServiceBase, AllServiceMixinUpdate):

    def __init__(self, database, config: AllServiceConfig):
        super().__init__(database, config)
        app.logger.info(
            " ready [{}] {} ".format(
                self.cfg.category,
                self.__class__.__name__
            )
        )

    def __who_import_get_new_dates(self):
        todo = []
        odr_list = WhoDateReported.find_all_as_str()
        for datum_list in WhoImportPandas.get_datum_list():
            o = datum_list["Date_reported"]
            app.logger.info("o: " + str(o))
            if o not in odr_list:
                todo.append(o)
        return todo

    def __get_new_location_groups(self):
        todo = []
        who_region_all = WhoCountryRegion.find_all_as_str()
        for oi in WhoImportPandas.get_regions():
            item = oi.who_region
            if item not in who_region_all:
                todo.append(item)
        return todo

    def __get_new_locations(self):
        todo = []
        who_countries = []
        for oc in WhoCountry.find_all():
            oc_key = {
                "location_code": oc.location_code,
                "location": oc.location,
                "location_group": oc.location_group.location_group,
            }
            who_countries.append(oc_key)
        for oi in WhoImportPandas.countries():
            country = {
                "location_code": oi.countries.country_code,
                "location": oi.countries.country,
                "location_group": oi.countries.who_region,
            }
            if country not in who_countries:
                todo.append(country)
        return todo

    def __update_date_reported(self):
        task = Notification.create(sector="WHO", task_name="__update_date_reported")
        self.log_line()
        app.logger.info(" [WHO] update date_reported [begin]")
        self.log_line()
        WhoDateReported.set_all_processed_update()
        i = 0
        for new_date_reported in self.__who_import_get_new_dates():
            i += 1
            output = " [WHO] date_reported [ " + str(i) + " ] " + str(new_date_reported)
            o = AllDateReportedFactory.create_new_object_for_who(
                my_date_reported=new_date_reported
            )
            db.session.add(o)
            db.session.commit()
            output += "   added " + str(o)
            app.logger.info(output)
        app.logger.info("")
        self.log_line()
        app.logger.info(" [WHO] update date_reported [done]")
        self.log_line()
        Notification.finish(task_id=task.id)
        return self

    def __update_location_group(self):
        task = Notification.create(sector="WHO", task_name="__update_location_group")
        self.log_line()
        app.logger.info(" [WHO] update location_group [begin]")
        self.log_line()
        WhoCountryRegion.set_all_processed_full_update()
        i = 0
        for new_location_group in self.__get_new_location_groups():
            i += 1
            output = " [WHO] location_group [ " + str(i) + " ] " + new_location_group
            c = WhoCountryRegion.find_by_location_group(
                location_group=new_location_group
            )
            if c is None:
                o = WhoCountryRegionFactory.create_new(
                    location_group_str=new_location_group
                )
                db.session.add(o)
                db.session.commit()
                output += "   added"
            else:
                output += "   NOT added ( " + str(c.id) + " ) "
            app.logger.info(output)
        app.logger.info("")
        self.log_line()
        app.logger.info(" [WHO] update location_group [done]")
        self.log_line()
        Notification.finish(task_id=task.id)
        return self

    def __update_location(self):
        task = Notification.create(sector="WHO", task_name="__update_location")
        self.log_line()
        app.logger.info(" [WHO] update location [begin]")
        self.log_line()
        self.__update_location_group()
        WhoCountry.set_all_processed_update()
        i = 0
        for new_location in self.__get_new_locations():
            i += 1
            i_country_code = new_location["location_code"]
            i_country = new_location["location"]
            i_who_region = new_location["location_group"]
            output = (
                "[WHO] location [ "
                + str(i)
                + " ] "
                + i_country_code
                + " | "
                + i_country
                + " | "
                + i_who_region
                + " | "
            )
            my_region = WhoCountryRegion.find_by_location_group(i_who_region)
            o = WhoCountryFactory.create_new(
                location=i_country,
                location_code=i_country_code,
                location_group=my_region,
            )
            db.session.add(o)
            db.session.commit()
            output2 = "   added ( " + str(o) + " ) "
            output += i_country_code + output2
            app.logger.info(output)
        db.session.commit()
        app.logger.info("")
        self.log_line()
        app.logger.info(" [WHO] update location [done]")
        self.log_line()
        Notification.finish(task_id=task.id)
        return self

    def __update_data(self):
        task = Notification.create(sector="WHO", task_name="__update_data")
        self.log_line()
        app.logger.info(" [WHO] update data [begin]")
        self.log_line()
        i = 0
        d = 0
        k = 0
        for my_date_reported in WhoDateReported.find_by_not_processed_update():
            for who_import in WhoImportPandas.find_by_datum(my_date_reported.datum):
                if who_import.country_code == "":
                    my_country = WhoCountry.find_by_location(who_import.country)
                else:
                    my_country = WhoCountry.find_by_location_code(
                        who_import.country_code
                    )
                o = WhoDataFactory.create_new(
                    my_who_import=who_import,
                    my_date=my_date_reported,
                    my_country=my_country,
                )
                db.session.add(o)
                i += 1
                k += 1
            d += 1
            if d % 7 == 0:
                db.session.commit()
                app.logger.info(
                    " [WHO] update data  "
                    + str(my_date_reported)
                    + " ... "
                    + str(i)
                    + " rows ( "
                    + str(k)
                    + " )"
                )
                k = 0
        db.session.commit()
        app.logger.info(" [WHO] update data :  " + str(i) + " rows total")
        app.logger.info("")
        self.log_line()
        app.logger.info(" [WHO] update data [done]")
        self.log_line()
        Notification.finish(task_id=task.id)
        return self

    def update_dimension_tables(self):
        task = Notification.create(sector="WHO", task_name="update_dimension_tables")
        self.log_line()
        app.logger.info(" [WHO] update dimension_tables [begin]")
        self.log_line()
        self.__update_date_reported()
        self.__update_location()
        app.logger.info("")
        self.log_line()
        app.logger.info(" [WHO] update dimension_tables [done]")
        self.log_line()
        Notification.finish(task_id=task.id)
        return self

    def update_fact_table(self):
        task = Notification.create(sector="WHO", task_name="update_fact_table")
        self.log_line()
        app.logger.info(" [WHO] update fact_table [begin]")
        self.log_line()
        self.__update_data()
        app.logger.info("")
        self.log_line()
        app.logger.info(" [WHO] update fact_table [done]")
        self.log_line()
        Notification.finish(task_id=task.id)
        return self

    def delete_last_day(self):
        task = Notification.create(sector="WHO", task_name="delete_last_day")
        self.log_line()
        app.logger.debug(" [WHO] delete last_day [START]")
        self.log_line()
        joungest_datum = WhoDateReported.get_joungest_datum()
        app.logger.info(" [WHO] joungest_datum:" + str(joungest_datum))
        app.logger.info(" [WHO] WhoData.find_by_date_reported(joungest_datum):")
        i = 0
        for data in WhoData.find_by_date_reported(joungest_datum):
            i += 1
            line = " [WHO] to be deleted [ " + str(i) + " ] " + str(data)
            app.logger.info(line)
        app.logger.info(" [WHO] WhoData.delete_data_for_one_day(joungest_datum)")
        WhoData.delete_data_for_one_day(joungest_datum)
        app.logger.info("")
        self.log_line()
        app.logger.debug(" [WHO] delete last_day [DONE]")
        self.log_line()
        Notification.finish(task_id=task.id)
        return self
