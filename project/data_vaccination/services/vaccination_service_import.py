import csv

import pandas
import sqlalchemy

from project.data.database import covid19_application
from project.data_all.services.all_config import BlueprintConfig
from project.data_all.model.all_model import AllDateReportedFactory
from project.data_all.services.all_service_mixins import AllServiceMixinImport
from project.data_all_notifications.notifications_model import Notification
from project.data_vaccination.model.vaccination_model_import import VaccinationImport
from project.data_vaccination.model.vaccination_model_import import (
    VaccinationImportFactory,
)

app = covid19_application.app
db = covid19_application.db


class VaccinationServiceImport(AllServiceMixinImport):
    def __init__(self, database, config: BlueprintConfig):
        self.__database = database
        self.cfg = config
        app.logger.info(" ready: [Vaccination] Service Import ")

    def __log_line(self):
        app.logger.info("------------------------------------------------------------")

    def count_file_rows(self):
        count = 0
        for line in open(self.cfg.cvsfile_path):
            count += 1
        count -= 1
        return count

    def import_file(self):
        task = Notification.create(sector="Vaccination", task_name="import_file").read()
        self.__log_line()
        app.logger.info(" [Vaccination] import [begin]")
        self.__log_line()
        app.logger.info(
            " [Vaccination] import into TABLE: "
            + self.cfg.tablename
            + " <--- from FILE "
            + self.cfg.cvsfile_path
        )
        self.__log_line()
        VaccinationImport.remove_all()
        self.__log_line()
        if covid19_application.use_pandoc_only:
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
        else:
            self.__log_line()
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
        self.__log_line()
        app.logger.info(
            " [Vaccination] imported into TABLE: {} {} <--- from FILE ".format(
                self.cfg.tablename, self.cfg.cvsfile_path
            )
        )
        self.__log_line()
        app.logger.info(" [Vaccination] import [done]")
        self.__log_line()
        Notification.finish(task_id=task.id)
        return self
