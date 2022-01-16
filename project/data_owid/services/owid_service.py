from project.data.database import app
from project.data_all.services.all_service_config import AllServiceConfig
from project.data_all.services.all_service_download import AllDownloadService
from project.data_all.services.all_service_mixins import AllServiceMixin

from project.data_all_notifications.notifications_model import Notification
from project.data_owid.services.owid_service_import import OwidServiceImport
from project.data_owid.services.owid_service_update import OwidServiceUpdate
from project.data_owid.services.owid_service_update_full import OwidServiceUpdateFull


class OwidService(AllServiceMixin):
    def __init__(self, database):
        self.__database = database
        self.cfg = AllServiceConfig.create_config_for_owid()
        self.service_download = AllDownloadService(database, self.cfg)
        self.service_import = OwidServiceImport(database, self.cfg)
        self.service_update = OwidServiceUpdate(database, self.cfg)
        self.service_update_full = OwidServiceUpdateFull(database, self.cfg)
        app.logger.info(
            " ready [{}] {} ".format(
                self.cfg.category,
                self.__class__.__name__
            )
        )

    def download(self):
        task = Notification.create(sector="OWID", task_name="download")
        self.service_download.download()
        Notification.finish(task_id=task.id)
        return self

    def count_file_rows(self):
        return self.service_import.count_file_rows()

    def import_file(self):
        task = Notification.create(sector="OWID", task_name="import_file")
        self.service_import.import_file()
        Notification.finish(task_id=task.id)
        return self

    def full_update_dimension_tables(self):
        task = Notification.create(sector="OWID", task_name="full_update_dimension_tables")
        self.service_update_full.full_update_dimension_tables()
        Notification.finish(task_id=task.id)
        return self

    def update_dimension_tables(self):
        task = Notification.create(sector="OWID", task_name="update_dimension_tables")
        self.service_update.update_dimension_tables()
        Notification.finish(task_id=task.id)
        return self

    def full_update_fact_table(self):
        task = Notification.create(sector="OWID", task_name="full_update_fact_table")
        self.service_update_full.full_update_fact_table()
        Notification.finish(task_id=task.id)
        return self

    def update_fact_table(self):
        task = Notification.create(sector="OWID", task_name="update_fact_table")
        self.service_update.update_fact_table()
        Notification.finish(task_id=task.id)
        return self

    def full_update(self):
        task = Notification.create(sector="OWID", task_name="full_update")
        self.service_import.import_file()
        self.service_update_full.full_update_dimension_tables()
        self.service_update_full.full_update_fact_table()
        Notification.finish(task_id=task.id)
        return self

    def update(self):
        task = Notification.create(sector="OWID", task_name="update")
        # self.service_import.import_file()
        self.service_update.update_dimension_tables()
        self.service_update.update_fact_table()
        Notification.finish(task_id=task.id)
        return self

    def delete_last_day(self):
        task = Notification.create(sector="OWID", task_name="delete_last_day")
        self.service_update.delete_last_day()
        Notification.finish(task_id=task.id)
        return self
