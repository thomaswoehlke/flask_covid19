import pandas as pd
import sqlalchemy

from datetime import date

from project.data.database import app, covid19_application
from project.data_all.services.all_service_config import AllServiceConfig
from project.data_all.services.all_service_download import AllDownloadService
from project.data_all.services.all_service_mixins import AllServiceMixin

from project.data_all_notifications.notifications_model import Notification
from project.data_rki.model.rki_model_data import RkiData
from project.data_rki.model.rki_model_date_reported import RkiMeldedatum
from project.data_rki.services.rki_service_import import RkiServiceImport
from project.data_rki.services.rki_service_update import RkiServiceUpdate
from project.data_rki.services.rki_service_update_full import RkiServiceUpdateFull


class RkiService(AllServiceMixin):
    def __init__(self, database):
        self.__database = database
        self.cfg = AllServiceConfig.create_config_for_rki()
        self.service_download = AllDownloadService(database, self.cfg)
        self.service_import = RkiServiceImport(database, self.cfg)
        self.service_update = RkiServiceUpdate(database, self.cfg)
        self.service_update_full = RkiServiceUpdateFull(database, self.cfg)
        app.logger.info(
            " ready [{}] {} ".format(
                self.cfg.category,
                self.__class__.__name__
            )
        )

    def download(self):
        task = Notification.create(sector=self.cfg.category, task_name="download")
        self.service_download.download()
        Notification.finish(task_id=task.id)
        return self

    def get_file_date(self):
        return "01.03.2022"

    def count_file_rows(self):
        return self.service_import.count_file_rows()

    def import_file(self):
        task = Notification.create(sector=self.cfg.category, task_name="import_file")
        self.service_import.import_file()
        Notification.finish(task_id=task.id)
        return self

    def full_update_dimension_tables(self):
        task = Notification.create(sector=self.cfg.category, task_name="full_update_dimension_tables")
        self.service_update_full.full_update_dimension_tables()
        Notification.finish(task_id=task.id)
        return self

    def update_dimension_tables(self):
        task = Notification.create(sector="RKI", task_name="update_dimension_tables")
        self.service_update.update_dimension_tables()
        Notification.finish(task_id=task.id)
        return self

    def full_update_fact_table(self):
        task = Notification.create(sector=self.cfg.category, task_name="full_update_fact_table")
        self.service_update_full.full_update_fact_table()
        Notification.finish(task_id=task.id)
        return self

    def update_fact_table(self):
        task = Notification.create(sector=self.cfg.category, task_name="update_fact_table")
        self.service_update.update_fact_table()
        Notification.finish(task_id=task.id)
        return self

    def full_update(self):
        task = Notification.create(sector=self.cfg.category, task_name="full_update")
        self.service_import.import_file()
        self.service_update_full.full_update_dimension_tables()
        self.service_update_full.full_update_fact_table()
        Notification.finish(task_id=task.id)
        return self

    def update(self):
        task = Notification.create(sector=self.cfg.category, task_name="update")
        # self.service_import.import_file()
        self.service_update.update_dimension_tables()
        self.service_update.update_fact_table()
        Notification.finish(task_id=task.id)
        return self

    def delete_last_day(self):
        task = Notification.create(sector=self.cfg.category, task_name="delete_last_day")
        self.service_update.delete_last_day()
        Notification.finish(task_id=task.id)
        return self

    def update_clean_brokenup(self):
        task = Notification.create(sector=self.cfg.category, task_name="update_clean_brokenup")
        result2 = Notification.get_rki_update_broken_date()
        result = Notification.get_rki_full_update_broken_date()
        resultlist = result.all()
        resultlist.extend(result2.all())
        if len(resultlist) > 0:
            t = task
            for t1 in resultlist:
                t2 = Notification.get_latest_by(sector=t1.sector, task_name=t1.task_name)
                if t2 is not None:
                    if t1.is_newer_than(t2):
                        # app.logger.info("newer:      "+str(t1))
                        t = t1
                        break
                    else:
                        app.logger.info("older than: "+str(t2))
                else:
                    t = t1
                    break
            app.logger.info("result: " + str(t))
            meldedatum = t.task_name.split(" ")[1]
            app.logger.info("meldedatum: " + meldedatum)
            d_meldedatum = date.fromisoformat(meldedatum)
            o_meldedatum = RkiMeldedatum.get_by_datum(d_meldedatum)
            app.logger.info("o_meldedatum: " + str(o_meldedatum))
            app.logger.info("RkiData.count(): " + str(RkiData.count()))
            RkiData.delete_by_date_reported(o_meldedatum)
            app.logger.info("RkiData.count(): " + str(RkiData.count()))
            Notification.finish(task_id=t.id)
            for ttt in Notification.get_rki_update_broken_date():
                Notification.finish(task_id=ttt.id)
        Notification.finish(task_id=task.id)
        return self

    def get_all_imported(self, page: int):
        engine = sqlalchemy.create_engine(covid19_application.db_uri)
        mypd = pd.read_sql_table('rki_import_pandas', con=engine).head(10)
        return mypd
