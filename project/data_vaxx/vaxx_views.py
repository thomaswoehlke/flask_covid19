from celery import states
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask_admin.contrib.sqla import ModelView
from project.data.database import admin
from project.data.database import app
from project.data.database import celery
from project.data.database import db
from project.data_vaxx.services.vaxx_service import VaccinationService
from project.web.model.web_model_transient import WebPageContent
from project.data_vaxx.model.vaxx_model_data import VaccinationData
from project.data_vaxx.model.vaxx_model_date_reported import (
    VaccinationDateReported,
)
from project.data_vaxx.model.vaxx_model_import import VaccinationImport

vaccination_service = VaccinationService(db)

app_vaccination = Blueprint(
    "vaxx", __name__,
    template_folder="templates",
    url_prefix="/vaxx"
)

admin.add_view(ModelView(VaccinationImport, db.session, category="Vaccination"))
admin.add_view(ModelView(VaccinationDateReported, db.session, category="Vaccination"))
admin.add_view(ModelView(VaccinationData, db.session, category="Vaccination"))


# ---------------------------------------------------------------------------------------------------------------
#  Url Routes Frontend
# ---------------------------------------------------------------------------------------------------------------


class VaccinationUrls:
    def __init__(self):
        app.logger.info(" ready: [Vaccination] VaccinationUrls ")

    @staticmethod
    @app_vaccination.route("")
    @app_vaccination.route("/")
    def url_vaccination_root():
        return redirect(url_for("vaxx.url_vaccination_info"))

    @staticmethod
    @app_vaccination.route("/info")
    def url_vaccination_info():
        page_info = WebPageContent("Vaccination", "Info")
        return render_template(
            "vaxx/vaccination_info.html",
            page_info=page_info
        )

    @staticmethod
    @app_vaccination.route("/imported/page/<int:page>")
    @app_vaccination.route("/imported")
    def url_vaccination_imported(page=1):
        page_info = WebPageContent("Vaccination", "Data: Germany Timeline imported")
        page_data = VaccinationImport.get_all(page)
        return render_template(
            "vaxx/imported/vaccination_imported.html",
            page_data=page_data,
            page_info=page_info,
        )

    @staticmethod
    @app_vaccination.route("/data/page/<int:page>")
    @app_vaccination.route("/data")
    def url_vaccination_data(page=1):
        page_info = WebPageContent("Vaccination", "Data: Germany Timeline")
        page_data = VaccinationData.get_all(page)
        return render_template(
            "vaxx/data/vaccination_data.html",
            page_data=page_data,
            page_info=page_info,
        )

    @staticmethod
    @app_vaccination.route("/delete_last_day")
    def url_vaccination_delete_last_day():
        app.logger.info("url_vaccination_delete_last_day [start]")
        flash("url_vaccination_delete_last_day [start]")
        vaccination_service.delete_last_day()
        flash("url_vaccination_delete_last_day [done]")
        app.logger.info("url_vaccination_delete_last_day [done]")
        return redirect(url_for("vaxx.url_vaccination_info"))


vaccination_urls = VaccinationUrls()

# ----------------------------------------------------------------------------------------------------------------
#  Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


class VaccinationTasks:
    def __init__(self):
        app.logger.info(" ready: [Vaccination] VaccinationTasks ")

    @staticmethod
    @celery.task(bind=True)
    def task_vaccination_import_file(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" Received: task_vaccination_import [OK] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
            vaccination_service.import_file()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_vaccination_import)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_vaccination_full_update_dimension_tables(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(
                " Received: task_vaccination_full_update_dimension_tables [OK] "
            )
            app.logger.info(
                "------------------------------------------------------------"
            )
            vaccination_service.full_update_dimension_tables()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_vaccination_full_update_dimension_tables)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_vaccination_update_dimension_tables(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" Received: task_vaccination_update_dimension_tables [OK] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
            vaccination_service.update_dimension_tables()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_vaccination_update_dimension_tables)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_vaccination_update_facttable(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" Received: task_vaccination_update_facttable [OK] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
            vaccination_service.update_fact_table()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_vaccination_update_facttable)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_vaccination_full_update_facttable(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" Received: task_vaccination_full_update_facttable [OK] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
            vaccination_service.full_update_fact_table()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_vaccination_full_update_facttable)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_vaccination_update(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" Received: task_vaccination_update [OK] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
            vaccination_service.full_update()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_vaccination_update)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_vaccination_full_update(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" Received: task_vaccination_full_update [OK] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
            vaccination_service.full_update()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_vaccination_full_update)"
        return result


vaccination_tasks = VaccinationTasks()

# ----------------------------------------------------------------------------------------------------------------
# URL Routes for Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


class VaccinationTaskUrls:
    def __init__(self):
        app.logger.info(" ready: [Vaccination] VaccinationTaskUrls ")

    @staticmethod
    @app_vaccination.route("/task/download")
    def url_task_vaccination_download():
        flash("vaccination_service.download started")
        vaccination_service.download()
        flash("vaccination_service.download done")
        return redirect(url_for("web_admin.url_admin_database_import_status"))

    @staticmethod
    @app_vaccination.route("/task/import")
    def url_task_vaccination_import():
        vaccination_tasks.task_vaccination_import_file.apply_async()
        flash("task_vaccination_import_file started")
        return redirect(url_for("web_admin.url_admin_database_import_status"))

    @staticmethod
    @app_vaccination.route("/task/update/full/dimension-tables")
    def url_task_vaccination_full_update_dimension_tables():
        flash("url_vaccination_task_update_dimensiontables_only started")
        vaccination_tasks.task_vaccination_full_update_dimension_tables.apply_async()
        return redirect(url_for("vaxx.url_vaccination_info"))

    @staticmethod
    @app_vaccination.route("/task/update/dimension-tables")
    def url_task_vaccination_update_dimension_tables():
        flash("url_vaccination_task_update_dimensiontables_only started")
        vaccination_tasks.task_vaccination_update_dimension_tables.apply_async()
        return redirect(url_for("vaxx.url_vaccination_info"))

    @staticmethod
    @app_vaccination.route("/task/update/fact-table/incremental/only")
    def url_task_vaccination_update_facttable():
        flash("url_vaccination_task_update_facttable_incremental_only started")
        vaccination_tasks.task_vaccination_update_facttable.apply_async()
        return redirect(url_for("vaxx.url_vaccination_info"))

    @staticmethod
    @app_vaccination.route("/task/update/fact-table/initial/only")
    def url_task_vaccination_full_update_facttable():
        flash("url_vaccination_task_update_facttable_initial_only started")
        vaccination_tasks.task_vaccination_full_update_facttable.apply_async()
        return redirect(url_for("vaxx.url_vaccination_info"))

    @staticmethod
    @app_vaccination.route("/task/full/update/")
    def url_task_vaccination_full_update():
        vaccination_service.download()
        flash("vaccination_service.download done")
        vaccination_tasks.task_vaccination_full_update.apply_async()
        flash("task_vaccination_full_update started")
        return redirect(url_for("vaxx.url_vaccination_info"))

    @staticmethod
    @app_vaccination.route("/task/update")
    def url_task_vaccination_update():
        vaccination_service.download()
        flash("vaccination_service.download done")
        vaccination_tasks.task_vaccination_update.apply_async()
        flash("task_vaccination_update started")
        return redirect(url_for("web_admin.url_admin_database_import_status"))


vaccination_task_urls = VaccinationTaskUrls()