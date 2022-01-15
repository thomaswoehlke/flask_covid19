import csv

import pandas
import sqlalchemy

from project.data.database import covid19_application
from project.data_all.services.all_service_config import AllServiceConfig
from project.data_all.model.all_model import AllDateReportedFactory
from project.data_all.services.all_service_mixins import AllServiceMixinImport

from project.data_all_notifications.notifications_model import Notification
from project.data_owid.model.owid_model_import import OwidImport
from project.data_owid.model.owid_model_import import OwidImportFactory

app = covid19_application.app
db = covid19_application.db


class OwidServiceImport(AllServiceMixinImport):
    def __init__(self, database, config: AllServiceConfig):
        self.__database = database
        self.cfg = config
        app.logger.info(" ready: [OWID] Service Import ")

    def count_file_rows(self):
        count = 0
        for line in open(self.cfg.cvsfile_path):
            count += 1
        count -= 1
        return count

    def import_file(self):
        task = Notification.create(sector="OWID", task_name="import_file")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] import [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(
            " [OWID] import into TABLE: {} {} <--- from FILE ".format(
                self.cfg.tablename, self.cfg.cvsfile_path
            )
        )
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" OwidImport.remove_all() START")
        OwidImport.remove_all()
        app.logger.info(" OwidImport.remove_all() DONE")
        app.logger.info("------------------------------------------------------------")
        if covid19_application.use_pandoc_only:
            app.logger.info(" owid_import_pandas START")
            engine = sqlalchemy.create_engine(covid19_application.db_uri_pandas)
            data = pandas.read_csv(self.cfg.cvsfile_path)
            data.to_sql(
                name='owid_import_pandas',
                if_exists='replace',
                con=engine
            )
            app.logger.info(" owid_import_pandas DONE")
        else:
            app.logger.info("------------------------------------------------------------")
            with open(self.cfg.cvsfile_path, newline="\n") as csv_file:
                file_reader = csv.DictReader(csv_file, delimiter=",", quotechar='"')
                k = 0
                for row in file_reader:
                    date_reported = row["date"]
                    d = AllDateReportedFactory.create_new_object_for_owid(
                        my_date_reported=date_reported
                    )
                    o = OwidImportFactory.create_new(
                        date_reported=date_reported, d=d, row=row
                    )
                    db.session.add(o)
                    k += 1
                    if (k % 2000) == 0:
                        db.session.commit()
                    if (k % 10000) == 0:
                        app.logger.info(" [OWID] import ... {} rows".format(str(k)))
                    if self.cfg.reached_limit_import_for_testing(row_number=k):
                        break
                db.session.commit()
                app.logger.info(" [OWID] import ... {} rows total".format(str(k)))
            app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(
            " [OWID] imported into TABLE: {} {} <--- from FILE ".format(
                self.cfg.tablename, self.cfg.cvsfile_path
            )
        )
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] import [done]")
        app.logger.info("------------------------------------------------------------")
        Notification.finish(task_id=task.id)
        return self
