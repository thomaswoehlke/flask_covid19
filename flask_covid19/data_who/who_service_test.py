from flask_covid19.app_config.database import app
from flask_covid19.data_all.all_config import BlueprintConfig


class WhoTestService:
    def __init__(self, database, who_service):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" WHO Test Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.__who_service = who_service
        self.cfg = BlueprintConfig.create_config_for_who()
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ready: [WHO] Test Service ")
        app.logger.debug("------------------------------------------------------------")
