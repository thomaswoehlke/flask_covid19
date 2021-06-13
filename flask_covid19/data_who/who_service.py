from flask_covid19_conf.database import app

from flask_covid19_app_all.all_service_mixins import AllServiceMixin
from flask_covid19_app_all.all_config import BlueprintConfig
from flask_covid19_app_all.all_service_download import AllDownloadService
from data_who.who_service_import import WhoServiceImport
from data_who.who_service_update import WhoServiceUpdate, WhoServiceUpdateFull


class WhoService(AllServiceMixin):
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" WHO Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = BlueprintConfig.create_config_for_who()
        self.service_download = AllDownloadService(database, self.cfg)
        self.service_import = WhoServiceImport(database, self.cfg)
        self.service_update = WhoServiceUpdate(database, self.cfg)
        self.service_update_full = WhoServiceUpdateFull(database, self.cfg)
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" WHO Service [ready]")

    def download(self):
        self.service_download.download()
        return self

    def import_file(self):
        self.service_import.import_file()
        return self

    def full_update_dimension_tables(self):
        self.service_update_full.full_update_dimension_tables()
        return self

    def update_dimension_tables(self):
        self.service_update.update_dimension_tables()
        return self

    def full_update_fact_table(self):
        self.service_update_full.full_update_fact_table()
        return self

    def update_fact_table(self):
        self.service_update.update_fact_table()
        return self

    def full_update(self):
        self.service_import.import_file()
        self.service_update_full.full_update_dimension_tables()
        self.service_update_full.full_update_fact_table()
        return self

    def update(self):
        self.service_import.import_file()
        self.service_update.update_dimension_tables()
        self.service_update.update_fact_table()
        return self

    def delete_last_day(self):
        self.service_update.delete_last_day()
        return self








