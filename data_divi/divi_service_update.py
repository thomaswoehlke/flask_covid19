from flask_covid19_conf.database import db, app

from data_all.all_config import BlueprintConfig
from flask_covid19_app_web.web_model_factory import BlueprintDateReportedFactory

from data_divi.divi_model import DiviRegion, DiviDateReported, DiviCountry, DiviData
from data_divi.divi_model_import import DiviImport


class DiviServiceUpdateBase:
    def __init__(self, database, config: BlueprintConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" DiviServiceUpdate [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" DiviServiceUpdate [ready]")
        app.logger.debug("------------------------------------------------------------")


class DiviServiceUpdateFull(DiviServiceUpdateBase):

    def __full_update_date_reported(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" DiviServiceUpdate.__update_date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        for i_date_reported, in DiviImport.get_dates_reported():
            i += 1
            output = " [ " + str(i) + " ] " + i_date_reported
            c = DiviDateReported.find_by_date_reported(i_date_reported)
            if c is None:
                o = BlueprintDateReportedFactory.create_new_object_for_divi(my_date_reported=i_date_reported)
                db.session.add(o)
                db.session.commit()
                output += " added"
            else:
                output += " NOT added "+str(c.id)
            app.logger.info(output)
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" DiviServiceUpdate.__update_date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __full_update_region(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" DiviServiceUpdate.__update_divi_region [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        for i_divi_region, in DiviImport.get_regions():
            i += 1
            output = " [ " + str(i) + " ] " + i_divi_region
            c = DiviRegion.find_by_region(i_divi_region)
            if c is None:
                o = DiviRegion(region=i_divi_region)
                db.session.add(o)
                db.session.commit()
                output += " added"
            else:
                output += " NOT added ( " + str(c.id) + " ) "
            app.logger.info(output)
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" DiviServiceUpdate.__update_divi_region [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __full_update_country(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" DiviServiceUpdate.__update_divi_country [begin]")
        app.logger.info("------------------------------------------------------------")
        result = DiviImport.countries()
        i = 0
        for result_item in result:
            i += 1
            i_country_code = result_item.countries.country_code
            i_country = result_item.countries.country
            i_divi_region = result_item.countries.divi_region
            output = " [ " + str(i) + " ] " + i_country_code + " | " + i_country + " | " + i_divi_region + " | "
            my_region = DiviRegion.find_by_region(i_divi_region)
            my_country = DiviCountry.find_by_country_code_and_country_and_divi_region_id(
                i_country_code, i_country, my_region
            )
            if my_country is None:
                o = DiviCountry(
                    country=i_country,
                    country_code=i_country_code,
                    region=my_region)
                db.session.add(o)
                db.session.commit()
                output2 = " added "
            else:
                output2 = " NOT added ( " + str(my_country.id) + " ) "
            output += i_country_code + output2
            app.logger.info(output)
        db.session.commit()
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" DiviServiceUpdate.__update_divi_country [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def get_new_dates_as_array_from_divi_import(self):
        new_dates_reported_from_import = []
        list_datum_of_all_divi_data = DiviData.get_datum_of_all_data()
        for item in DiviImport.get_datum_of_all_divi_import():
            if not item in list_datum_of_all_divi_data:
                new_dates_reported_from_import.append(item)
        return new_dates_reported_from_import

    def __full_update_fact_table(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" DiviServiceUpdate.__update_fact_tables_incremental [begin]")
        app.logger.info("------------------------------------------------------------")
        new_dates_reported_from_import = self.get_new_dates_as_array_from_divi_import()
        i = 0
        for my_date_reported in new_dates_reported_from_import:
            app.logger.info(my_date_reported)
            my_date = DiviDateReported.find_by_date_reported(my_date_reported)
            if my_date is None:
                myday = DiviDateReported.create_new_object_factory(my_date_reported)
                db.session.add(myday)
                db.session.commit()
            my_date = DiviDateReported.get_by_date_reported(my_date_reported)
            k = 0
            for result_item in DiviImport.get_for_one_day(my_date_reported):
                if result_item.country_code == "":
                    my_country = DiviCountry.get_by_country(result_item.country)
                else:
                    my_country = DiviCountry.get_by_country_code(result_item.country_code)
                o = DiviData(
                    cases_new=int(result_item.new_cases),
                    cases_cumulative=int(result_item.cumulative_cases),
                    deaths_new=int(result_item.new_deaths),
                    deaths_cumulative=int(result_item.cumulative_deaths),
                    date_reported=my_date,
                    country=my_country
                )
                db.session.add(o)
                i += 1
                k += 1
                if i % 2000 == 0:
                    app.logger.info(" update DIVI incremental ... "+str(i)+" rows")
            db.session.commit()
            app.logger.info(" update DIVI incremental ... " + str(i) + " rows [" + str(my_date) + "] (" + str(k) + ")")
        app.logger.info(" update DIVI incremental :  "+str(i)+" rows total")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" DiviServiceUpdate.__update_fact_tables_incremental [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __full_update_dimension_tables(self):
        self.__full_update_date_reported()
        self.__full_update_region()
        self.__full_update_country()
        return self

    def full_update_dimension_tables(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" update_dimension_tables_only [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__full_update_dimension_tables()
        app.logger.info(" update_dimension_tables_only [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def full_update_fact_table(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" update_fact_tables_initial_only [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__full_update_fact_table()
        app.logger.info(" update_fact_tables_initial_only [done]")
        app.logger.info("------------------------------------------------------------")
        return self


class DiviServiceUpdate(DiviServiceUpdateBase):

    def __update_date_reported(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" DiviServiceUpdate.__update_date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        for i_date_reported, in DiviImport.get_dates_reported():
            i += 1
            output = " [ " + str(i) + " ] " + i_date_reported
            c = DiviDateReported.find_by_date_reported(i_date_reported)
            if c is None:
                o = DiviDateReported.create_new_object_factory(my_date_rep=i_date_reported)
                db.session.add(o)
                db.session.commit()
                output += " added"
            else:
                output += " NOT added "+str(c.id)
            app.logger.info(output)
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" DiviServiceUpdate.__update_date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_region(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" DiviServiceUpdate.__update_divi_region [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        for i_divi_region, in DiviImport.get_regions():
            i += 1
            output = " [ " + str(i) + " ] " + i_divi_region
            c = DiviRegion.find_by_region(i_divi_region)
            if c is None:
                o = DiviRegion(region=i_divi_region)
                db.session.add(o)
                db.session.commit()
                output += " added"
            else:
                output += " NOT added ( " + str(c.id) + " ) "
            app.logger.info(output)
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" DiviServiceUpdate.__update_divi_region [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_country(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" DiviServiceUpdate.__update_divi_country [begin]")
        app.logger.info("------------------------------------------------------------")
        result = DiviImport.countries()
        i = 0
        for result_item in result:
            i += 1
            i_country_code = result_item.countries.country_code
            i_country = result_item.countries.country
            i_divi_region = result_item.countries.divi_region
            output = " [ " + str(i) + " ] " + i_country_code + " | " + i_country + " | " + i_divi_region + " | "
            my_region = DiviRegion.find_by_region(i_divi_region)
            my_country = DiviCountry.find_by_country_code_and_country_and_divi_region_id(
                i_country_code, i_country, my_region
            )
            if my_country is None:
                o = DiviCountry(
                    country=i_country,
                    country_code=i_country_code,
                    region=my_region)
                db.session.add(o)
                db.session.commit()
                output2 = " added "
            else:
                output2 = " NOT added ( " + str(my_country.id) + " ) "
            output += i_country_code + output2
            app.logger.info(output)
        db.session.commit()
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" DiviServiceUpdate.__update_divi_country [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def get_new_dates_as_array_from_divi_import(self):
        new_dates_reported_from_import = []
        list_datum_of_all_divi_data = DiviData.get_datum_of_all_divi_data()
        for item in DiviImport.get_datum_of_all_divi_import():
            if not item in list_datum_of_all_divi_data:
                new_dates_reported_from_import.append(item)
        return new_dates_reported_from_import

    def __update_fact_table(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" DiviServiceUpdate.__update_fact_table_initial [begin]")
        app.logger.info("------------------------------------------------------------")
        DiviData.remove_all()
        new_dates_reported_from_import = DiviImport.get_new_dates_as_array()
        i = 0
        for my_date_reported in new_dates_reported_from_import:
            my_date = DiviDateReported.find_by_date_reported(my_date_reported)
            if my_date is None:
                myday = DiviDateReported.create_new_object_factory(my_date_reported)
                db.session.add(myday)
                my_date = myday
            for result_item in DiviImport.get_for_one_day(my_date_reported):
                my_country = DiviCountry.find_by_country_code(result_item.country_code)
                o = DiviData(
                    cases_new=int(result_item.new_cases),
                    cases_cumulative=int(result_item.cumulative_cases),
                    deaths_new=int(result_item.new_deaths),
                    deaths_cumulative=int(result_item.cumulative_deaths),
                    date_reported=my_date,
                    country=my_country
                )
                db.session.add(o)
                result_item.row_imported = True
                db.session.add(result_item)
                i += 1
                if i % 2000 == 0:
                    app.logger.info(" update divi initial ... "+str(i)+" rows")
                    db.session.commit()
            db.session.commit()
        app.logger.info(" update divi initial :  "+str(i)+" total rows")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" DiviServiceUpdate.__update_fact_table_initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_dimension_tables(self):
        self.__update_date_reported()
        self.__update_region()
        self.__update_country()
        return self

    def update_dimension_tables(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" DiviServiceUpdate.update_dimension_tables_only [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__update_dimension_tables()
        app.logger.info(" DiviServiceUpdate.update_dimension_tables_only [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_fact_table(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" DiviServiceUpdate.update_fact_tables_incremental_only [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__update_fact_table()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" DiviServiceUpdate.update_fact_tables_incremental_only [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def delete_last_day(self):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" DiviServiceUpdate.delete_last_day() [START]")
        app.logger.debug("------------------------------------------------------------")
        joungest_datum_str = DiviData.get_joungest_datum()
        joungest_datum = DiviDateReported.find_by_date_reported(joungest_datum_str)
        app.logger.info("joungest_datum:")
        app.logger.info(joungest_datum)
        app.logger.info("DiviData.get_data_for_one_day(joungest_datum):")
        i = 0
        for data in DiviData.get_data_for_one_day(joungest_datum):
            i += 1
            line = " | " + str(i) + " | " + str(data.date_reported) + " | " + data.country.country + " | to be deleted"
            app.logger.info(line)
        app.logger.info("DiviData.delete_data_for_one_day(joungest_datum)")
        DiviData.delete_data_for_one_day(joungest_datum)
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" DiviServiceUpdate.delete_last_day() [DONE]")
        app.logger.debug("------------------------------------------------------------")
