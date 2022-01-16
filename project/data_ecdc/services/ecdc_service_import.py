import csv

import pandas
import sqlalchemy

from project.data.database import covid19_application
from project.data_all.services.all_service import AllServiceBase
from project.data_all.services.all_service_config import AllServiceConfig
from project.data_all import AllDateReportedFactory
from project.data_all.services.all_service_mixins import AllServiceMixinImport

from project.data_all_notifications.notifications_model import Notification
from project.data_ecdc.model.ecdc_model_import import EcdcImport
from project.data_ecdc.factories.ecdc_model_import import EcdcImportFactory

app = covid19_application.app
db = covid19_application.db


class EcdcServiceImport(AllServiceBase, AllServiceMixinImport):

    def __init__(self, database, config: AllServiceConfig):
        super().__init__(database, config)
        app.logger.info(
            " ready [{}] {} ".format(
                self.cfg.category,
                self.__class__.__name__
            )
        )

    def count_file_rows(self):
        count = 0
        for line in open(self.cfg.cvsfile_path):
            count += 1
        count -= 1
        return count

    def import_file(self):
        task = Notification.create(
            sector=self.cfg.category,
            task_name="import_file"
        )
        self.log_line()
        app.logger.info(" [ECDC] import [begin]")
        self.log_line()
        app.logger.info(
            " [{}] imported into TABLE: {} <--- from FILE {} [START]".format(
                self.cfg.category,
                self.cfg.tablename,
                self.cfg.cvsfile_path
            )
        )
        k = 0
        self.log_line()
        app.logger.info(" EcdcImport.remove_all() START")
        EcdcImport.remove_all()
        app.logger.info(" EcdcImport.remove_all() DONE")
        self.log_line()
        app.logger.info(" ecdc_import_pandas START")
        engine = sqlalchemy.create_engine(covid19_application.db_uri)
        data = pandas.read_csv(self.cfg.cvsfile_path)
        data.to_sql(
            name='ecdc_import_pandas',
            if_exists='replace',
            con=engine
        )
        app.logger.info(" ecdc_import_pandas DONE")
        if not covid19_application.use_pandoc_only:
            self.log_line()
            with open(self.cfg.cvsfile_path, newline="") as csv_file:
                file_reader = csv.DictReader(csv_file, delimiter=",", quotechar='"')
                for row in file_reader:
                    date_rep = row["dateRep"]
                    d = AllDateReportedFactory.create_new_object_for_ecdc(
                        my_date_reported=date_rep
                    )
                    o = EcdcImportFactory.create_new(
                        date_reported=date_rep, d=d, row=row
                    )
                    db.session.add(o)
                    k = k + 1
                    if (k % 1000) == 0:
                        db.session.commit()
                    if (k % 10000) == 0:
                        app.logger.info(" [ECDC] import  ...  {} rows".format(str(k)))
                    if self.cfg.reached_limit_import_for_testing(row_number=k):
                        break
                db.session.commit()
                app.logger.info(" [ECDC] import  ...  {} rows total".format(str(k)))
            app.logger.info("")
        self.log_line()
        app.logger.info(
            " [{}] imported into TABLE: {} <--- from FILE {} [DONE]".format(
                self.cfg.category,
                self.cfg.tablename,
                self.cfg.cvsfile_path
            )
        )
        self.log_line()
        app.logger.info(" [ECDC] import [done]")
        self.log_line()
        Notification.finish(task_id=task.id)
        return self
