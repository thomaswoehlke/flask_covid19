from flask import render_template, redirect, url_for, flash, Blueprint
from celery import states
from celery.utils.log import get_task_logger
from flask_login import login_required

from flask_covid19.blueprints.app_web.web_model_transient import WebPageContent

from flask_covid19.blueprints.data_divi.divi_model_import import DiviImport
from flask_covid19.blueprints.data_divi.divi_model import DiviData

from flask_covid19.blueprints.app_web.web_services import divi_service
from flask_covid19.blueprints.data_divi.divi_test_service import DiviTestService
from flask_covid19.blueprints.data_divi.divi_views import app, db, celery, app_divi

divi_test_service = DiviTestService(db, divi_service)



# ---------------------------------------------------------------------------------------------------------------
#  Url Routes Frontend
# ---------------------------------------------------------------------------------------------------------------


@app_divi.route('/test/tests')
@login_required
def url_divi_test_tests():
    page_info = WebPageContent('DIVI', "Tests")
    return render_template(
        'divi/divi_tests.html',
        page_info=page_info)


@app_divi.route('/test/divi_import/countries')
@login_required
def url_divi_test_divi_import_countries():
    flash("url_divi_mytest - START: DiviImport.countries()")
    app.logger.info("url_divi_mytest - START: DiviImport.countries()")
    i = 0
    for c in DiviImport.countries():
        i += 1
        line = " | " + str(i) + " | " + c.countries.country_code + " | " + c.countries.country + " | " \
               + c.countries.divi_region + " | "
        app.logger.info(line)
    flash("url_divi_mytest - DONE: DiviImport.countries()")
    return redirect(url_for('divi_test.url_divi_test_tests'))


@app_divi.route('/test/divi_import/get_new_dates_as_array')
@login_required
def url_divi_test_divi_import_get_new_dates_as_array():
    app.logger.info("url_divi_mytest - DONE: DiviImport.countries()")
    flash("url_divi_mytest - START: DiviImport.get_new_dates_as_array()")
    app.logger.info("url_divi_mytest - START: DiviImport.get_new_dates_as_array()")
    app.logger.info("DiviImport.get_new_dates_as_array():")
    i = 0
    for date_reported in DiviImport.get_new_dates_as_array():
        i += 1
        line = " | " + str(i) + " | " + date_reported + " | "
        app.logger.info(line)
    flash("url_divi_mytest - DONE: DiviImport.get_new_dates_as_array()")
    app.logger.info("url_divi_mytest - DONE: DiviImport.get_new_dates_as_array()")
    return redirect(url_for('divi_test.url_divi_test_tests'))


@app_divi.route('/test/divi_data/get_datum_of_all_divi_data')
@login_required
def url_divi_test_divi_data_get_datum_of_all_divi_data():
    app.logger.info("url_divi_test_divi_data_get_datum_of_all_divi_data - DONE: DiviData.get_datum_of_all_divi_data()")
    flash("url_divi_test_divi_data_get_datum_of_all_divi_data - START: DiviData.get_datum_of_all_divi_data()")
    for datum in DiviData.get_datum_of_all_data():
        app.logger.info(str(datum))
    flash("url_divi_test_divi_data_get_datum_of_all_divi_data - DONE: DiviData.get_datum_of_all_divi_data()")
    app.logger.info("url_divi_test_divi_data_get_datum_of_all_divi_data - DONE: DiviData.get_datum_of_all_divi_data()")
    return redirect(url_for('divi_test.url_divi_test_tests'))


@app_divi.route('/test/divi_data/get_datum_of_all_divi_import')
@login_required
def url_divi_test_divi_data_get_datum_of_all_divi_import():
    app.logger.info("url_divi_test_divi_data_get_datum_of_all_divi_import - START: DiviImport.get_datum_of_all_divi_import()")
    flash("url_divi_test_divi_data_get_datum_of_all_divi_import - START: DiviImport.get_datum_of_all_divi_import()")
    for datum in DiviImport.get_datum_of_all_divi_import():
        app.logger.info(str(datum))
    flash("url_divi_test_divi_data_get_datum_of_all_divi_import - DONE: DiviImport.get_datum_of_all_divi_import()")
    app.logger.info("url_divi_test_divi_data_get_datum_of_all_divi_import - DONE: DiviImport.get_datum_of_all_divi_import()")
    return redirect(url_for('divi_test.url_divi_test_tests'))


@app_divi.route('/test/divi_service/service_update/divi_import_get_new_dates_as_array')
@login_required
def url_divi_test_divi_service_divi_import_get_new_dates_as_array():
    app.logger.info("url_divi_test_divi_import_get_new_dates_as_array - START: DiviService.divi_import_get_new_dates_as_array()")
    flash("url_divi_test_divi_import_get_new_dates_as_array - START: DiviService.divi_import_get_new_dates_as_array()")
    for datum in divi_service.service_update.get_new_dates_as_array_from_divi_import():
        app.logger.info(str(datum))
    flash("url_divi_test_divi_import_get_new_dates_as_array - DONE: DiviService.divi_import_get_new_dates_as_array()")
    app.logger.info("url_divi_test_divi_import_get_new_dates_as_array - DONE: DiviService.divi_import_get_new_dates_as_array()")
    return redirect(url_for('divi_test.url_divi_test_tests'))


@app_divi.route('/test/divi_test_service/delete_last_day')
@login_required
def url_divi_test_divi_test_service_delete_last_days_data():
    app.logger.info("url_divi_test_divi_test_service_delete_last_days_data - START: DiviService.divi_import_get_new_dates_as_array()")
    flash("url_divi_test_divi_test_service_delete_last_days_data - START: DiviService.divi_import_get_new_dates_as_array()")
    divi_test_service.delete_last_day()
    flash("url_divi_test_divi_test_service_delete_last_days_data - DONE: DiviService.divi_import_get_new_dates_as_array()")
    app.logger.info("url_divi_test_divi_test_service_delete_last_days_data - DONE: DiviService.divi_import_get_new_dates_as_array()")
    return redirect(url_for('divi_test.url_divi_test_tests'))


# ----------------------------------------------------------------------------------------------------------------
#  Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


@celery.task(bind=True)
def task_divi_test_update_star_schema_incremental(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_divi_test_update_star_schema_incremental [OK] ")
    logger.info("------------------------------------------------------------")
    divi_test_service.run_update_star_schema_incremental()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_divi_test_update_star_schema_incremental)"
    return result

# ----------------------------------------------------------------------------------------------------------------
#  URL Routes for Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


@app_divi.route('/test/task/update_star_schema_incremental')
@login_required
def url_task_divi_test_update_star_schema_incremental():
    app.logger.info("url_task_divi_update_star_schema_incremental - START: task_divi_update_star_schema_incremental()")
    flash("url_task_divi_update_star_schema_incremental - START: task_divi_update_star_schema_incremental()")
    task_divi_test_update_star_schema_incremental.apply_async()
    flash("url_task_divi_update_star_schema_incremental - DONE: task_divi_update_star_schema_incremental()")
    app.logger.info("url_task_divi_update_star_schema_incremental - DONE: task_divi_update_star_schema_incremental()")
    return redirect(url_for('divi_test.url_divi_test_tests'))
