from flask import render_template, redirect, url_for, flash, Blueprint
from celery import states
from celery.utils.log import get_task_logger

from flask_covid19_conf.database import app, celery
from flask_covid19_app_web.web_dispachter_matrix_service import all_dispachter_matrix_service
from flask_covid19_app_web.web_model_transient import WebPageContent

drop_and_create_data_again = True

blueprint_app_all = Blueprint('app_all', __name__, template_folder='templates', url_prefix='/app/all')


# ---------------------------------------------------------------------------------------------------------------
#  Url Routes Frontend
# ---------------------------------------------------------------------------------------------------------------


@blueprint_app_all.route('/info')
def url_all_info():
    page_info = WebPageContent('All', "Info")
    return render_template(
        'app_all/app_all_info.html',
        page_info=page_info)


@blueprint_app_all.route('/delete_last_day')
def url_all_delete_last_day():
    app.logger.info("url_all_delete_last_day [start]")
    flash("url_all_delete_last_day [start]")
    all_dispachter_matrix_service.delete_last_day()
    flash("url_all_delete_last_day [done]")
    app.logger.info("url_all_delete_last_day [done]")
    return redirect(url_for('app_all.url_all_info'))

# ----------------------------------------------------------------------------------------------------------------
#  Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


@celery.task(bind=True)
def task_all_alive_message(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" task_all_alive_message [received] ")
    logger.info("------------------------------------------------------------")
    self.update_state(state=states.SUCCESS)
    result = "OK (task_all_alive_message)"
    return result


@celery.task(bind=True)
def task_all_import_file(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" task_all_import_file [start] ")
    logger.info("------------------------------------------------------------")
    all_dispachter_matrix_service.import_file()
    logger.info("------------------------------------------------------------")
    logger.info(" task_all_import_file [done] ")
    logger.info("------------------------------------------------------------")
    self.update_state(state=states.SUCCESS)
    result = "OK (task_all_import_all_files)"
    return result


@celery.task(bind=True)
def task_all_update_full_dimension_tables(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" task_all_update_full_dimension_tables [start] ")
    logger.info("------------------------------------------------------------")
    all_dispachter_matrix_service.full_update_dimension_tables()
    logger.info("------------------------------------------------------------")
    logger.info(" task_all_update_full_dimension_tables [done] ")
    logger.info("------------------------------------------------------------")
    self.update_state(state=states.SUCCESS)
    result = "OK (task_all_update_full_dimension_tables)"
    return result


@celery.task(bind=True)
def task_all_update_dimension_tables(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" task_all_update_dimension_tables [start] ")
    logger.info("------------------------------------------------------------")
    all_dispachter_matrix_service.update_dimension_tables()
    logger.info("------------------------------------------------------------")
    logger.info(" task_all_update_dimension_tables [done] ")
    logger.info("------------------------------------------------------------")
    self.update_state(state=states.SUCCESS)
    result = "OK (task_all_update_dimension_tables)"
    return result


@celery.task(bind=True)
def task_all_full_update_fact_table(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" task_all_update_fact_table_initial_only [start] ")
    logger.info("------------------------------------------------------------")
    all_dispachter_matrix_service.full_update_fact_table()
    logger.info("------------------------------------------------------------")
    logger.info(" task_all_update_fact_table_initial_only [done] ")
    logger.info("------------------------------------------------------------")
    self.update_state(state=states.SUCCESS)
    result = "OK (task_all_update_fact_table_initial_only)"
    return result


@celery.task(bind=True)
def task_all_update_fact_table(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" task_all_update_fact_table [start] ")
    logger.info("------------------------------------------------------------")
    all_dispachter_matrix_service.update_fact_table()
    logger.info("------------------------------------------------------------")
    logger.info(" task_all_update_fact_table [done] ")
    logger.info("------------------------------------------------------------")
    self.update_state(state=states.SUCCESS)
    result = "OK (task_all_update_fact_table)"
    return result


@celery.task(bind=True)
def task_all_full_update(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" task_all_full_update [start] ")
    logger.info("------------------------------------------------------------")
    all_dispachter_matrix_service.full_update()
    logger.info("------------------------------------------------------------")
    logger.info(" task_all_full_update [done] ")
    logger.info("------------------------------------------------------------")
    self.update_state(state=states.SUCCESS)
    result = "OK (task_all_full_update)"
    return result


@celery.task(bind=True)
def task_all_update(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" task_all_update [start] ")
    logger.info("------------------------------------------------------------")
    all_dispachter_matrix_service.update()
    logger.info("------------------------------------------------------------")
    logger.info(" task_all_update [done] ")
    logger.info("------------------------------------------------------------")
    self.update_state(state=states.SUCCESS)
    result = "OK (task_all_update)"
    return result

# ----------------------------------------------------------------------------------------------------------------
#  URL Routes for Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


@blueprint_app_all.route('/task/download')
def url_task_all_download():
    app.logger.info("url_task_all_download_all_files [start]")
    all_dispachter_matrix_service.download()
    app.logger.info("url_task_all_download_all_files [done]")
    return redirect(url_for('app_all.url_all_info'))


@blueprint_app_all.route('/task/import')
def url_task_all_import():
    app.logger.info("url_task_all_import_all_files [start]")
    task_all_import_file.apply_async()
    flash(message="async url_task_all_import_all_files [start]", category="warning")
    app.logger.warn("async url_task_all_import_all_files [start]")
    app.logger.info("url_task_all_import_all_files [done]")
    return redirect(url_for('app_all.url_all_info'))


@blueprint_app_all.route('/task/full/update/dimension_tables')
def url_task_all_full_update_dimension_tables():
    app.logger.info("url_task_all_update_full_dimension_tables [start]")
    task_all_update_full_dimension_tables.apply_async()
    flash(message="async task_all_update_full_dimension_tables [start]", category="warning")
    app.logger.warn("async task_all_update_full_dimension_tables [start]")
    app.logger.info("url_task_all_update_full_dimension_tables [done]")
    return redirect(url_for('app_all.url_all_info'))


@blueprint_app_all.route('/task/update/dimension_tables')
def url_task_all_update_dimension_tables():
    app.logger.info("url_task_all_update_dimension_tables [start]")
    task_all_update_dimension_tables.apply_async()
    flash(message="async task_all_update_dimension_tables [start]", category="warning")
    app.logger.warn("async task_all_update_dimension_tables [start]")
    app.logger.info("url_task_all_update_dimension_tables [done]")
    return redirect(url_for('app_all.url_all_info'))


@blueprint_app_all.route('/task/full/update/fact_table')
def url_task_all_full_update_fact_table():
    app.logger.info("url_task_all_full_update_fact_table [start]")
    task_all_full_update_fact_table.apply_async()
    flash(message="async task_all_full_update_fact_table [start]", category="warning")
    app.logger.warn("async task_all_full_update_fact_table [start]")
    app.logger.info("url_task_all_full_update_fact_table [done]")
    return redirect(url_for('app_all.url_all_info'))


@blueprint_app_all.route('/task/update/fact_table')
def url_task_all_update_fact_table():
    app.logger.info("url_task_all_update_fact_table [start]")
    task_all_update_fact_table.apply_async()
    flash(message="async task_all_update_fact_table [start]", category="warning")
    app.logger.warn("async task_all_update_fact_table [start]")
    app.logger.info("url_task_all_update_fact_table [done]")
    return redirect(url_for('app_all.url_all_info'))


@blueprint_app_all.route('/task/full/update')
def url_task_all_full_update():
    app.logger.info("url_task_all_full_update [start]")
    all_dispachter_matrix_service.download()
    task_all_full_update.apply_async()
    flash(message="async task_all_full_update [start]", category="warning")
    app.logger.warn("async task_all_full_update [start]")
    app.logger.info("url_task_all_full_update [done]")
    return redirect(url_for('app_all.url_all_info'))


@blueprint_app_all.route('/task/update')
def url_task_all_update():
    app.logger.info("url_task_all_update [start]")
    all_dispachter_matrix_service.download()
    task_all_update.apply_async()
    flash(message="async task_all_update [start]", category="warning")
    app.logger.warn("async task_all_update [start]")
    app.logger.info("url_task_all_update [done]")
    return redirect(url_for('app_all.url_all_info'))
