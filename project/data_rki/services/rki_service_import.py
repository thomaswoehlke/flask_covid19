import csv

import pandas
import sqlalchemy

from project.data.database import covid19_application
from project.data_all.services.all_service_base import AllServiceBase
from project.data_all.services.all_service_config import AllServiceConfig
from project.data_all.services.all_service_mixins import AllServiceMixinImport

from project.data_all_notifications.notifications_model import Notification
from project.data_rki.model.rki_model_import import RkiImport
from project.data_rki.model.rki_model_import import RkiImportFactory
from project.data_rki.model.rki_model_import import RkiServiceImportFactory

app = covid19_application.app
db = covid19_application.db


class RkiServiceImport(AllServiceBase, AllServiceMixinImport):

    def __init__(self, database, config: AllServiceConfig):
        self.__database = database
        self.cfg = config
        app.logger.info(" ready [{}] {} ".format(
            self.cfg, self.__class__.__name__
        ))

    def count_file_rows(self):
        count = 0
        for line in open(self.cfg.cvsfile_path):
            count += 1
        count -= 1
        return count

    def import_file(self):
        task = Notification.create(sector=self.cfg.category, task_name="import_file")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [{}] import_file  [begin]".format(self.cfg.category))
        app.logger.info("------------------------------------------------------------")
        app.logger.info(
            " [{}] import into TABLE: {} <--- from FILE {} [START]".format(
                self.cfg.category, self.cfg.tablename, self.cfg.cvsfile_path
            )
        )
        app.logger.info("------------------------------------------------------------")
        app.logger.info("START: RkiImport.remove_all()")
        RkiImport.remove_all()
        app.logger.info("DONE: RkiImport.remove_all()")
        app.logger.info("------------------------------------------------------------")
        if covid19_application.use_pandoc_only:
            app.logger.info(" rki_import_pandas START")
            engine = sqlalchemy.create_engine(covid19_application.db_uri)
            data = pandas.read_csv(self.cfg.cvsfile_path)
            data.to_sql(
                name='rki_import_pandas',
                if_exists='replace',
                con=engine,
                chunksize=5000,
                method='multi'
            )
            app.logger.info(" rki_import_pandas DONE")
            app.logger.info(
                "------------------------------------------------------------")
        else:
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
                        app.logger.info(
                            " [{}] import ... {} rows".format(
                                self.cfg.category, str(k)
                            )
                        )
                    if self.cfg.reached_limit_import_for_testing(row_number=k):
                        break
                db.session.commit()
                app.logger.info(
                    " [{}] import ... {} rows total".format(
                        self.cfg.category, str(k)
                    )
                )
            app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(
            " [{}] import into TABLE: {} <--- from FILE {} [DONE]".format(
                self.cfg.category, self.cfg.tablename, self.cfg.cvsfile_path
            )
        )
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [{}] import_file  [done]".format(self.cfg.category))
        app.logger.info("------------------------------------------------------------")
        Notification.finish(task_id=task.id)
        return self
