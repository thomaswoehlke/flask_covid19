from flask_covid19_conf.database import db, app  # , cache
from app_all.all_config import BlueprintConfig
from app_all.all_service_mixins import AllServiceMixinUpdate, AllServiceMixinUpdateFull
from flask_covid19_app.blueprints.app_web.web_model_factory import BlueprintDateReportedFactory
from flask_covid19_app.blueprints.data_who.who_model import WhoCountryRegion, WhoDateReported, WhoCountry, WhoData
from flask_covid19_app.blueprints.data_who.who_model_factory import WhoCountryRegionFactory, WhoCountryFactory, \
    WhoDataFactory
from flask_covid19_app.blueprints.data_who.who_model_import import WhoImport


class WhoServiceUpdateBase:
    def __init__(self, database, config: BlueprintConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" WhoServiceUpdateBase [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug("  WhoServiceUpdateBase [ready]")


class WhoServiceUpdateFull(WhoServiceUpdateBase, AllServiceMixinUpdateFull):

    def __full_update_date_reported(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WhoServiceUpdateFull.__full_update_date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        WhoDateReported.remove_all()
        # with app.app_context():
        #     cache.clear()
        log_lines = []
        i = 0
        # myresultarray = []
        # myresultset = WhoImport.get_all_datum()
        # for my_datum_item in myresultset:
        #    my_datum = my_datum_item.datum
        #    if not my_datum in myresultarray:
        #        myresultarray.append(my_datum)
        # for a in myresultset:
        #    app.logger.info(str(a))
        # for b in WhoImport.get_dates_reported_as_string_array():
        #    app.logger.info(str(b))
        for s_date_reported in WhoImport.get_dates_reported_as_string_array():
            i += 1
            o = BlueprintDateReportedFactory.create_new_object_for_who(my_date_reported=s_date_reported)
            db.session.add(o)
            output = " full update WHO date_reported ... " + str(i) + " rows ... (" + str(o) + ")"
            log_lines.append(output)
        db.session.commit()
        for log_line in log_lines:
            app.logger.info(log_line)
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WhoServiceUpdateFull.__full_update_date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __full_update_region(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WhoServiceUpdateFull.__full_update_region [begin]")
        app.logger.info("------------------------------------------------------------")
        WhoCountryRegion.remove_all()
        log_lines = []
        i = 0
        for region_str, in WhoImport.get_regions():
            i += 1
            o = WhoCountryRegionFactory.create_new(location_group_str=region_str)
            db.session.add(o)
            output = " full update WHO region ... " + str(i) + " rows ... (" + str(o) + ")"
            log_lines.append(output)
        db.session.commit()
        for log_line in log_lines:
            app.logger.info(log_line)
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WhoServiceUpdateFull.__full_update_region [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __full_update_country(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WhoServiceUpdateFull.__full_update_country [begin]")
        app.logger.info("------------------------------------------------------------")
        WhoCountry.remove_all()
        self.__full_update_region()
        # with app.app_context():
        #     cache.clear()
        log_lines = []
        i = 0
        for country_item in WhoImport.countries():
            i += 1
            str_country_code = country_item.countries.country_code
            str_country = country_item.countries.country
            str_who_region = country_item.countries.who_region
            location_group = WhoCountryRegion.find_by_location_group(location_group=str_who_region)
            o = WhoCountryFactory.create_new(
                location=str_country, location_code=str_country_code, location_group=location_group
            )
            db.session.add(o)
            output = " full update WHO country ... " + str(i) + " rows ... (" + str(o) + ")"
            log_lines.append(output)
        db.session.commit()
        for log_line in log_lines:
            app.logger.info(log_line)
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WhoServiceUpdateFull.__full_update_country [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __full_update_data(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WhoServiceUpdateFull.__full_update_data [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WhoData.remove_all() [begin]")
        WhoData.remove_all()
        # with app.app_context():
        #     cache.clear()
        app.logger.info(" WhoData.remove_all() [done]")
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
                    my_country=who_country
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
                app.logger.info(" full update WHO data ... " + str(i) + " rows ... " + s2 + " (" + str(k) + ")")
                k = 0
        db.session.commit()
        app.logger.info(" full update WHO data:  " + str(i) + " total rows")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WhoServiceUpdateFull.__full_update_data [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def full_update_dimension_tables(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WhoServiceUpdateFull.full_update_dimension_tables [begin]")
        app.logger.info("------------------------------------------------------------")
        WhoData.remove_all()
        self.__full_update_date_reported()
        self.__full_update_country()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WhoServiceUpdateFull.full_update_dimension_tables [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def full_update_fact_table(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WhoServiceUpdateFull.full_update_fact_table [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__full_update_data()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WhoServiceUpdateFull.full_update_fact_table [done]")
        app.logger.info("------------------------------------------------------------")
        return self


class WhoServiceUpdate(WhoServiceUpdateBase, AllServiceMixinUpdate):

    def __who_import_get_new_dates(self):
        todo = []
        odr_list = WhoDateReported.find_all_as_str()
        for datum_list in WhoImport.get_datum_list():
            o = datum_list['date_reported_import_str']
            app.logger.info("o: " + str(o))
            if o not in odr_list:
                todo.append(o)
        return todo

    def __get_new_location_groups(self):
        todo = []
        who_region_all = WhoCountryRegion.find_all_as_str()
        for oi in WhoImport.get_regions():
            item = oi.who_region
            if item not in who_region_all:
                todo.append(item)
        return todo

    def __get_new_locations(self):
        todo = []
        who_countries = []
        for oc in WhoCountry.find_all():
            oc_key = {
                'location_code': oc.location_code,
                'location': oc.location,
                'location_group': oc.location_group.location_group
            }
            who_countries.append(oc_key)
        for oi in WhoImport.countries():
            country = {
                'location_code': oi.countries.country_code,
                'location': oi.countries.country,
                'location_group': oi.countries.who_region
            }
            if country not in who_countries:
                todo.append(country)
        return todo

    def __update_date_reported(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WhoServiceUpdate.__update_date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        WhoDateReported.set_all_processed_update()
        i = 0
        for new_date_reported in self.__who_import_get_new_dates():
            i += 1
            output = " [ " + str(i) + " ] " + str(new_date_reported)
            o = BlueprintDateReportedFactory.create_new_object_for_who(my_date_reported=new_date_reported)
            db.session.add(o)
            db.session.commit()
            output += "   added " + str(o)
            app.logger.info(output)
        app.logger.info("")
        app.logger.info(" WhoServiceUpdate.__update_date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_location_group(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WhoServiceUpdate.__update_location_group [begin]")
        app.logger.info("------------------------------------------------------------")
        WhoCountryRegion.set_all_processed_full_update()
        i = 0
        for new_location_group in self.__get_new_location_groups():
            i += 1
            output = " [ " + str(i) + " ] " + new_location_group
            c = WhoCountryRegion.find_by_location_group(location_group=new_location_group)
            if c is None:
                o = WhoCountryRegionFactory.create_new(location_group_str=new_location_group)
                db.session.add(o)
                db.session.commit()
                output += "   added"
            else:
                output += "   NOT added ( " + str(c.id) + " ) "
            app.logger.info(output)
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WhoServiceUpdate.__update_location_group [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_location(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WhoServiceUpdate.__update_location [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__update_location_group()
        WhoCountry.set_all_processed_update()
        i = 0
        for new_location in self.__get_new_locations():
            i += 1
            i_country_code = new_location['location_code']
            i_country = new_location['location']
            i_who_region = new_location['location_group']
            output = " [ " + str(i) + " ] " + i_country_code + " | " + i_country + " | " + i_who_region + " | "
            my_region = WhoCountryRegion.find_by_location_group(i_who_region)
            o = WhoCountryFactory.create_new(
                location=i_country, location_code=i_country_code, location_group=my_region
            )
            db.session.add(o)
            db.session.commit()
            output2 = "   added ( " + str(o) + " ) "
            output += i_country_code + output2
            app.logger.info(output)
        db.session.commit()
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WhoServiceUpdate.__update_location [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_data(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WhoServiceUpdate.__update_data [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        d = 0
        k = 0
        for my_date_reported in WhoDateReported.find_by_not_processed_update():
            for who_import in WhoImport.find_by_datum(my_date_reported.datum):
                if who_import.country_code == "":
                    my_country = WhoCountry.find_by_location(who_import.country)
                else:
                    my_country = WhoCountry.find_by_location_code(who_import.country_code)
                o = WhoDataFactory.create_new(
                    my_who_import=who_import,
                    my_date=my_date_reported,
                    my_country=my_country)
                db.session.add(o)
                i += 1
                k += 1
            d += 1
            if d % 7 == 0:
                db.session.commit()
                app.logger.info(" update WHO  " + str(my_date_reported) + " ... " + str(i) + " rows ( " + str(k) + " )")
                k = 0
        db.session.commit()
        app.logger.info(" update WHO incremental :  " + str(i) + " rows total")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WhoServiceUpdate.__update_data [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_dimension_tables(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" update_dimension_tables_only [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__update_date_reported()
        self.__update_location()
        app.logger.info(" update_dimension_tables_only [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_fact_table(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" update_fact_table_only [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__update_data()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" update_fact_table_only [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def delete_last_day(self):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" WhoServiceUpdate.delete_last_day() [START]")
        app.logger.debug("------------------------------------------------------------")
        joungest_datum = WhoDateReported.get_joungest_datum()
        app.logger.info(" joungest_datum:")
        app.logger.info(str(joungest_datum))
        app.logger.info(" WhoData.find_by_date_reported(joungest_datum):")
        i = 0
        for data in WhoData.find_by_date_reported(joungest_datum):
            i += 1
            line = " WHO: to be deleted [ " + str(i) + " ] " + str(data)
            app.logger.info(line)
        app.logger.info(" WhoData.delete_data_for_one_day(joungest_datum)")
        WhoData.delete_data_for_one_day(joungest_datum)
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" WhoServiceUpdate.delete_last_day() [DONE]")
        app.logger.debug("------------------------------------------------------------")
        return self
