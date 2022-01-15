from project.data.database import app
from project.data_all.services.all_service_config import AllServiceConfig


class AllServiceBase:

    def __init__(self, database, config: AllServiceConfig):
        self.__database = database
        self.cfg = config

    def __log_line(self):
        app.logger.info("------------------------------------------------------------")
