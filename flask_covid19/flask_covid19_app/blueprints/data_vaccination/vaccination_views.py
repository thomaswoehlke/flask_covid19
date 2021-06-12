from flask import render_template, redirect, url_for, flash, Blueprint
from celery import states
from celery.utils.log import get_task_logger
from flask_admin.contrib.sqla import ModelView

from flask_covid19_conf.database import app, admin, db, celery
from flask_covid19_app.blueprints.app_web.web_dispachter_matrix_service import vaccination_service

from flask_covid19_app.blueprints.data_vaccination.vaccination_model import VaccinationData
from flask_covid19_app.blueprints.data_vaccination.vaccination_model import VaccinationDateReported
from flask_covid19_app.blueprints.data_vaccination.vaccination_model_import import VaccinationImport, VaccinationFlat
from flask_covid19_app.blueprints.app_web.web_model_transient import WebPageContent


app_vaccination = Blueprint('vaccination', __name__, template_folder='templates', url_prefix='/vaccination')

admin.add_view(ModelView(VaccinationImport, db.session, category="Vaccination"))
admin.add_view(ModelView(VaccinationFlat, db.session, category="Vaccination"))
admin.add_view(ModelView(VaccinationDateReported, db.session, category="Vaccination"))
admin.add_view(ModelView(VaccinationData, db.session, category="Vaccination"))


# ---------------------------------------------------------------------------------------------------------------
#  Url Routes Frontend
# ---------------------------------------------------------------------------------------------------------------


@app_vaccination.route('')
@app_vaccination.route('/')
def url_vaccination_root():
    return redirect(url_for('vaccination.url_vaccination_info'))


@app_vaccination.route('/info')
def url_vaccination_info():
    page_info = WebPageContent('Vaccination', "Info")
    return render_template(
        'vaccination/vaccination_info.html',
        page_info=page_info)


@app_vaccination.route('/imported/page/<int:page>')
@app_vaccination.route('/imported')
def url_vaccination_imported(page=1):
    page_info = WebPageContent('Vaccination', "Data: Germany Timeline imported")
    page_data = VaccinationImport.get_all_as_page(page)
    return render_template(
        'vaccination/imported/vaccination_imported.html',
        page_data=page_data,
        page_info=page_info)


@app_vaccination.route('/data/page/<int:page>')
@app_vaccination.route('/data')
def url_vaccination_data(page=1):
    page_info = WebPageContent('Vaccination', "Data: Germany Timeline")
    page_data = VaccinationData.get_all_as_page(page)
    return render_template(
        'vaccination/data/vaccination_data.html',
        page_data=page_data,
        page_info=page_info)


@app_vaccination.route('/delete_last_day')
def url_vaccination_delete_last_day():
    app.logger.info("url_vaccination_delete_last_day [start]")
    flash("url_vaccination_delete_last_day [start]")
    vaccination_service.delete_last_day()
    flash("url_vaccination_delete_last_day [done]")
    app.logger.info("url_vaccination_delete_last_day [done]")
    return redirect(url_for('vaccination.url_vaccination_info'))

# ----------------------------------------------------------------------------------------------------------------
#  Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


@celery.task(bind=True)
def task_vaccination_import_file(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_vaccination_import [OK] ")
    logger.info("------------------------------------------------------------")
    vaccination_service.import_file()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_vaccination_import)"
    return result


@celery.task(bind=True)
def task_vaccination_full_update_dimension_tables(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_vaccination_full_update_dimension_tables [OK] ")
    logger.info("------------------------------------------------------------")
    vaccination_service.full_update_dimension_tables()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_vaccination_full_update_dimension_tables)"
    return result


@celery.task(bind=True)
def task_vaccination_update_dimension_tables(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_vaccination_update_dimension_tables [OK] ")
    logger.info("------------------------------------------------------------")
    vaccination_service.update_dimension_tables()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_vaccination_update_dimension_tables)"
    return result


@celery.task(bind=True)
def task_vaccination_update_facttable(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_vaccination_update_facttable [OK] ")
    logger.info("------------------------------------------------------------")
    vaccination_service.update_fact_table()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_vaccination_update_facttable)"
    return result


@celery.task(bind=True)
def task_vaccination_full_update_facttable(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_vaccination_full_update_facttable [OK] ")
    logger.info("------------------------------------------------------------")
    vaccination_service.full_update_fact_table()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_vaccination_full_update_facttable)"
    return result


@celery.task(bind=True)
def task_vaccination_update(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_vaccination_update [OK] ")
    logger.info("------------------------------------------------------------")
    vaccination_service.full_update()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_vaccination_update)"
    return result


@celery.task(bind=True)
def task_vaccination_full_update(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_vaccination_full_update [OK] ")
    logger.info("------------------------------------------------------------")
    vaccination_service.full_update()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_vaccination_full_update)"
    return result

# ----------------------------------------------------------------------------------------------------------------
# URL Routes for Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


@app_vaccination.route('/task/download')
def url_task_vaccination_download():
    flash("vaccination_service.download started")
    vaccination_service.download()
    flash("vaccination_service.download done")
    return redirect(url_for('vaccination.url_vaccination_info'))


@app_vaccination.route('/task/import')
def url_task_vaccination_import():
    task_vaccination_import_file.apply_async()
    flash("task_vaccination_import_file started")
    return redirect(url_for('vaccination.url_vaccination_info'))


@app_vaccination.route('/task/update/full/dimension-tables')
def url_task_vaccination_full_update_dimension_tables():
    flash("url_vaccination_task_update_dimensiontables_only started")
    task_vaccination_full_update_dimension_tables.apply_async()
    return redirect(url_for('vaccination.url_vaccination_info'))


@app_vaccination.route('/task/update/dimension-tables')
def url_task_vaccination_update_dimension_tables():
    flash("url_vaccination_task_update_dimensiontables_only started")
    task_vaccination_update_dimension_tables.apply_async()
    return redirect(url_for('vaccination.url_vaccination_info'))


@app_vaccination.route('/task/update/fact-table/incremental/only')
def url_task_vaccination_update_facttable():
    flash("url_vaccination_task_update_facttable_incremental_only started")
    task_vaccination_update_facttable.apply_async()
    return redirect(url_for('vaccination.url_vaccination_info'))


@app_vaccination.route('/task/update/fact-table/initial/only')
def url_task_vaccination_full_update_facttable():
    flash("url_vaccination_task_update_facttable_initial_only started")
    task_vaccination_full_update_facttable.apply_async()
    return redirect(url_for('vaccination.url_vaccination_info'))


@app_vaccination.route('/task/full/update/')
def url_task_vaccination_full_update():
    vaccination_service.download()
    flash("vaccination_service.download done")
    task_vaccination_full_update.apply_async()
    flash("task_vaccination_full_update started")
    return redirect(url_for('vaccination.url_vaccination_info'))


@app_vaccination.route('/task/update')
def url_task_vaccination_update():
    vaccination_service.download()
    flash("vaccination_service.download done")
    task_vaccination_update.apply_async()
    flash("task_vaccination_update started")
    return redirect(url_for('vaccination.url_vaccination_info'))
