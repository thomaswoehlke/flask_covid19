from flask_covid19_conf.database import app
from data_all.all_config import BlueprintConfig
from data_divi.divi_model import DiviDateReported, DiviData


class DiviTestService:
    def __init__(self, database, divi_service):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" DIVI Test Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.__service = divi_service
        self.cfg = BlueprintConfig.create_config_for_intensivregister()
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" DIVI Test Service [ready]")

    def delete_last_day(self):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" DiviTestService.delete_last_day() [START]")
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
        app.logger.debug(" DiviTestService.delete_last_day() [DONE]")
        app.logger.debug("------------------------------------------------------------")

