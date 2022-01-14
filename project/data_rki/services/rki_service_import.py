import csv

import pandas
import sqlalchemy

from project.data.database import covid19_application
from project.data_all.services.all_config import BlueprintConfig
from project.data_all.services.all_service_mixins import AllServiceMixinImport

from project.data_all_notifications.notifications_model import Notification
from project.data_rki.model.rki_model_import import RkiImport
from project.data_rki.model.rki_model_import import RkiImportFactory
from project.data_rki.model.rki_model_import import RkiServiceImportFactory

db_uri = covid19_application.db_uri
app = covid19_application.app
db = covid19_application.db


class RkiServiceImport(AllServiceMixinImport):
    def __init__(self, database, config: BlueprintConfig):
        self.__database = database
        self.cfg = config
        app.logger.info(" ready: [RKI] Service Import ")

    def count_file_rows(self):
        count = 0
        for line in open(self.cfg.cvsfile_path):
            count += 1
        count -= 1
        return count

    def import_file(self):
        task = Notification.create(sector="RKI", task_name="import_file")
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
        app.logger.info("START: RkiImport.remove_all()")
        RkiImport.remove_all()
        app.logger.info("DONE: RkiImport.remove_all()")
        app.logger.info("------------------------------------------------------------")
        engine = sqlalchemy.create_engine(db_uri)
        data = pandas.read_csv(self.cfg.cvsfile_path)
        data.to_sql('rki_import_pandas', engine)
        app.logger.info("------------------------------------------------------------")
        with open(self.cfg.cvsfile_path, newline="\n") as csv_file:
            file_reader = csv.DictReader(
                csv_file,
                delimiter=",",
                quotechar='"'
            )
            k = 0
            for row in file_reader:
                k += 1
                my_datum = RkiServiceImportFactory.row_str_to_date_fields(row)
                o = RkiImportFactory.create_new(row=row, my_datum=my_datum)
                db.session.add(o)
                if (k % 500) == 0:
                    db.session.commit()
                if (k % 10000) == 0:
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
        Notification.finish(task_id=task.id)
        return self
