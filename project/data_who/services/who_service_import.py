import csv
import sys

import pandas
import sqlalchemy

from project.data.database import covid19_application
from project.data_all.services.all_service import AllServiceBase
from project.data_all.services.all_service_config import AllServiceConfig
from project.data_all.services.all_service_mixins import AllServiceMixinImport
from project.data_all_notifications.notifications_model import Notification
from project.data_who.model.who_model_import_dao import WhoImportDao

app = covid19_application.app
db = covid19_application.db


class WhoServiceImport(AllServiceBase, AllServiceMixinImport):

    def __init__(self, database, config: AllServiceConfig):
        super().__init__(database, config)
        app.logger.info(
            " ready [{}] {} ".format(
                self.cfg.category,
                self.__class__.__name__
            )
        )

    def count_file_rows(self):
        count = 0
        for line in open(self.cfg.cvsfile_path):
            count += 1
        count -= 1
        return count

    def import_file(self):
        task = Notification.create(
            self.cfg.category,
            task_name="import_file"
        )
        self.log_line()
        app.logger.info(" [WHO] import [begin]")
        self.log_line()
        app.logger.info(
            " [WHO] import into TABLE: {} {} <--- from FILE [begin]".format(
                self.cfg.tablename, self.cfg.cvsfile_path
            )
        )
        #if sys.platform == "linux":
        #    keyDate_reported = "\ufeffDate_reported"
        #else:
        #    keyDate_reported = "ï»¿Date_reported"
        self.log_line()
        app.logger.info(" WhoImport.remove_all() START")
        WhoImportDao.remove_all()
        app.logger.info(" WhoImport.remove_all() DONE")
        self.log_line()
        app.logger.info(" who_import_pandas START")
        engine = sqlalchemy.create_engine(covid19_application.db_uri)
        data = pandas.read_csv(
            self.cfg.cvsfile_path,
            parse_dates=False,
            infer_datetime_format=False
        )
        data.to_sql(
            name='who_import_pandas',
            if_exists='replace',
            con=engine
        )
        app.logger.info(" who_import_pandas DONE")
        self.log_line()
        app.logger.info(
            " [WHO] import into TABLE: {} {} <--- from FILE [DONE]".format(
                self.cfg.tablename, self.cfg.cvsfile_path
            )
        )
        self.log_line()
        app.logger.info(" [WHO] import [done]")
        self.log_line()
        Notification.finish(task_id=task.id)
        return self
