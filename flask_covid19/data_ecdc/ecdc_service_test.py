from flask_covid19.app_config.database import app
from flask_covid19.data_all.all_config import BlueprintConfig


class EcdcTestService:
    def __init__(self, database, ecdc_service):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" ECDC Test Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.__ecdc_service = ecdc_service
        self.cfg = BlueprintConfig.create_config_for_ecdc()
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ready: [ECDC] Test Service ")
        app.logger.debug("------------------------------------------------------------")

