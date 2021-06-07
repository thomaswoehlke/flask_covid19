from flask import flash

from database import app

from flask_covid19.blueprints.app_all.all_service_mixins import AllServiceMixin
from flask_covid19.blueprints.app_all.all_config import BlueprintConfig
from flask_covid19.blueprints.app_all.all_service_download import BlueprintDownloadService
from flask_covid19.blueprints.data_ecdc.ecdc_service_import import EcdcServiceImport
from flask_covid19.blueprints.data_ecdc.ecdc_service_update import EcdcServiceUpdate, EcdcServiceUpdateFull


class EcdcService(AllServiceMixin):
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" ECDC Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = BlueprintConfig.create_config_for_ecdc()
        self.service_download = BlueprintDownloadService(database, self.cfg)
        self.service_import = EcdcServiceImport(database, self.cfg)
        self.service_update = EcdcServiceUpdate(database, self.cfg)
        self.service_update_full = EcdcServiceUpdateFull(database, self.cfg)
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ECDC Service [ready] ")
        app.logger.debug("------------------------------------------------------------")

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

