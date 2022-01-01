import csv

from project.app_bootstrap.database import app
from project.app_bootstrap.database import db
from project.data_all.all_config import BlueprintConfig
from project.data_all.model.all_model_date_reported_factory import (
    BlueprintDateReportedFactory,
)
from project.data_all.framework.services.all_service_import_mixins import AllServiceMixinImport
from project.data_all.model.all_task_model import Task
from project.data_ecdc.model.ecdc_model_import import EcdcImport
from project.data_ecdc.model.ecdc_model_import import EcdcImportFactory


class EcdcServiceImport(AllServiceMixinImport):
    def __init__(self, database, config: BlueprintConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" ECDC Service Import [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ready: [ECDC] Service Import")
        app.logger.debug("------------------------------------------------------------")

    def import_file(self):
        task = Task.create(sector="ECDC", task_name="import_file").read()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [ECDC] import [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(
            " [ECDC] import into TABLE: "
            + self.cfg.tablename
            + " <--- from FILE "
            + self.cfg.cvsfile_path
        )
        k = 0
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" EcdcImport.remove_all() START")
        EcdcImport.remove_all()
        app.logger.info(" EcdcImport.remove_all() DONE")
        app.logger.info("------------------------------------------------------------")
        with open(self.cfg.cvsfile_path, newline="") as csv_file:
            file_reader = csv.DictReader(csv_file, delimiter=",", quotechar='"')
            for row in file_reader:
                date_rep = row["dateRep"]
                d = BlueprintDateReportedFactory.create_new_object_for_ecdc(
                    my_date_reported=date_rep
                )
                o = EcdcImportFactory.create_new(date_reported=date_rep, d=d, row=row)
                db.session.add(o)
                k = k + 1
                if (k % 1000) == 0:
                    db.session.commit()
                if (k % 10000) == 0:
                    app.logger.info(" [ECDC] import  ...  " + str(k) + " rows")
                if self.cfg.reached_limit_import_for_testing(row_number=k):
                    break
            db.session.commit()
            app.logger.info(" [ECDC] import  ...  " + str(k) + " rows total")
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(
            " [ECDC] imported into TABLE: "
            + self.cfg.tablename
            + " <--- from FILE "
            + self.cfg.cvsfile_path
        )
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [ECDC] import [done]")
        app.logger.info("------------------------------------------------------------")
        Task.finish(task_id=task.id)
        return self
