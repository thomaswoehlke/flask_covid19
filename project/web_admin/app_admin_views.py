from celery import states

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import login_required

from project.data.database import app, celery
from project.web.web.web_dispachter_service import admin_service
from project.web.web.web_model_transient import WebPageContent

drop_and_create_data_again = True

app_web_admin = Blueprint(
    "web_admin", __name__, template_folder="templates", url_prefix="/app/admin"
)


# -------------------------------------------------------------------------------------
#  Url Routes Frontend
# -------------------------------------------------------------------------------------


class AppAdminUrls:
    def __init__(self):
        app.logger.info(" ready: [WEB] AppAdminUrls ")

    @staticmethod
    @app_web_admin.route("/status")
    @login_required
    def url_admin_status():
        page_info = WebPageContent("Admin", "System Status")
        return render_template(
            "app_web_admin/admin_status.html", page_info=page_info)

    @staticmethod
    @app_web_admin.route("/info")
    @login_required
    def url_admin_info():
        page_info = WebPageContent("Admin", "Info")
        return render_template(
            "app_web_admin/admin_info.html", page_info=page_info)

    @staticmethod
    @app_web_admin.route("/database_table_row_count")
    @login_required
    def url_admin_database_table_row_count():
        page_info = WebPageContent("Admin", "DB Row Count")
        db_table_row_count = admin_service.database_table_row_count()
        return render_template(
            "app_web_admin/table_row_count/status.html",
            db_table_row_count=db_table_row_count,
            page_info=page_info
        )

    @staticmethod
    @app_web_admin.route("/database_import_status")
    @login_required
    def url_admin_database_import_status():
        page_info = WebPageContent("Admin", "DB Import Status")
        db_import_status = admin_service.database_import_status()
        return render_template(
            "app_web_admin/database_import_status.html",
            db_import_status=db_import_status,
            page_info=page_info
        )


app_admin_urls = AppAdminUrls()

# -------------------------------------------------------------------------------------
#  Celery TASKS
# -------------------------------------------------------------------------------------


class AppAdminTasks:
    def __init__(self):
        app.logger.info(" ready: [WEB] AppAdminTasks ")

    @staticmethod
    @celery.task(bind=True)
    def task_admin_alive_message(self):
        self.update_state(state=states.STARTED)
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" task_admin_alive_message [received] ")
        app.logger.info("------------------------------------------------------------")
        self.update_state(state=states.SUCCESS)
        result = "OK (task_admin_alive_message)"
        return result


app_admin_tasks = AppAdminTasks()

# -------------------------------------------------------------------------------------
#  URL Routes for Celery TASKS
# -------------------------------------------------------------------------------------


class AppAdminTaskUrls:
    def __init__(self):
        app.logger.info(" ready: [WEB] AppAdminTaskUrls ")

    @staticmethod
    @app_web_admin.route("/task/alive_message")
    @login_required
    def url_task_admin_alive_message():
        app.logger.info("url_task_admin_message_start [start]")
        app_admin_tasks.task_admin_alive_message.apply_async()
        flash("alive_message_task started")
        app.logger.info("url_task_admin_message_start [done]")
        return redirect(url_for("web_admin.url_admin_tasks"))

    @staticmethod
    @app_web_admin.route("/task/database/dump")
    @login_required
    def url_task_admin_database_dump():
        app.logger.info("url_task_admin_database_dump [start]")
        admin_service.database_dump()
        flash("admin_service.run_admin_database_dump started")
        app.logger.info("url_task_admin_database_dump [done]")
        return redirect(url_for("web_admin.url_admin_tasks"))

    @staticmethod
    @app_web_admin.route("/task/database/reimport")
    @login_required
    def url_task_admin_database_dump_reimport():
        app.logger.info("url_task_admin_database_dump_reimport [start]")
        admin_service.database_dump_reimport()
        flash("admin_service.run_admin_database_import started")
        app.logger.info("url_task_admin_database_dump_reimport [done]")
        return redirect(url_for("web_admin.url_admin_tasks"))

    @staticmethod
    @app_web_admin.route("/task/database/drop_create")
    @login_required
    def url_task_admin_database_dropcreate():
        app.logger.info("url_task_admin_database_dropcreate [start]")
        admin_service.database_drop_and_create()
        flash("admin_service.run_admin_database_drop started")
        app.logger.info("url_task_admin_database_dropcreate [done]")
        return redirect(url_for("web_admin.url_admin_tasks"))


app_admin_task_urls = AppAdminTaskUrls()
