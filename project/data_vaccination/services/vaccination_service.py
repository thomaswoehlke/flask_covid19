from project.app_bootstrap.database import app
from project.data_all.all_config import BlueprintConfig
from project.data_all.all_service_download import AllDownloadService
from project.data_all.all_service_mixins import AllServiceMixin

from project.data_all.data_all_notifications.notifications_model import Task
from project.data_vaccination.services.vaccination_service_import import (
    VaccinationServiceImport,
)
from project.data_vaccination.services.vaccination_service_update import (
    VaccinationServiceUpdate,
)
from project.data_vaccination.services.vaccination_service_update_full import (
    VaccinationServiceUpdateFull,
)


class VaccinationService(AllServiceMixin):
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Vaccination Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = BlueprintConfig.create_config_for_rki_vaccination()
        self.service_download = AllDownloadService(database, self.cfg)
        self.service_import = VaccinationServiceImport(database, self.cfg)
        self.service_update = VaccinationServiceUpdate(database, self.cfg)
        self.service_update_full = VaccinationServiceUpdateFull(database, self.cfg)
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ready: [Vaccination] Service ")
        app.logger.debug("------------------------------------------------------------")

    def download(self):
        task = Task.create(sector="Vaccination", task_name="download")
        self.service_download.download()
        Task.finish(task_id=task.id)
        return self

    def count_file_rows(self):
        return self.service_import.count_file_rows()

    def import_file(self):
        task = Task.create(sector="Vaccination", task_name="import_file")
        self.service_import.import_file()
        Task.finish(task_id=task.id)
        return self

    def full_update_dimension_tables(self):
        task = Task.create(
            sector="Vaccination", task_name="full_update_dimension_tables"
        )
        self.service_update_full.full_update_dimension_tables()
        Task.finish(task_id=task.id)
        return self

    def update_dimension_tables(self):
        task = Task.create(sector="Vaccination", task_name="update_dimension_tables")
        self.service_update.update_dimension_tables()
        Task.finish(task_id=task.id)
        return self

    def full_update_fact_table(self):
        task = Task.create(sector="Vaccination", task_name="full_update_fact_table")
        self.service_update_full.full_update_fact_table()
        Task.finish(task_id=task.id)
        return self

    def update_fact_table(self):
        task = Task.create(sector="Vaccination", task_name="update_fact_table")
        self.service_update.update_fact_table()
        Task.finish(task_id=task.id)
        return self

    def full_update(self):
        task = Task.create(sector="Vaccination", task_name="full_update")
        self.service_import.import_file()
        self.service_update_full.full_update_dimension_tables()
        self.service_update_full.full_update_fact_table()
        Task.finish(task_id=task.id)
        return self

    def update(self):
        task = Task.create(sector="Vaccination", task_name="update")
        # self.service_import.import_file()
        self.service_update.update_dimension_tables()
        self.service_update.update_fact_table()
        Task.finish(task_id=task.id)
        return self

    def delete_last_day(self):
        task = Task.create(sector="Vaccination", task_name="delete_last_day")
        self.service_update.delete_last_day()
        Task.finish(task_id=task.id)
        return self
