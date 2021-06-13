from app_config.database import db, app
from data_all.all_config import BlueprintConfig
from data_ecdc.ecdc_model_factories import EcdcContinentFactory, EcdcCountryFactory, EcdcDataFactory
from data_ecdc.ecdc_model_import import EcdcImport
from app_web.web_model_factory import BlueprintDateReportedFactory
from data_ecdc.ecdc_model import EcdcDateReported, EcdcContinent, EcdcCountry, EcdcData


class EcdcServiceUpdateBase:
    def __init__(self, database, config: BlueprintConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" ECDC Service Update [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" [ECDC] Service Update [ready] ")
        app.logger.debug("------------------------------------------------------------")


class EcdcServiceUpdateFull(EcdcServiceUpdateBase):

    def __full_update_date_reported(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [ECDC] full update date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        EcdcDateReported.remove_all()
        result_date_rep = EcdcImport.get_date_rep()
        k = 0
        for result_item in result_date_rep:
            k += 1
            my_date_rep = result_item[0]
            o = BlueprintDateReportedFactory.create_new_object_for_ecdc(my_date_reported=my_date_rep)
            db.session.add(o)
            a = str(o)
            b = str(k)
            app.logger.info(" [ECDC] full update date_reported ... " + b + " rows ... (" + a + ")")
        db.session.commit()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [ECDC] full update date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __full_update_continent(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [ECDC] full update continent [begin]")
        app.logger.info("------------------------------------------------------------")
        EcdcContinent.remove_all()
        result_continent = EcdcImport.get_continent()
        k = 0
        for result_item in result_continent:
            k += 1
            my_continent_exp = result_item[0]
            o = EcdcContinentFactory.create_new(location_group_str=my_continent_exp)
            a = str(o)
            b = str(k)
            app.logger.info(" [ECDC] full update continent ... " + b + " rows ... (" + a + ")")
            db.session.add(o)
        db.session.commit()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [ECDC] full update continent [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __full_update_country(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [ECDC] full update country [begin]")
        app.logger.info("------------------------------------------------------------")
        EcdcData.remove_all()
        EcdcCountry.remove_all()
        self.__full_update_continent()
        all_continents = EcdcContinent.find_all()
        k = 0
        for my_continent in all_continents:
            result_countries_of_continent = EcdcImport.get_countries_of_continent(my_continent)
            for c in result_countries_of_continent:
                k += 1
                o = EcdcCountryFactory.create_new(c, my_continent)
                a = str(o)
                b = str(k)
                app.logger.info(" [ECDC] full update country  ... " + b + " rows ... (" + a + ")")
                db.session.add(o)
        db.session.commit()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [ECDC] full update country [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __get_date_reported_from_import(self):
        dict_date_reported_from_import = {}
        result_date_str_from_ecdc_import = EcdcImport.get_date_rep()
        for item_date_str_from_ecdc_import in result_date_str_from_ecdc_import:
            item_date_str_from_ecdc_import_str = str(item_date_str_from_ecdc_import[0])
            app.logger.info(item_date_str_from_ecdc_import_str)
            my_date_reported_search_str = EcdcDateReported.get_date_format_from_ecdc_import_format(
                date_reported_ecdc_import_fomat=item_date_str_from_ecdc_import_str
            )
            app.logger.debug(my_date_reported_search_str)
            my_ecdc_date_reported_obj = EcdcDateReported.find_by_date_reported(
                date_reported_import_str=my_date_reported_search_str
            )
            if my_ecdc_date_reported_obj is None:
                my_ecdc_date_reported_obj = EcdcDateReported.create_new_object_factory(
                    my_date_rep=item_date_str_from_ecdc_import_str
                )
                db.session.add(my_ecdc_date_reported_obj)
                db.session.commit()
            my_ecdc_date_reported_obj = EcdcDateReported.get_by_date_reported(
                date_reported_import_str=my_date_reported_search_str
            )
            dict_date_reported_from_import[item_date_str_from_ecdc_import_str] = my_ecdc_date_reported_obj
        return dict_date_reported_from_import

    def __get_continent_from_import(self, ecdc_import: EcdcImport):
        my_a = ecdc_import.continent_exp
        ecdc_continent = EcdcContinent.find_by_region(s_location_group=ecdc_import.continent_exp)
        if ecdc_continent in None:
            ecdc_continent = EcdcContinent(region=my_a)
            db.session.add(ecdc_continent)
            db.session.commit()
        ecdc_continent = EcdcContinent.find_by_region(my_a)
        return ecdc_continent

    def __full_update_data(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [ECDC] full update data [begin]")
        app.logger.info("------------------------------------------------------------")
        EcdcData.remove_all()
        i = 0
        k = 0
        d = 0
        for ecdc_datereported in EcdcDateReported.find_all():
            ecdc_datereported_str = ecdc_datereported.date_reported_import_str
            for ecdc_import in EcdcImport.find_by_date_reported(ecdc_datereported_str):
                ecdc_country = EcdcCountry.get_by(
                    location=ecdc_import.countries_and_territories,
                    geo_id=ecdc_import.geo_id,
                    location_code=ecdc_import.country_territory_code,
                )
                my_deaths = int(ecdc_import.deaths)
                my_cases = int(ecdc_import.cases)
                if ecdc_import.cumulative_number_for_14_days_of_covid19_cases_per_100000 == '':
                    my_cumulative_number = 0.0
                else:
                    my_cumulative_number = \
                        float(ecdc_import.cumulative_number_for_14_days_of_covid19_cases_per_100000)
                o = EcdcDataFactory.create_new(
                    date_reported=ecdc_datereported,
                    location=ecdc_country,
                    my_deaths=my_deaths,
                    my_cases=my_cases,
                    my_cumulative_number=my_cumulative_number
                )
                db.session.add(o)
                d += 1
                i += 1
                k += 1
            if d % 7 == 0:
                s1 = str(i)
                s2 = str(ecdc_datereported)
                s3 = str(k)
                app.logger.info(" [ECDC] full update data  ... " + s1 + " rows ... " + s2 + " (" + s3 + ")")
                k = 0
                db.session.commit()
        db.session.commit()
        app.logger.info(" [ECDC] full update data  ... " + str(i) + " rows total")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [ECDC] full update data [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def full_update_fact_table(self):
        self.__full_update_data()
        return self

    def full_update_dimension_tables(self):
        EcdcData.remove_all()
        self.__full_update_date_reported()
        self.__full_update_country()
        return self


class EcdcServiceUpdate(EcdcServiceUpdateBase):

    def __get_new_dates(self):
        todo = []
        odr_list = EcdcDateReported.find_all_as_str()
        for oi in EcdcImport.get_date_reported_import_str_list():
            item = oi[0]
            app.logger.info("o: " + str(item))
            if item not in odr_list:
                todo.append(item)
        return todo

    def __get_new_location_groups(self):
        todo = []
        bundesland_all = EcdcContinent.find_all_as_str()
        for oi in EcdcImport.get_bundesland_list():
            item = oi.bundesland
            app.logger.info("lg: " + str(item))
            if item not in bundesland_all:
                todo.append(item)
        return todo

    def __get_new_locations(self):
        todo = []
        country_all = EcdcCountry.find_all_as_str()
        for my_continent in EcdcContinent.find_all_as_str():
            for oi in EcdcImport.get_countries_of_continent(my_continent):
                item = oi.landkreis
                app.logger.info("l: " + str(item) + " -- " + str(my_continent))
                if item not in country_all:
                    new_location = (
                        oi.landkreis,
                        oi.id_landkreis,
                        my_continent
                    )
                    todo.append(new_location)
        return todo

    def __update_date_reported(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [ECDC] update date_reported  [begin]")
        app.logger.info("------------------------------------------------------------")
        result_date_rep = EcdcImport.get_date_rep()
        k = 0
        for result_item in result_date_rep:
            k += 1
            my_date_rep = result_item[0]
            oo = EcdcDateReported.find_by_date_reported(my_date_rep)
            if oo is None:
                o = BlueprintDateReportedFactory.create_new_object_for_ecdc(
                    my_date_reported=my_date_rep
                )
                db.session.add(o)
                db.session.commit()
            app.logger.info(" [ECDC] update date_reported " + my_date_rep + " ... " + str(k) + " rows ")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [ECDC] update date_reported  [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_continent(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [ECDC] update continent [begin]")
        app.logger.info("------------------------------------------------------------")
        result_continent = EcdcImport.get_continent()
        for result_item in result_continent:
            my_continent_exp = result_item[0]
            o = EcdcContinentFactory.create_new(location_group_str=my_continent_exp)
            app.logger.info(" [ECDC] update continent ... " + str(o) + " rows ")
            db.session.add(o)
        db.session.commit()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [ECDC] update continent [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_country(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [ECDC] update country [begin]")
        app.logger.info("------------------------------------------------------------")
        all_continents = EcdcContinent.find_all()
        for my_continent in all_continents:
            result_countries_of_continent = EcdcImport.get_countries_of_continent(my_continent)
            for c in result_countries_of_continent:
                o = EcdcCountryFactory.create_new(c, my_continent)
                app.logger.info(" [ECDC] update country " + str(o) + " ")
                db.session.add(o)
            db.session.commit()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [ECDC] update country [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __get_continent_from_import(self, ecdc_import: EcdcImport):
        my_a = ecdc_import.continent_exp
        ecdc_continent = EcdcContinent.find_by_region(my_a)
        if ecdc_continent in None:
            ecdc_continent = EcdcContinent(region=my_a)
            db.session.add(ecdc_continent)
            db.session.commit()
        ecdc_continent = EcdcContinent.find_by_region(my_a)
        return ecdc_continent

    def __get_country_from_import(self, ecdc_import: EcdcImport):
        my_countries_and_territories = ecdc_import.countries_and_territories
        my_geo_id = ecdc_import.geo_id
        my_country_territory_code = ecdc_import.country_territory_code
        my_pop_data_2019 = ecdc_import.pop_data_2019
        ecdc_country = EcdcCountry.find_by(
            location=my_countries_and_territories,
            geo_id=my_geo_id,
            location_code=my_country_territory_code
        )
        if ecdc_country is None:
            my_continent = self.__get_continent_from_import(ecdc_import)
            app.logger.info(my_continent.id + " "+my_continent.region)
            o = EcdcCountry(
                countries_and_territories=my_countries_and_territories,
                pop_data_2019=my_pop_data_2019,
                geo_id=my_geo_id,
                country_territory_code=my_country_territory_code,
                continent=my_continent
            )
            db.session.add(o)
            db.session.commit()
            ecdc_country = EcdcCountry.get_by(
                location=my_countries_and_territories,
                geo_id=my_geo_id,
                location_code=my_country_territory_code
            )
        return ecdc_country

    def __get_date_reported_from_import(self):
        dict_date_reported_from_import = {}
        result_date_str_from_ecdc_import = EcdcImport.get_date_rep()
        for item_date_str_from_ecdc_import in result_date_str_from_ecdc_import:
            item_date_str_from_ecdc_import_str = str(item_date_str_from_ecdc_import[0])
            app.logger.info(item_date_str_from_ecdc_import_str)
            my_date_reported_search_str = EcdcDateReported.get_date_format_from_ecdc_import_format(
                date_reported_ecdc_import_fomat=item_date_str_from_ecdc_import_str
            )
            app.logger.debug(my_date_reported_search_str)
            my_ecdc_date_reported_obj = EcdcDateReported.find_by_date_reported(
                date_reported_import_str=my_date_reported_search_str
            )
            if my_ecdc_date_reported_obj is None:
                my_ecdc_date_reported_obj = EcdcDateReported.create_new_object_factory(
                    my_date_rep=item_date_str_from_ecdc_import_str
                )
                db.session.add(my_ecdc_date_reported_obj)
                db.session.commit()
            my_ecdc_date_reported_obj = EcdcDateReported.get_by_date_reported(
                date_reported_import_str=my_date_reported_search_str
            )
            dict_date_reported_from_import[item_date_str_from_ecdc_import_str] = my_ecdc_date_reported_obj
        return dict_date_reported_from_import

    def update_dimension_tables(self):
        self.__update_date_reported()
        self.__update_continent()
        self.__update_country()
        return self

    def __update_data(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [ECDC] update data [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        dict_date_reported_from_import = self.__get_date_reported_from_import()
        for my_date_reported in dict_date_reported_from_import.keys():
            my_ecdc_datereported = dict_date_reported_from_import[my_date_reported]
            for item_ecdc_data_import in EcdcImport.find_by_date_reported(my_date_reported):
                my_ecdc_country = self.__get_country_from_import(item_ecdc_data_import)
                my_deaths = int(item_ecdc_data_import.deaths)
                my_cases = int(item_ecdc_data_import.cases)
                if item_ecdc_data_import.cumulative_number_for_14_days_of_covid19_cases_per_100000 == '':
                    my_cumulative_number = 0.0
                else:
                    my_cumulative_number = \
                        float(item_ecdc_data_import.cumulative_number_for_14_days_of_covid19_cases_per_100000)
                o = EcdcDataFactory.create_new(
                    date_reported=my_ecdc_datereported,
                    location=my_ecdc_country,
                    my_deaths=my_deaths,
                    my_cases=my_cases,
                    my_cumulative_number=my_cumulative_number
                )
                db.session.add(o)
                i += 1
                if i % 1000 == 0:
                    app.logger.info(" [ECDC] update data  ... " + str(i) + " rows")
                    db.session.commit()
        db.session.commit()
        app.logger.info(" [ECDC] update data  ... " + str(i) + " rows total")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [ECDC] update data [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_fact_table(self):
        self.__update_data()
        return self

    def delete_last_day(self):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" [ECDC] delete last_day [START]")
        app.logger.debug("------------------------------------------------------------")
        joungest_datum_str = EcdcData.get_joungest_datum()
        joungest_datum = EcdcDateReported.find_by_date_reported(joungest_datum_str)
        app.logger.info(" joungest_datum:")
        app.logger.info(joungest_datum)
        app.logger.info(" WhoData.get_data_for_one_day(joungest_datum):")
        i = 0
        for data in EcdcData.get_data_for_one_day(joungest_datum):
            i += 1
            line = " [ECDC] delete last_day [ " + str(i) + " ] " + str(data.date_reported) + " | " + str(data.country) + " | to be deleted"
            app.logger.info(line)
        app.logger.info(" WhoData.delete_data_for_one_day(joungest_datum)")
        EcdcData.delete_data_for_one_day(joungest_datum)
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" [ECDC] delete last_day [DONE]")
        app.logger.debug("------------------------------------------------------------")
        return self
