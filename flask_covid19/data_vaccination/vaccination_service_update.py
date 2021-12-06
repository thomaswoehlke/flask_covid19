from flask_covid19.app_config.database import app
from flask_covid19.app_config.database import db
from flask_covid19.data_all.all_config import BlueprintConfig
from flask_covid19.data_all.all_model_date_reported_factory import (
    BlueprintDateReportedFactory,
)
from flask_covid19.data_all.all_service_update_mixins import AllServiceMixinUpdate
from flask_covid19.data_vaccination.vaccination_model_data import VaccinationData
from flask_covid19.data_vaccination.vaccination_model_data import VaccinationDataFactory
from flask_covid19.data_vaccination.vaccination_model_date_reported import (
    VaccinationDateReported,
)
from flask_covid19.data_vaccination.vaccination_model_import import VaccinationImport


class VaccinationServiceUpdateBase:
    def __init__(self, database, config: BlueprintConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Vaccination Service Update [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ready: [Vaccination] Service Update")
        app.logger.debug("------------------------------------------------------------")


class VaccinationServiceUpdate(VaccinationServiceUpdateBase, AllServiceMixinUpdate):
    def __get_new_dates(self):
        todo = []
        odr_list = VaccinationDateReported.find_all_as_str()
        for oi in VaccinationImport.get_date_reported_import_str_list():
            item = oi[0]
            app.logger.info("o: " + str(item))
            if item not in odr_list:
                todo.append(item)
        return todo

    def __update_date_reported(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [Vaccination] update date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        VaccinationDateReported.set_all_processed_update()
        date_reported_list = VaccinationImport.get_date_reported_as_array()
        i = 0
        for one_date_reported in date_reported_list:
            i += 1
            output = (
                " [Vaccination] date_reported [ "
                + str(i)
                + " ] "
                + str(one_date_reported)
                + " added"
            )
            o = BlueprintDateReportedFactory.create_new_object_for_vaccination(
                one_date_reported
            )
            db.session.add(o)
            app.logger.info(output)
        db.session.commit()
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [Vaccination] update date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_fact_table(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [Vaccination] update fact_table [begin]")
        app.logger.info("------------------------------------------------------------")
        result_date_rep = VaccinationImport.get_daterep_missing_in_vaccination_data()
        i = 0
        for item_date_rep in result_date_rep:
            date_reported = VaccinationDateReported.get_by_date_reported(item_date_rep)
            for item_data_import in VaccinationImport.find_by_datum(item_date_rep):
                o = VaccinationDataFactory.create_new(date_reported, item_data_import)
                db.session.add(o)
                i += 1
                if i % 500 == 0:
                    app.logger.info(
                        " [Vaccination] update fact_table ... " + str(i) + " rows"
                    )
                    db.session.commit()
        db.session.commit()
        app.logger.info(
            " [Vaccination] update fact_table ... " + str(i) + " rows total"
        )
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [Vaccination] update fact_table [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_dimension_tables(self):
        self.__update_date_reported()
        return self

    def update_fact_table(self):
        self.__update_fact_table()
        return self

    def delete_last_day(self):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" VaccinationServiceUpdate.delete_last_day [START]")
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" not implemented")
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" VaccinationServiceUpdate.delete_last_day [DONE]")
        app.logger.debug("------------------------------------------------------------")
        return self
