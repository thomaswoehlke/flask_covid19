from database import app
from flask_covid19.blueprints.app_all.all_config import BlueprintConfig
from flask_covid19.blueprints.data_who.who_model import WhoDateReported, WhoData


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

    def run_update_star_schema_incremental(self):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" WhoTestService.run_update_star_schema_incremental() [START]")
        app.logger.debug("------------------------------------------------------------")
        self.__who_service.update_star_schema()
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" WhoTestService.run_update_star_schema_incremental() [DONE]")
        app.logger.debug("------------------------------------------------------------")
