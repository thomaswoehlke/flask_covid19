from project.data.database import app
from project.data_all.services.all_config import BlueprintConfig


class WhoTestService:
    def __init__(self, database, who_service):
        self.__database = database
        self.__who_service = who_service
        self.cfg = BlueprintConfig.create_config_for_who()
        app.logger.info(" ready: [WHO] Test Service ")
