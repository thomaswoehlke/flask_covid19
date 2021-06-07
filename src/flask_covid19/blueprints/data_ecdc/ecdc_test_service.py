from database import app
from flask_covid19.blueprints.app_all.all_config import BlueprintConfig


class EcdcTestService:
    def __init__(self, database, ecdc_service):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" ECDC Test Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.__ecdc_service = ecdc_service
        self.cfg = BlueprintConfig.create_config_for_ecdc()
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ECDC Test Service [ready]")

    def run_update_star_schema_incremental(self):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" EcdcTestService.run_update_star_schema_incremental() [START]")
        app.logger.debug("------------------------------------------------------------")
        self.__ecdc_service.update_star_schema()
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" EcdcTestService.run_update_star_schema_incremental() [DONE]")
        app.logger.debug("------------------------------------------------------------")
