from flask_covid19_conf.database import app
from flask_covid19_app_all.all_config import BlueprintConfig


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
