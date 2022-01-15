import csv
import sys

import pandas
import sqlalchemy

from project.data.database import covid19_application
from project.data_all.services.all_service_config import AllServiceConfig
from project.data_all.model.all_model import AllDateReportedFactory
from project.data_all.services.all_service_mixins import AllServiceMixinImport
from project.data_all_notifications.notifications_model import Notification
from project.data_who.model.who_model_import import WhoImport
from project.data_who.model.who_model_import import WhoImportFactory

app = covid19_application.app
db = covid19_application.db


class WhoServiceImport(AllServiceMixinImport):
    def __init__(self, database, config: AllServiceConfig):
        self.__database = database
        self.cfg = config
        app.logger.debug(" ready: [WHO] WhoServiceImport ")

    def __log_line(self):
        app.logger.info("------------------------------------------------------------")

    def count_file_rows(self):
        count = 0
        for line in open(self.cfg.cvsfile_path):
            count += 1
        count -= 1
        return count

    def import_file(self):
        task = Notification.create(sector="WHO", task_name="import_file")
        self.__log_line()
        app.logger.info(" [WHO] import [begin]")
        self.__log_line()
        app.logger.info(
            " [WHO] import into TABLE: {} {} <--- from FILE [begin]".format(
                self.cfg.tablename, self.cfg.cvsfile_path
            )
        )
        if sys.platform == "linux":
            keyDate_reported = "\ufeffDate_reported"
        else:
            keyDate_reported = "ï»¿Date_reported"
        self.__log_line()
        app.logger.info(" WhoImport.remove_all() START")
        WhoImport.remove_all()
        app.logger.info(" WhoImport.remove_all() DONE")
        self.__log_line()
        if covid19_application.use_pandoc_only:
            app.logger.info(" who_import_pandas START")
            engine = sqlalchemy.create_engine(covid19_application.db_uri)
            data = pandas.read_csv(self.cfg.cvsfile_path)
            data.to_sql(
                name='who_import_pandas',
                if_exists='replace',
                con=engine)
            app.logger.info(" who_import_pandas DONE")
            self.__log_line()
        else:
            with open(self.cfg.cvsfile_path, newline="\n") as csv_file:
                file_reader = csv.DictReader(csv_file, delimiter=",", quotechar='"')
                k = 0
                for row in file_reader:
                    date_reported = row[keyDate_reported]
                    d = AllDateReportedFactory.create_new_object_for_who(
                        my_date_reported=date_reported
                    )
                    o = WhoImportFactory.create_new(
                        date_reported=date_reported, d=d, row=row
                    )
                    db.session.add(o)
                    k += 1
                    if (k % 2000) == 0:
                        db.session.commit()
                    if (k % 10000) == 0:
                        app.logger.info(" [WHO] import ... {} rows".format(
                            str(k))
                        )
                    if self.cfg.reached_limit_import_for_testing(row_number=k):
                        break
                db.session.commit()
                app.logger.info(" [WHO] import ... {} rows total".format(
                    str(k))
                )
            app.logger.info("")
        self.__log_line()
        app.logger.info(
            " [WHO] import into TABLE: {} {} <--- from FILE [DONE]".format(
                self.cfg.tablename, self.cfg.cvsfile_path
            )
        )
        self.__log_line()
        app.logger.info(" [WHO] import [done]")
        self.__log_line()
        Notification.finish(task_id=task.id)
        return self
