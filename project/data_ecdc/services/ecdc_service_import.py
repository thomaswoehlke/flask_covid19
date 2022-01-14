import csv

import pandas
import sqlalchemy

from project.data.database import covid19_application
from project.data_all.services.all_config import BlueprintConfig
from project.data_all.model.all_model_date_reported_factory import (
    AllDateReportedFactory,
)
from project.data_all.services.all_service_mixins import AllServiceMixinImport

from project.data_all_notifications.notifications_model import Notification
from project.data_ecdc.model.ecdc_model_import import EcdcImport
from project.data_ecdc.model.ecdc_model_import import EcdcImportFactory

db_uri = covid19_application.db_uri
app = covid19_application.app
db = covid19_application.db


class EcdcServiceImport(AllServiceMixinImport):
    def __init__(self, database, config: BlueprintConfig):
        self.__database = database
        self.cfg = config
        app.logger.info(" ready: [ECDC] Service Import")

    def count_file_rows(self):
        count = 0
        for line in open(self.cfg.cvsfile_path):
            count += 1
        count -= 1
        return count

    def import_file(self):
        task = Notification.create(sector="ECDC", task_name="import_file")
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
        engine = sqlalchemy.create_engine(db_uri)
        data = pandas.read_csv(self.cfg.cvsfile_path)
        data.to_sql('ecdc_import_pandas', engine)
        app.logger.info("------------------------------------------------------------")
        with open(self.cfg.cvsfile_path, newline="") as csv_file:
            file_reader = csv.DictReader(csv_file, delimiter=",", quotechar='"')
            for row in file_reader:
                date_rep = row["dateRep"]
                d = AllDateReportedFactory.create_new_object_for_ecdc(
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
        Notification.finish(task_id=task.id)
        return self
