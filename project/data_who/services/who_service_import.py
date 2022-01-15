import csv
import sys

import pandas
import sqlalchemy

from project.data.database import covid19_application
from project.data_all.services.all_config import BlueprintConfig
from project.data_all.model.all_model_date_reported_factory import (
    AllDateReportedFactory,
)
from project.data_all.services.all_service_mixins import AllServiceMixinImport
from project.data_all_notifications.notifications_model import Notification
from project.data_who.model.who_model_import import WhoImport
from project.data_who.model.who_model_import import WhoImportFactory

app = covid19_application.app
db = covid19_application.db


class WhoServiceImport(AllServiceMixinImport):
    def __init__(self, database, config: BlueprintConfig):
        self.__database = database
        self.cfg = config
        app.logger.debug(" ready: [WHO] Service Import ")

    def count_file_rows(self):
        count = 0
        for line in open(self.cfg.cvsfile_path):
            count += 1
        count -= 1
        return count

    def import_file(self):
        task = Notification.create(sector="WHO", task_name="import_file")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [WHO] import [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(
            " [WHO] import into TABLE: "
            + self.cfg.tablename
            + " <--- from FILE "
            + self.cfg.cvsfile_path
        )
        if sys.platform == "linux":
            keyDate_reported = "\ufeffDate_reported"
        else:
            keyDate_reported = "ï»¿Date_reported"
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WhoImport.remove_all() START")
        WhoImport.remove_all()
        app.logger.info(" WhoImport.remove_all() DONE")
        app.logger.info("------------------------------------------------------------")
        if covid19_application.use_pandoc_only:
            engine = sqlalchemy.create_engine(covid19_application.db_uri_pandas)
            data = pandas.read_csv(self.cfg.cvsfile_path)
            data.to_sql('who_import_pandas', engine)
            app.logger.info(
                "------------------------------------------------------------")
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
                        app.logger.info(" [WHO] import  ... " + str(k) + " rows")
                    if self.cfg.reached_limit_import_for_testing(row_number=k):
                        break
                db.session.commit()
                app.logger.info(" [WHO] import  ... " + str(k) + " rows total")
            app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(
            " [WHO] imported into TABLE: "
            + self.cfg.tablename
            + " <--- from FILE "
            + self.cfg.cvsfile_path
        )
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [WHO] import [done]")
        app.logger.info("------------------------------------------------------------")
        Notification.finish(task_id=task.id)
        return self
