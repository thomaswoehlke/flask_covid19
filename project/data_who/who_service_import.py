import csv
import sys

from project.app_bootstrap.database import covid19_application
from data_all.all_config import BlueprintConfig
from data_all.model.all_model_date_reported_factory import (
    BlueprintDateReportedFactory,
)
from data_all.framework.services.all_service_import_mixins import AllServiceMixinImport
from data_all.model.all_task_model import Task
from project.data_who.who_model_flat import WhoFlat
from project.data_who.who_model_flat import WhoFlatFactory
from project.data_who.who_model_import import WhoImport
from project.data_who.who_model_import import WhoImportFactory

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
        app.logger.info("------------------------------------------------------------")
        if sys.platform == "linux":
            keyDate_reported = "\ufeffDate_reported"
        else:
            keyDate_reported = "ï»¿Date_reported"
        WhoImport.remove_all()
        WhoFlat.remove_all()
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
                my_data = {
                    "new_cases": int(row["New_cases"]),
                    "cumulative_cases": int(row["Cumulative_cases"]),
                    "new_deaths": int(row["New_deaths"]),
                    "cumulative_deaths": int(row["Cumulative_deaths"]),
                }
                oo = WhoFlatFactory.create_new(
                    date_reported=date_reported, d=d, row=row, my_data=my_data
                )
                db.session.add(oo)
                k += 1
                if (k % 2000) == 0:
                    db.session.commit()
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
