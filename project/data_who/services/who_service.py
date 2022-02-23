import pandas as pd
import sqlalchemy

from project.data.database import app, covid19_application
from project.data_all.services.all_service_config import AllServiceConfig
from project.data_all.services.all_service_download import AllDownloadService
from project.data_all.services.all_service_mixins import AllServiceMixin
from project.data_all_notifications.notifications_model import Notification
from project.data_who.model.who_model_date_reported import WhoDateReported
from project.data_who.model.who_model_import_dao import WhoImportDao
from project.data_who.services.who_service_import import WhoServiceImport
from project.data_who.services.who_service_update import WhoServiceUpdate
from project.data_who.services.who_service_update_full import WhoServiceUpdateFull


class WhoService(AllServiceMixin):
    def __init__(self, database):
        self.__database = database
        self.cfg = AllServiceConfig.create_config_for_who()
        self.service_download = AllDownloadService(database, self.cfg)
        self.service_import = WhoServiceImport(database, self.cfg)
        self.service_update = WhoServiceUpdate(database, self.cfg)
        self.service_update_full = WhoServiceUpdateFull(database, self.cfg)
        app.logger.info(
            " ready [{}] {} ".format(
                self.cfg.category,
                self.__class__.__name__
            )
        )

    def download(self):
        task = Notification.create(
            sector=self.cfg.category,
            task_name="download"
        )
        self.service_download.download()
        Notification.finish(task_id=task.id)
        return self

    def get_file_date(self):
        return "01.01.2022"

    def count_file_rows(self):
        return self.service_import.count_file_rows()

    def import_file(self):
        task = Notification.create(
            sector=self.cfg.category,
            task_name="import_file"
        )
        self.service_import.import_file()
        Notification.finish(task_id=task.id)
        return self

    def full_update_dimension_tables(self):
        n = Notification.create(
            sector=self.cfg.category,
            task_name="full_update_dimension_tables"
        )
        self.service_update_full.full_update_dimension_tables()
        Notification.finish(task_id=n.id)
        return self

    def update_dimension_tables(self):
        task = Notification.create(
            sector=self.cfg.category,
            task_name="update_dimension_tables"
        )
        self.service_update.update_dimension_tables()
        Notification.finish(task_id=task.id)
        return self

    def full_update_fact_table(self):
        task = Notification.create(
            sector=self.cfg.category,
            task_name="full_update_fact_table"
        )
        self.service_update_full.full_update_fact_table()
        Notification.finish(task_id=task.id)
        return self

    def update_fact_table(self):
        task = Notification.create(
            sector=self.cfg.category,
            task_name="update_fact_table"
        )
        self.service_update.update_fact_table()
        Notification.finish(task_id=task.id)
        return self

    def full_update(self):
        task = Notification.create(
            sector=self.cfg.category,
            task_name="full_update"
        )
        self.service_import.import_file()
        self.service_update_full.full_update_dimension_tables()
        self.service_update_full.full_update_fact_table()
        Notification.finish(task_id=task.id)
        return self

    def update(self):
        task = Notification.create(
            sector=self.cfg.category,
            task_name="update"
        )
        # self.service_import.import_file()
        self.service_update.update_dimension_tables()
        self.service_update.update_fact_table()
        Notification.finish(task_id=task.id)
        return self

    def delete_last_day(self):
        task = Notification.create(
            sector=self.cfg.category,
            task_name="delete_last_day"
        )
        self.service_update.delete_last_day()
        Notification.finish(task_id=task.id)
        return self

    def get_all_imported(self, page: int):
        engine = sqlalchemy.create_engine(covid19_application.db_uri)
        mypd = pd.read_sql_table('who_import_pandas', con=engine)
        return mypd

    def get_new_dates_as_array(self):
        new_dates_as_array = []
        old_dates = WhoDateReported.find_all_as_str()
        for news_date in WhoImportDao.get_datum_list():
            nd = news_date["Date_reported"]
            if nd not in old_dates:
                new_dates_as_array.append(nd)
        return new_dates_as_array
