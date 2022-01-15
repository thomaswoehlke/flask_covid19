import csv

import pandas
import sqlalchemy

from project.data.database import covid19_application
from project.data_all.services.all_service import AllServiceBase
from project.data_all.services.all_service_config import AllServiceConfig
from project.data_all import AllDateReportedFactory
from project.data_all.services.all_service_mixins import AllServiceMixinImport
from project.data_all_notifications.notifications_model import Notification
from project.data_vaxx.model.vaxx_model_import import VaccinationImport
from project.data_vaxx.model.vaxx_model_import import (
    VaccinationImportFactory,
)

app = covid19_application.app
db = covid19_application.db


class VaccinationServiceImport(AllServiceBase, AllServiceMixinImport):

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
        app.logger.info(" [Vaccination] import [begin]")
        self.log_line()
        app.logger.info(
            " [Vaccination] import into TABLE: {} <--- from FILE {} [START]".format(
                self.cfg.tablename, self.cfg.cvsfile_path
            )
        )
        self.log_line()
        VaccinationImport.remove_all()
        self.log_line()
        app.logger.info(" vaccination_import_pandas START")
        engine = sqlalchemy.create_engine(covid19_application.db_uri)
        data = pandas.read_csv(
            self.cfg.cvsfile_path,
            delimiter="\t")
        data.to_sql(
            name='vaccination_import_pandas',
            if_exists='replace',
            con=engine
        )
        app.logger.info(" vaccination_import_pandas DONE")
        if not covid19_application.use_pandoc_only:
            self.log_line()
            k = 0
            with open(self.cfg.cvsfile_path, newline="\n") as csv_file:
                file_reader = csv.DictReader(csv_file, delimiter="\t", quotechar='"')
                for row in file_reader:
                    date_reported = row["date"]
                    d = AllDateReportedFactory.create_new_object_for_vaccination(
                        my_date_reported=date_reported
                    )
                    o = VaccinationImportFactory.create_new(
                        date_reported=date_reported, d=d, row=row
                    )
                    db.session.add(o)
                    k += 1
                    if (k % 100) == 0:
                        db.session.commit()
                        app.logger.info(" [Vaccination] import ... {} rows".format(
                            str(k))
                        )
                db.session.commit()
                app.logger.info(" [Vaccination] import ... {} rows total".format(
                    str(k))
                )
            app.logger.info("")
        self.log_line()
        app.logger.info(
            " [Vaccination] import into TABLE: {} <--- from FILE {} [DONE]".format(
                self.cfg.tablename, self.cfg.cvsfile_path
            )
        )
        self.log_line()
        app.logger.info(" [Vaccination] import [done]")
        self.log_line()
        Notification.finish(task_id=task.id)
        return self
