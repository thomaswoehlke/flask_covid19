from project.data.database import app
from project.data_all.services.all_config import BlueprintConfig


class EcdcTestService:
    def __init__(self, database, ecdc_service):
        self.__database = database
        self.__ecdc_service = ecdc_service
        self.cfg = BlueprintConfig.create_config_for_ecdc()
        app.logger.info(" ready: [ECDC] Test Service ")
