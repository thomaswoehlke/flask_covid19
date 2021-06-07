from flask import flash

from database import app

from flask_covid19.blueprints.app_all.all_service_mixins import AllServiceMixin
from flask_covid19.blueprints.app_all.all_config import BlueprintConfig
from flask_covid19.blueprints.app_all.all_service_download import BlueprintDownloadService
from flask_covid19.blueprints.data_owid.owid_service_import import OwidServiceImport
from flask_covid19.blueprints.data_owid.owid_service_update import OwidServiceUpdate, OwidServiceUpdateFull


class OwidService(AllServiceMixin):
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" OWID Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = BlueprintConfig.create_config_for_owid()
        self.service_download = BlueprintDownloadService(database, self.cfg)
        self.service_import = OwidServiceImport(database, self.cfg)
        self.service_update = OwidServiceUpdate(database, self.cfg)
        self.service_update_full = OwidServiceUpdateFull(database, self.cfg)
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" OWID Service [ready]")

    def download(self):
        flash("OwidService.download [start]")
        # TODO self.service_download.download()
        self.service_download.download()
        flash("OwidService.download [done]")
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

