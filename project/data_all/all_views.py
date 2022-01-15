from celery import states

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import login_required

from project.data.database import app, celery
from project.web.services.web_dispachter_service import (
    all_service_dispachter_matrix,
)
from project.web.model.web_model_transient import WebPageContent

drop_and_create_data_again = True

app_all = Blueprint(
    "data_all", __name__, template_folder="templates", url_prefix="/app/all"
)

# -----------------------------------------------------------------------------------
#  Url Routes Frontend
# -----------------------------------------------------------------------------------


class AllUrls:
    def __init__(self):
        app.logger.info(" ready: [ALL] AllUrls ")

    @staticmethod
    @app_all.route("/info")
    @login_required
    def url_all_info():
        page_info = WebPageContent("All", "Info")
        return render_template("data_all/data_all_info.html", page_info=page_info)

    @staticmethod
    @app_all.route("/delete_last_day")
    @login_required
    def url_all_delete_last_day():
        app.logger.info("url_all_delete_last_day [start]")
        flash("url_all_delete_last_day [start]")
        all_service_dispachter_matrix.delete_last_day()
        flash("url_all_delete_last_day [done]")
        app.logger.info("url_all_delete_last_day [done]")
        return redirect(url_for("data_all.url_all_info"))


all_urls = AllUrls()


# ------------------------------------------------------------------------------------
#  Celery TASKS
# ------------------------------------------------------------------------------------


class AllTasks:
    def __init__(self):
        app.logger.info(" ready: [ALL] AllTasks ")

    @staticmethod
    @celery.task(bind=True)
    def task_all_alive_message(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" task_all_alive_message [received] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
        self.update_state(state=states.SUCCESS)
        result = "OK (task_all_alive_message)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_all_import_file(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" task_all_import_file [start] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
            all_service_dispachter_matrix.import_file()
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" task_all_import_file [done] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
        self.update_state(state=states.SUCCESS)
        result = "OK (task_all_import_all_files)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_all_update_full_dimension_tables(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" task_all_update_full_dimension_tables [start] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
            all_service_dispachter_matrix.full_update_dimension_tables()
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" task_all_update_full_dimension_tables [done] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
        self.update_state(state=states.SUCCESS)
        result = "OK (task_all_update_full_dimension_tables)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_all_update_dimension_tables(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" task_all_update_dimension_tables [start] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
            all_service_dispachter_matrix.update_dimension_tables()
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" task_all_update_dimension_tables [done] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
        self.update_state(state=states.SUCCESS)
        result = "OK (task_all_update_dimension_tables)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_all_full_update_fact_table(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" task_all_update_fact_table_initial_only [start] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
            all_service_dispachter_matrix.full_update_fact_table()
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" task_all_update_fact_table_initial_only [done] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
        self.update_state(state=states.SUCCESS)
        result = "OK (task_all_update_fact_table_initial_only)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_all_update_fact_table(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" task_all_update_fact_table [start] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
            all_service_dispachter_matrix.update_fact_table()
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" task_all_update_fact_table [done] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
        self.update_state(state=states.SUCCESS)
        result = "OK (task_all_update_fact_table)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_all_full_update(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" task_all_full_update [start] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
            all_service_dispachter_matrix.full_update()
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" task_all_full_update [done] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
        self.update_state(state=states.SUCCESS)
        result = "OK (task_all_full_update)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_all_update(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" task_all_update [start] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
            all_service_dispachter_matrix.update()
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" task_all_update [done] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
        self.update_state(state=states.SUCCESS)
        result = "OK (task_all_update)"
        return result


all_tasks = AllTasks()

# -----------------------------------------------------------------------------------
#  URL Routes for Celery TASKS
# -----------------------------------------------------------------------------------


class AllTaskUrls:
    def __init__(self):
        app.logger.info(" ready: [ALL] AllTaskUrls ")

    @staticmethod
    @app_all.route("/task/download")
    @login_required
    def url_task_all_download():
        app.logger.info("url_task_all_download_all_files [start]")
        all_service_dispachter_matrix.download()
        app.logger.info("url_task_all_download_all_files [done]")
        return redirect(url_for("data_all.url_all_info"))

    @staticmethod
    @app_all.route("/task/import")
    @login_required
    def url_task_all_import():
        app.logger.info("url_task_all_import_all_files [start]")
        all_tasks.task_all_import_file.apply_async()
        flash(message="async url_task_all_import_all_files [start]", category="warning")
        app.logger.warn("async url_task_all_import_all_files [start]")
        app.logger.info("url_task_all_import_all_files [done]")
        return redirect(url_for("data_all.url_all_info"))

    @staticmethod
    @app_all.route("/task/full/update/dimension_tables")
    @login_required
    def url_task_all_full_update_dimension_tables():
        app.logger.info("url_task_all_update_full_dimension_tables [start]")
        all_tasks.task_all_update_full_dimension_tables.apply_async()
        flash(
            message="async task_all_update_full_dimension_tables [start]",
            category="warning",
        )
        app.logger.warn("async task_all_update_full_dimension_tables [start]")
        app.logger.info("url_task_all_update_full_dimension_tables [done]")
        return redirect(url_for("data_all.url_all_info"))

    @staticmethod
    @app_all.route("/task/update/dimension_tables")
    @login_required
    def url_task_all_update_dimension_tables():
        app.logger.info("url_task_all_update_dimension_tables [start]")
        all_tasks.task_all_update_dimension_tables.apply_async()
        flash(
            message="async task_all_update_dimension_tables [start]", category="warning"
        )
        app.logger.warn("async task_all_update_dimension_tables [start]")
        app.logger.info("url_task_all_update_dimension_tables [done]")
        return redirect(url_for("data_all.url_all_info"))

    @staticmethod
    @app_all.route("/task/full/update/fact_table")
    @login_required
    def url_task_all_full_update_fact_table():
        app.logger.info("url_task_all_full_update_fact_table [start]")
        all_tasks.task_all_full_update_fact_table.apply_async()
        flash(
            message="async task_all_full_update_fact_table [start]", category="warning"
        )
        app.logger.warn("async task_all_full_update_fact_table [start]")
        app.logger.info("url_task_all_full_update_fact_table [done]")
        return redirect(url_for("data_all.url_all_info"))

    @staticmethod
    @app_all.route("/task/update/fact_table")
    @login_required
    def url_task_all_update_fact_table():
        app.logger.info("url_task_all_update_fact_table [start]")
        all_tasks.task_all_update_fact_table.apply_async()
        flash(message="async task_all_update_fact_table [start]", category="warning")
        app.logger.warn("async task_all_update_fact_table [start]")
        app.logger.info("url_task_all_update_fact_table [done]")
        return redirect(url_for("data_all.url_all_info"))

    @staticmethod
    @app_all.route("/task/full/update")
    @login_required
    def url_task_all_full_update():
        app.logger.info("url_task_all_full_update [start]")
        all_service_dispachter_matrix.download()
        all_tasks.task_all_full_update.apply_async()
        flash(message="async task_all_full_update [start]", category="warning")
        app.logger.warn("async task_all_full_update [start]")
        app.logger.info("url_task_all_full_update [done]")
        return redirect(url_for("data_all.url_all_info"))

    @staticmethod
    @app_all.route("/task/update")
    @login_required
    def url_task_all_update(next=None):
        app.logger.info("url_task_all_update [start]")
        all_service_dispachter_matrix.download()
        all_tasks.task_all_update.apply_async()
        flash(message="async task_all_update [start]", category="warning")
        app.logger.warn("async task_all_update [start]")
        app.logger.info("url_task_all_update [done]")
        return redirect(url_for("data_all.url_all_info"))


all_task_urls = AllTaskUrls()
