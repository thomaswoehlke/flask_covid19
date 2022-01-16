from project.data.database import app
from project.data_all.services.all_service_config import AllServiceConfig


class EcdcTestService:
    def __init__(self, database, ecdc_service):
        self.__database = database
        self.__ecdc_service = ecdc_service
        self.cfg = AllServiceConfig.create_config_for_ecdc()
        app.logger.info(
            " ready [{}] {} ".format(
                self.cfg.category,
                self.__class__.__name__
            )
        )
