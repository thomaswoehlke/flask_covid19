import csv
import sys

from project.app_bootstrap.database import covid19_application
from project.data_all.all_config import BlueprintConfig
from project.data_all.all_model_date_reported_factory import (
    BlueprintDateReportedFactory,
)
from project.data_all.all_service_mixins import AllServiceMixinImport
from project.data_all.notifications.notifications_model import Task
from project.data_who.model.who_model_import import WhoImport
from project.data_who.model.who_model_import import WhoImportFactory

app = covid19_application.app
db = covid19_application.db


class WhoServiceImport(AllServiceMixinImport):
    def __init__(self, database, config: BlueprintConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" [WHO] Service Import [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" ready: [WHO] Service Import ")
        app.logger.debug("------------------------------------------------------------")

    def count_file_rows(self):
        count = 0
        for line in open(self.cfg.cvsfile_path):
            count += 1
        count -= 1
        return count

    def import_file(self):
        task = Task.create(sector="WHO", task_name="import_file").read()
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
        with open(self.cfg.cvsfile_path, newline="\n") as csv_file:
            file_reader = csv.DictReader(csv_file, delimiter=",", quotechar='"')
            k = 0
            for row in file_reader:
                date_reported = row[keyDate_reported]
                d = BlueprintDateReportedFactory.create_new_object_for_who(
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
        Task.finish(task_id=task.id)
        return self
