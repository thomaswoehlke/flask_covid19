from project.data.database import app
from project.data.database import db
from project.data_all import AllDateReportedFactory
from project.data_all.services.all_service import AllServiceBase
from project.data_all.services.all_service_config import AllServiceConfig

from project.data_all.services.all_service_mixins import (
    AllServiceMixinUpdateFull,
)
from project.data_all_notifications.notifications_model import Notification
from project.data_vaccination.model.vaccination_model_data import VaccinationData
from project.data_vaccination.model.vaccination_model_data import VaccinationDataFactory
from project.data_vaccination.model.vaccination_model_date_reported import (
    VaccinationDateReported,
)
from project.data_vaccination.model.vaccination_model_import import VaccinationImport


class VaccinationServiceUpdateFull(AllServiceBase, AllServiceMixinUpdateFull):

    def __init__(self, database, config: AllServiceConfig):
        super().__init__(database, config)
        app.logger.info(
            " ready [{}] {} ".format(
                self.cfg.category,
                self.__class__.__name__
            )
        )

    def __full_update_date_reported(self):
        app.logger.info(" [Vaccination] full update date_reported [begin]")
        super.__log_line()
        VaccinationDateReported.remove_all()
        date_reported_list = VaccinationImport.get_date_reported_as_array()
        i = 0
        for one_date_reported in date_reported_list:
            i += 1
            o = AllDateReportedFactory.create_new_object_for_vaccination(
                my_date_reported=one_date_reported
            )
            db.session.add(o)
            output = (
                " [Vaccination] full update date_reported [ " + str(i) + " ] " + str(o)
            )
            app.logger.info(output)
        db.session.commit()
        app.logger.info("")
        super.__log_line()
        app.logger.info(" [Vaccination] full update date_reported [done]")
        super.__log_line()
        return self

    def __full_update_fact_table(self):
        super.__log_line()
        app.logger.info(" [Vaccination] full update [begin]")
        super.__log_line()
        VaccinationData.remove_all()
        result_date_rep = VaccinationImport.get_date_rep()
        i = 0
        for item_date_rep in result_date_rep:
            date_reported = VaccinationDateReported.get_by_datum(datum=item_date_rep)
            for item_import in VaccinationImport.find_by_datum(
                date_reported.datum
            ):
                o = VaccinationDataFactory.create_new(date_reported, item_import)
                item_import.processed_full_update = True
                db.session.add(o)
                i += 1
                if i % 500 == 0:
                    app.logger.info(
                        " [Vaccination] full update ... " + str(i) + " rows"
                    )
                    db.session.commit()
        db.session.commit()
        app.logger.info(" [Vaccination] full update ... " + str(i) + " rows total")
        app.logger.info("")
        super.__log_line()
        app.logger.info(" [Vaccination] full update [done]")
        super.__log_line()
        return self

    def full_update_dimension_tables(self):
        task = Notification.create(
            sector="Vaccination", task_name="full_update_dimension_tables"
        ).read()
        VaccinationData.remove_all()
        self.__full_update_date_reported()
        Notification.finish(task_id=task.id)
        return self

    def full_update_fact_table(self):
        task = Notification.create(
            sector="Vaccination", task_name="full_update_fact_table"
        ).read()
        self.__full_update_fact_table()
        Notification.finish(task_id=task.id)
        return self
