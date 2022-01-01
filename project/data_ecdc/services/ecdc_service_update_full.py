from project.app_bootstrap.database import app
from project.app_bootstrap.database import db
from project.data_all.all_model_date_reported_factory import (
    BlueprintDateReportedFactory,
)
from project.data_all.framework.services.all_service_update_full_mixins import (
    AllServiceMixinUpdateFull,
)
from project.data_all.task.all_task_model import Task
from project.data_ecdc.model.ecdc_model import EcdcDateReported
from project.data_ecdc.model.ecdc_model_data import EcdcData
from project.data_ecdc.model.ecdc_model_data import EcdcDataFactory
from project.data_ecdc.model.ecdc_model_import import EcdcImport
from project.data_ecdc.model.ecdc_model_location import EcdcCountry
from project.data_ecdc.model.ecdc_model_location import EcdcCountryFactory
from project.data_ecdc.model.ecdc_model_location_group import EcdcContinent
from project.data_ecdc.model.ecdc_model_location_group import EcdcContinentFactory
from project.data_ecdc.services.ecdc_service_update import EcdcServiceUpdateBase


class EcdcServiceUpdateFull(EcdcServiceUpdateBase, AllServiceMixinUpdateFull):
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
            o = BlueprintDateReportedFactory.create_new_object_for_ecdc(
                my_date_reported=my_date_rep
            )
            db.session.add(o)
            a = str(o)
            b = str(k)
            app.logger.info(
                " [ECDC] full update date_reported ... " + b + " rows ... (" + a + ")"
            )
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
            app.logger.info(
                " [ECDC] full update continent ... " + b + " rows ... (" + a + ")"
            )
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
            result_countries_of_continent = EcdcImport.get_countries_of_continent(
                my_continent
            )
            for c in result_countries_of_continent:
                k += 1
                o = EcdcCountryFactory.create_new(c, my_continent)
                a = str(o)
                b = str(k)
                app.logger.info(
                    " [ECDC] full update country  ... " + b + " rows ... (" + a + ")"
                )
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
            my_date_reported_search_str = (
                EcdcDateReported.get_date_format_from_ecdc_import_format(
                    date_reported_ecdc_import_fomat=item_date_str_from_ecdc_import_str
                )
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
            dict_date_reported_from_import[
                item_date_str_from_ecdc_import_str
            ] = my_ecdc_date_reported_obj
        return dict_date_reported_from_import

    def __get_continent_from_import(self, ecdc_import: EcdcImport):
        my_a = ecdc_import.continent_exp
        ecdc_continent = EcdcContinent.find_by_region(
            s_location_group=ecdc_import.continent_exp
        )
        if ecdc_continent in None:
            ecdc_continent = EcdcContinent(region=my_a)
            db.session.add(ecdc_continent)
            db.session.commit()
        ecdc_continent = EcdcContinent.find_by_region(my_a)
        return ecdc_continent

    def __full_update_data(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [ECDC] full update [begin]")
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
                a = ecdc_import.cumulative_number_for_14_days_of_covid19_cases_per_100000
                if (a == "") or (a is None):
                    my_cumulative_number = 0.0
                else:
                    my_cumulative_number = float(
                        ecdc_import.cumulative_number_for_14_days_of_covid19_cases_per_100000
                    )
                o = EcdcDataFactory.create_new(
                    date_reported=ecdc_datereported,
                    location=ecdc_country,
                    my_deaths=my_deaths,
                    my_cases=my_cases,
                    my_cumulative_number=my_cumulative_number,
                )
                db.session.add(o)
                d += 1
                i += 1
                k += 1
            if d % 7 == 0:
                s1 = str(i)
                s2 = str(ecdc_datereported)
                s3 = str(k)
                app.logger.info(
                    " [ECDC] full update ... "
                    + s1
                    + " rows ... "
                    + s2
                    + " ("
                    + s3
                    + ")"
                )
                k = 0
                db.session.commit()
        db.session.commit()
        app.logger.info(" [ECDC] full update ... " + str(i) + " rows total")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [ECDC] full update [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def full_update_fact_table(self):
        task = Task.create(sector="ECDC", task_name="full_update_fact_table").read()
        self.__full_update_data()
        Task.finish(task_id=task.id)
        return self

    def full_update_dimension_tables(self):
        task = Task.create(
            sector="ECDC", task_name="full_update_dimension_tables"
        ).read()
        EcdcData.remove_all()
        self.__full_update_date_reported()
        self.__full_update_country()
        Task.finish(task_id=task.id)
        return self
