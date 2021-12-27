import csv

from project.app_bootstrap.database import app
from project.app_bootstrap.database import db
from project.data_all.all_config import BlueprintConfig
from project.data_all.model.all_model_date_reported_factory import (
    BlueprintDateReportedFactory,
)
from project.data_all.framework.services.all_service_import_mixins import AllServiceMixinImport
from project.data_all.model.all_task_model import Task
from project.data_owid.owid_model_flat import OwidFlat
from project.data_owid.owid_model_flat import OwidFlatFactory
from project.data_owid.owid_model_import import OwidImport
from project.data_owid.owid_model_import import OwidImportFactory


class OwidServiceImport(AllServiceMixinImport):
    def __init__(self, database, config: BlueprintConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" OWID Service Import [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ready: [OWID] Service Import ")
        app.logger.debug("------------------------------------------------------------")

    def import_file(self):
        task = Task.create(sector="OWID", task_name="import_file").read()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] import [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(
            " [OWID] import into TABLE: "
            + self.cfg.tablename
            + " <--- from FILE "
            + self.cfg.cvsfile_path
        )

        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WhoImport.remove_all() START")
        OwidImport.remove_all()
        app.logger.info(" WhoImport.remove_all() DONE")
        app.logger.info(" WhoFlat.remove_all()   START")
        OwidFlat.remove_all()
        app.logger.info(" WhoFlat.remove_all()   DONE")
        app.logger.info("------------------------------------------------------------")
        with open(self.cfg.cvsfile_path, newline="\n") as csv_file:
            file_reader = csv.DictReader(csv_file, delimiter=",", quotechar='"')
            k = 0
            for row in file_reader:
                date_reported = row["date"]
                d = BlueprintDateReportedFactory.create_new_object_for_owid(
                    my_date_reported=date_reported
                )
                o = OwidImportFactory.create_new(
                    date_reported=date_reported, d=d, row=row
                )
                db.session.add(o)
                # f = OwidFlatFactory.create_new(d=d, row=row)
                # db.session.add(f)
                k += 1
                if (k % 2000) == 0:
                    db.session.commit()
                if (k % 10000) == 0:
                    app.logger.info(" [OWID] import ... " + str(k) + " rows")
                if self.cfg.reached_limit_import_for_testing(row_number=k):
                    break
            db.session.commit()
            app.logger.info(" [OWID] import ... " + str(k) + " rows total")
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(
            " [OWID] imported into TABLE: "
            + self.cfg.tablename
            + " <--- from FILE "
            + self.cfg.cvsfile_path
        )
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] import [done]")
        app.logger.info("------------------------------------------------------------")
        Task.finish(task_id=task.id)
        return self
