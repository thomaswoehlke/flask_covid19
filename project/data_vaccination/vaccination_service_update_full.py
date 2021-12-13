from project.app_bootstrap.database import app
from project.app_bootstrap.database import db
from project.data_all.all_task_model import Task
from project.data_all.all_model_date_reported_factory import (
    BlueprintDateReportedFactory,
)
from project.data_all.all_service_update_full_mixins import (
    AllServiceMixinUpdateFull,
)
from project.data_vaccination.vaccination_model_data import VaccinationData
from project.data_vaccination.vaccination_model_data import VaccinationDataFactory
from project.data_vaccination.vaccination_model_date_reported import (
    VaccinationDateReported,
)
from project.data_vaccination.vaccination_model_import import VaccinationImport
from project.data_vaccination.vaccination_service_update import (
    VaccinationServiceUpdateBase,
)


class VaccinationServiceUpdateFull(
    VaccinationServiceUpdateBase, AllServiceMixinUpdateFull
):
    def __full_update_date_reported(self):
        app.logger.info(" [Vaccination] full update date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        VaccinationDateReported.remove_all()
        date_reported_list = VaccinationImport.get_date_reported_as_array()
        i = 0
        for one_date_reported in date_reported_list:
            i += 1
            o = BlueprintDateReportedFactory.create_new_object_for_vaccination(
                my_date_reported=one_date_reported
            )
            db.session.add(o)
            output = (
                "  [Vaccination] full update date_reported [ " + str(i) + " ] " + str(o)
            )
            app.logger.info(output)
        db.session.commit()
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [Vaccination] full update date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __full_update_fact_table(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [Vaccination] full update [begin]")
        app.logger.info("------------------------------------------------------------")
        VaccinationData.remove_all()
        result_date_rep = VaccinationImport.get_date_rep()
        i = 0
        for (item_date_rep,) in result_date_rep:
            date_reported = VaccinationDateReported.get_by_datum(datum=item_date_rep)
            for item_import in VaccinationImport.find_by_datum(
                date_reported.date_reported_import_str
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
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [Vaccination] full update [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def full_update_dimension_tables(self):
        task = Task.create(sector="Vaccination", task_name="full_update_dimension_tables").read()
        VaccinationData.remove_all()
        self.__full_update_date_reported()
        Task.finish(task_id=task.id)
        return self

    def full_update_fact_table(self):
        task = Task.create(sector="Vaccination", task_name="full_update_fact_table").read()
        self.__full_update_fact_table()
        Task.finish(task_id=task.id)
        return self
