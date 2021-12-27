import csv

from project.app_bootstrap.database import app
from project.app_bootstrap.database import db
from data_all.all_config import BlueprintConfig
from data_all.framework.services.all_service_import_mixins import AllServiceMixinImport
from data_all.model.all_task_model import Task
from project.data_rki.rki_model_flat import RkiFlat
from project.data_rki.rki_model_flat import RkiFlatFactory
from project.data_rki.rki_model_import import RkiImport
from project.data_rki.rki_model_import import RkiImportFactory
from project.data_rki.rki_model_import import RkiServiceImportFactory


class RkiServiceImport(AllServiceMixinImport):
    def __init__(self, database, config: BlueprintConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" [RKI] Service Import [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ready: [RKI] Service Import ")
        app.logger.debug("------------------------------------------------------------")

    def import_file(self):
        task = Task.create(sector="RKI", task_name="import_file").read()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] import_file  [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(
            " [RKI] import into TABLE: "
            + self.cfg.tablename
            + " <--- from FILE "
            + self.cfg.cvsfile_path
        )
        app.logger.info("------------------------------------------------------------")
        RkiImport.remove_all()
        RkiFlat.remove_all()
        with open(self.cfg.cvsfile_path, newline="\n") as csv_file:
            file_reader = csv.DictReader(csv_file, delimiter=",", quotechar='"')
            k = 0
            for row in file_reader:
                k += 1
                my_datum = RkiServiceImportFactory.row_str_to_date_fields(row)
                o = RkiImportFactory.create_new(row=row, my_datum=my_datum)
                db.session.add(o)
                #my_int_data = RkiServiceImportFactory.row_str_to_int_fields(row)
                #oo = RkiFlatFactory.create_new(
                #    row=row, my_int_data=my_int_data, my_datum=my_datum
                #)
                #db.session.add(oo)
                if (k % 200) == 0:
                    db.session.commit()
                    app.logger.info(" [RKI] import ... " + str(k) + " rows")
                if self.cfg.reached_limit_import_for_testing(row_number=k):
                    break
            db.session.commit()
            app.logger.info(" [RKI] import ... " + str(k) + " rows total")
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(
            " [RKI] imported into TABLE: "
            + self.cfg.tablename
            + " <--- from FILE "
            + self.cfg.cvsfile_path
        )
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] import_file  [done]")
        app.logger.info("------------------------------------------------------------")
        Task.finish(task_id=task.id)
        return self
