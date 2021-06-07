from flask import flash

from database import app
from flask_covid19.blueprints.app_all.all_service_mixins import AllServiceMixin
from flask_covid19.blueprints.app_all.all_config import BlueprintConfig
from flask_covid19.blueprints.app_all.all_service_download import BlueprintDownloadService
from flask_covid19.blueprints.data_rki.rki_service_import import RkiServiceImport
from flask_covid19.blueprints.data_rki.rki_service_update import RkiServiceUpdate, RkiServiceUpdateFull


class RkiService(AllServiceMixin):
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = BlueprintConfig.create_config_for_rki()
        self.service_download = BlueprintDownloadService(database, self.cfg)
        self.service_import = RkiServiceImport(database, self.cfg)
        self.service_update = RkiServiceUpdate(database, self.cfg)
        self.service_update_full = RkiServiceUpdateFull(database, self.cfg)
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" RKI Service [ready]")

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

    def full_update_star_schema(self):
        self.service_update_full.full_update_star_schema()
        return self

    def update_star_schema(self):
        self.service_update.update_star_schema()
        return self

    def full_update(self):
        self.service_import.import_file()
        self.service_update_full.full_update_star_schema()
        return self

    def update(self):
        self.service_import.import_file()
        self.service_update.update_star_schema()
        return self

    def delete_last_day(self):
        self.service_update.delete_last_day()
        return self

    def delete_last_location_group(self):
        self.service_update.delete_last_location_group()
        return self

