from flask import render_template, redirect, url_for, flash, Blueprint
from celery import states
from celery.utils.log import get_task_logger

from flask_covid19_conf.database import app, celery
from flask_covid19_app.blueprints.app_web.web_dispachter_matrix_service import app_admin_service
from flask_covid19_app.blueprints.app_web.web_model_transient import WebPageContent

drop_and_create_data_again = True

blueprint_app_admin = Blueprint('app_admin', __name__, template_folder='templates', url_prefix='/app/admin')


# ---------------------------------------------------------------------------------------------------------------
#  Url Routes Frontend
# ---------------------------------------------------------------------------------------------------------------


@blueprint_app_admin.route('/tasks')
def url_admin_tasks():
    page_info = WebPageContent('Admin', "Admin Tasks")
    return render_template(
        'app_admin/admin_tasks.html',
        page_info=page_info)


@blueprint_app_admin.route('/info')
def url_admin_info():
    page_info = WebPageContent('Admin', "Info")
    return render_template(
        'app_admin/admin_info.html',
        page_info=page_info)


# ----------------------------------------------------------------------------------------------------------------
#  Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


@celery.task(bind=True)
def task_admin_alive_message(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" task_admin_alive_message [received] ")
    logger.info("------------------------------------------------------------")
    self.update_state(state=states.SUCCESS)
    result = "OK (task_admin_alive_message)"
    return result


# ----------------------------------------------------------------------------------------------------------------
#  URL Routes for Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


@blueprint_app_admin.route('/task/alive_message')
def url_task_admin_alive_message():
    app.logger.info("url_task_admin_message_start [start]")
    task_admin_alive_message.apply_async()
    flash("alive_message_task started")
    app.logger.info("url_task_admin_message_start [done]")
    return redirect(url_for('app_admin.url_admin_tasks'))


@blueprint_app_admin.route('/task/database/dump')
def url_task_admin_database_dump():
    app.logger.info("url_task_admin_database_dump [start]")
    app_admin_service.database_dump()
    flash("admin_service.run_admin_database_dump started")
    app.logger.info("url_task_admin_database_dump [done]")
    return redirect(url_for('app_admin.url_admin_tasks'))


@blueprint_app_admin.route('/task/database/reimport')
def url_task_admin_database_dump_reimport():
    app.logger.info("url_task_admin_database_dump_reimport [start]")
    app_admin_service.database_dump_reimport()
    flash("admin_service.run_admin_database_import started")
    app.logger.info("url_task_admin_database_dump_reimport [done]")
    return redirect(url_for('app_admin.url_admin_tasks'))


@blueprint_app_admin.route('/task/database/drop_create')
def url_task_admin_database_dropcreate():
    app.logger.info("url_task_admin_database_dropcreate [start]")
    app_admin_service.database_drop_and_create()
    flash("admin_service.run_admin_database_drop started")
    app.logger.info("url_task_admin_database_dropcreate [done]")
    return redirect(url_for('app_admin.url_admin_tasks'))
