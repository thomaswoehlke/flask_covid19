from flask import render_template, redirect, url_for, flash, Blueprint
from celery import states
from celery.utils.log import get_task_logger

from app_config.database import app, celery
from app_web.web_dispachter_matrix_service import all_dispachter_matrix_service, AllDataServiceDispachterMatrix
from app_web.web_model_transient import WebPageContent

drop_and_create_data_again = True

blueprint_app_all = Blueprint('app_all', __name__, template_folder='templates', url_prefix='/app/all')


# ---------------------------------------------------------------------------------------------------------------
#  Url Routes Frontend
# ---------------------------------------------------------------------------------------------------------------

class AllUrls:

    @staticmethod
    @blueprint_app_all.route('/info')
    def url_all_info():
        page_info = WebPageContent('All', "Info")
        return render_template(
            'app_all/app_all_info.html',
            page_info=page_info)

    @staticmethod
    @blueprint_app_all.route('/delete_last_day')
    def url_all_delete_last_day():
        app.logger.info("url_all_delete_last_day [start]")
        flash("url_all_delete_last_day [start]")
        all_dispachter_matrix_service.delete_last_day()
        flash("url_all_delete_last_day [done]")
        app.logger.info("url_all_delete_last_day [done]")
        return redirect(url_for('app_all.url_all_info'))


all_urls = AllUrls()

# ----------------------------------------------------------------------------------------------------------------
#  Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


class AllTasks:

    @staticmethod
    @celery.task(bind=True)
    def task_all_alive_message(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" task_all_alive_message [received] ")
            app.logger.info("------------------------------------------------------------")
        self.update_state(state=states.SUCCESS)
        result = "OK (task_all_alive_message)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_all_import_file(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" task_all_import_file [start] ")
            app.logger.info("------------------------------------------------------------")
            all_dispachter_matrix_service.import_file()
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" task_all_import_file [done] ")
            app.logger.info("------------------------------------------------------------")
        self.update_state(state=states.SUCCESS)
        result = "OK (task_all_import_all_files)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_all_update_full_dimension_tables(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" task_all_update_full_dimension_tables [start] ")
            app.logger.info("------------------------------------------------------------")
            all_dispachter_matrix_service.full_update_dimension_tables()
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" task_all_update_full_dimension_tables [done] ")
            app.logger.info("------------------------------------------------------------")
        self.update_state(state=states.SUCCESS)
        result = "OK (task_all_update_full_dimension_tables)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_all_update_dimension_tables(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" task_all_update_dimension_tables [start] ")
            app.logger.info("------------------------------------------------------------")
            all_dispachter_matrix_service.update_dimension_tables()
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" task_all_update_dimension_tables [done] ")
            app.logger.info("------------------------------------------------------------")
        self.update_state(state=states.SUCCESS)
        result = "OK (task_all_update_dimension_tables)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_all_full_update_fact_table(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" task_all_update_fact_table_initial_only [start] ")
            app.logger.info("------------------------------------------------------------")
            all_dispachter_matrix_service.full_update_fact_table()
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" task_all_update_fact_table_initial_only [done] ")
            app.logger.info("------------------------------------------------------------")
        self.update_state(state=states.SUCCESS)
        result = "OK (task_all_update_fact_table_initial_only)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_all_update_fact_table(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" task_all_update_fact_table [start] ")
            app.logger.info("------------------------------------------------------------")
            all_dispachter_matrix_service.update_fact_table()
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" task_all_update_fact_table [done] ")
            app.logger.info("------------------------------------------------------------")
        self.update_state(state=states.SUCCESS)
        result = "OK (task_all_update_fact_table)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_all_full_update(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" task_all_full_update [start] ")
            app.logger.info("------------------------------------------------------------")
            all_dispachter_matrix_service.full_update()
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" task_all_full_update [done] ")
            app.logger.info("------------------------------------------------------------")
        self.update_state(state=states.SUCCESS)
        result = "OK (task_all_full_update)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_all_update(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" task_all_update [start] ")
            app.logger.info("------------------------------------------------------------")
            all_dispachter_matrix_service.update()
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" task_all_update [done] ")
            app.logger.info("------------------------------------------------------------")
        self.update_state(state=states.SUCCESS)
        result = "OK (task_all_update)"
        return result


all_tasks = AllTasks()

# ----------------------------------------------------------------------------------------------------------------
#  URL Routes for Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


class AllTaskUrls:

    @staticmethod
    @blueprint_app_all.route('/task/download')
    def url_task_all_download():
        app.logger.info("url_task_all_download_all_files [start]")
        all_dispachter_matrix_service.download()
        app.logger.info("url_task_all_download_all_files [done]")
        return redirect(url_for('app_all.url_all_info'))

    @staticmethod
    @blueprint_app_all.route('/task/import')
    def url_task_all_import():
        app.logger.info("url_task_all_import_all_files [start]")
        all_tasks.task_all_import_file.apply_async()
        flash(message="async url_task_all_import_all_files [start]", category="warning")
        app.logger.warn("async url_task_all_import_all_files [start]")
        app.logger.info("url_task_all_import_all_files [done]")
        return redirect(url_for('app_all.url_all_info'))

    @staticmethod
    @blueprint_app_all.route('/task/full/update/dimension_tables')
    def url_task_all_full_update_dimension_tables():
        app.logger.info("url_task_all_update_full_dimension_tables [start]")
        all_tasks.task_all_update_full_dimension_tables.apply_async()
        flash(message="async task_all_update_full_dimension_tables [start]", category="warning")
        app.logger.warn("async task_all_update_full_dimension_tables [start]")
        app.logger.info("url_task_all_update_full_dimension_tables [done]")
        return redirect(url_for('app_all.url_all_info'))

    @staticmethod
    @blueprint_app_all.route('/task/update/dimension_tables')
    def url_task_all_update_dimension_tables():
        app.logger.info("url_task_all_update_dimension_tables [start]")
        all_tasks.task_all_update_dimension_tables.apply_async()
        flash(message="async task_all_update_dimension_tables [start]", category="warning")
        app.logger.warn("async task_all_update_dimension_tables [start]")
        app.logger.info("url_task_all_update_dimension_tables [done]")
        return redirect(url_for('app_all.url_all_info'))

    @staticmethod
    @blueprint_app_all.route('/task/full/update/fact_table')
    def url_task_all_full_update_fact_table():
        app.logger.info("url_task_all_full_update_fact_table [start]")
        all_tasks.task_all_full_update_fact_table.apply_async()
        flash(message="async task_all_full_update_fact_table [start]", category="warning")
        app.logger.warn("async task_all_full_update_fact_table [start]")
        app.logger.info("url_task_all_full_update_fact_table [done]")
        return redirect(url_for('app_all.url_all_info'))

    @staticmethod
    @blueprint_app_all.route('/task/update/fact_table')
    def url_task_all_update_fact_table():
        app.logger.info("url_task_all_update_fact_table [start]")
        all_tasks.task_all_update_fact_table.apply_async()
        flash(message="async task_all_update_fact_table [start]", category="warning")
        app.logger.warn("async task_all_update_fact_table [start]")
        app.logger.info("url_task_all_update_fact_table [done]")
        return redirect(url_for('app_all.url_all_info'))

    @staticmethod
    @blueprint_app_all.route('/task/full/update')
    def url_task_all_full_update():
        app.logger.info("url_task_all_full_update [start]")
        all_dispachter_matrix_service.download()
        all_tasks.task_all_full_update.apply_async()
        flash(message="async task_all_full_update [start]", category="warning")
        app.logger.warn("async task_all_full_update [start]")
        app.logger.info("url_task_all_full_update [done]")
        return redirect(url_for('app_all.url_all_info'))

    @staticmethod
    @blueprint_app_all.route('/task/update')
    def url_task_all_update():
        app.logger.info("url_task_all_update [start]")
        all_dispachter_matrix_service.download()
        all_tasks.task_all_update.apply_async()
        flash(message="async task_all_update [start]", category="warning")
        app.logger.warn("async task_all_update [start]")
        app.logger.info("url_task_all_update [done]")
        return redirect(url_for('app_all.url_all_info'))


all_task_urls = AllTaskUrls()