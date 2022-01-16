from project.data.database import app
from project.data_all.services.all_service_config import AllServiceConfig


class WhoTestService:
    def __init__(self, database, who_service):
        self.__database = database
        self.__who_service = who_service
        self.cfg = AllServiceConfig.create_config_for_who()
        app.logger.info(
            " ready [{}] {} ".format(
                self.cfg.category,
                self.__class__.__name__
            )
        )
