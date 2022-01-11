from project.app_bootstrap.database import app
from project.data_all.all_service_mixins import AllServiceMixin
from project.data_all_notifications.notifications_model import Notification
from project.data_ecdc.services.ecdc_service import EcdcService
from project.data_owid.services.owid_service import OwidService
from project.data_rki.services.rki_service import RkiService
from project.data_vaccination.services.vaccination_service import VaccinationService
from project.data_who.services.who_service import WhoService


class AllDataServiceDispachterMatrix(AllServiceMixin):
    def __init__(
        self,
        who_service: WhoService,
        owid_service: OwidService,
        rki_service: RkiService,
        vaccination_service: VaccinationService,
        ecdc_service: EcdcService,
    ):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" [ALL] Dispachter Matrix Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__services_for = {
            "download": [
                who_service,
                vaccination_service,
                ecdc_service,
                owid_service,
                # rki_service,
            ],
            "import_file": [
                who_service,
                vaccination_service,
                ecdc_service,
                owid_service,
                # rki_service,
            ],
            "full_update_dimension_tables": [
                who_service,
                vaccination_service,
                ecdc_service,
                owid_service,
                # rki_service,
            ],
            "update_dimension_tables": [
                who_service,
                owid_service,
                # rki_service
            ],
            "full_update_fact_table": [
                who_service,
                vaccination_service,
                ecdc_service,
                owid_service,
                # rki_service,
            ],
            "update_fact_table": [
                who_service,
                owid_service,
                # rki_service
            ],
            "full_update": [
                who_service,
                vaccination_service,
                ecdc_service,
                owid_service,
                # rki_service,
            ],
            "update": [
                who_service,
                owid_service,
                # rki_service
            ],
            "update_but_full_update": [
                vaccination_service,
                ecdc_service
            ],
            "delete_last_day": [
                who_service,
                owid_service,
                # rki_service
            ],
        }
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ready: [ALL] Dispachter Matrix Service")
        app.logger.debug("------------------------------------------------------------")

    def download(self):
        task = Notification.create(sector="ALL", task_name="download")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" [ALL] download [start]")
        app.logger.info(" ")
        for service in self.__services_for["download"]:
            service.download()
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" [ALL] download [done] ")
        app.logger.debug("------------------------------------------------------------")
        Notification.finish(task_id=task.id)
        return self

    def import_file(self):
        task = Notification.create(sector="ALL", task_name="import_file")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" [ALL] import_file [start]")
        app.logger.debug("------------------------------------------------------------")
        for service in self.__services_for["import_file"]:
            service.import_file()
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" [ALL] import_file [done] ")
        app.logger.debug("------------------------------------------------------------")
        Notification.finish(task_id=task.id)
        return self

    def full_update_dimension_tables(self):
        task = Notification.create(sector="ALL", task_name="full_update_dimension_tables")
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" [ALL] full_update_dimension_tables [start] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        for service in self.__services_for["full_update_dimension_tables"]:
            service.full_update_dimension_tables()
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" [ALL] full_update_dimension_tables [done] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        Notification.finish(task_id=task.id)
        return self

    def update_dimension_tables(self):
        task = Notification.create(sector="ALL", task_name="update_dimension_tables")
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" [ALL] update_dimension_tables [start] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        for service in self.__services_for["update_dimension_tables"]:
            service.update_dimension_tables()
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" [ALL] update_dimension_tables [done] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        Notification.finish(task_id=task.id)
        return self

    def full_update_fact_table(self):
        task = Notification.create(sector="ALL", task_name="full_update_fact_table")
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" [ALL] full_update_fact_table [start] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        for service in self.__services_for["full_update_fact_table"]:
            service.full_update_fact_table()
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" [ALL] full_update_fact_table [done] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        Notification.finish(task_id=task.id)
        return self

    def update_fact_table(self):
        task = Notification.create(sector="ALL", task_name="update_fact_table")
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" [ALL] update_fact_table [start] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        for service in self.__services_for["update_fact_table"]:
            service.update_fact_table()
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" [ALL] update_fact_table [done] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        Notification.finish(task_id=task.id)
        return self

    def full_update(self):
        task = Notification.create(sector="ALL", task_name="full_update")
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" [ALL] full_update [start] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        for service in self.__services_for["full_update"]:
            service.full_update()
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" [ALL] full_update [done] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        Notification.finish(task_id=task.id)
        return self

    def update(self):
        task = Notification.create(sector="ALL", task_name="update")
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" [ALL] update [start] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        for service in self.__services_for["update"]:
            service.update()
        for service in self.__services_for["update_but_full_update"]:
            service.full_update()
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" [ALL] update [done] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        Notification.finish(task_id=task.id)
        return self

    def delete_last_day(self):
        task = Notification.create(sector="ALL", task_name="delete_last_day")
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" [ALL] delete_last_day [start] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        for service in self.__services_for["delete_last_day"]:
            service.delete_last_day()
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" [ALL] delete_last_day [done] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        Notification.finish(task_id=task.id)
        return self
