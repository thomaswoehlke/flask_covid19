from app_config.database import app
from data_all.all_config import BlueprintConfig


class WhoTestService:
    def __init__(self, database, who_service):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" WHO Test Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.__who_service = who_service
        self.cfg = BlueprintConfig.create_config_for_who()
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" WHO Test Service [ready]")
        app.logger.debug("------------------------------------------------------------")
