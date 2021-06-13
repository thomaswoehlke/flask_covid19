from flask import render_template, redirect, url_for, flash, Blueprint
from sqlalchemy.exc import OperationalError
from celery import states
from celery.utils.log import get_task_logger
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required

from flask_covid19_conf.database import app, admin, db, celery # , cache
from app_web.web_dispachter_matrix_service import who_service
from app_web.web_model_transient import WebPageContent

from data_who.who_model_import import WhoImport, WhoFlat
from data_who.who_model import WhoCountryRegion, WhoCountry, WhoDateReported, WhoData
from data_who.who_test_service import WhoTestService

who_test_service = WhoTestService(db, who_service)

app_who = Blueprint('who', __name__, template_folder='templates', url_prefix='/who')

admin.add_view(ModelView(WhoImport, db.session, category="WHO"))
admin.add_view(ModelView(WhoFlat, db.session, category="WHO"))
admin.add_view(ModelView(WhoDateReported, db.session, category="WHO"))
admin.add_view(ModelView(WhoCountryRegion, db.session, category="WHO"))
admin.add_view(ModelView(WhoCountry, db.session, category="WHO"))
admin.add_view(ModelView(WhoData, db.session, category="WHO"))


# ---------------------------------------------------------------------------------------------------------------
#  Url Routes Frontend
# ---------------------------------------------------------------------------------------------------------------


@app_who.route('')
@app_who.route('/')
def url_who_root():
    return redirect(url_for('who.url_who_info'))


@app_who.route('/info')
def url_who_info():
    page_info = WebPageContent('WHO', "Info")
    return render_template(
        'who/who_info.html',
        page_info=page_info)


@app_who.route('/imported/page/<int:page>')
@app_who.route('/imported')
@login_required
def url_who_imported(page=1):
    page_info = WebPageContent('WHO', "Last Import")
    try:
        page_data = WhoImport.get_all(page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'who/imported/who_imported.html',
        page_data=page_data,
        page_info=page_info)


@app_who.route('/flat/page/<int:page>')
@app_who.route('/flat')
@login_required
def url_who_flat(page=1):
    page_info = WebPageContent('WHO', "Flat")
    try:
        page_data = WhoFlat.get_all(page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'who/flat/who_flat.html',
        page_data=page_data,
        page_info=page_info)


@app_who.route('/date_reported/all/page/<int:page>')
@app_who.route('/date_reported/all')
def url_who_date_reported_all(page: int = 1):
    page_info = WebPageContent('WHO', "Date Reported", "All")
    try:
        page_data = WhoDateReported.get_all(page)
    except OperationalError:
        flash("No regions in the database.")
        page_data = None
    return render_template(
        'who/date_reported/all/who_date_reported_all.html',
        page_data=page_data,
        page_info=page_info)


@app_who.route('/date_reported/<int:date_reported_id>/page/<int:page>')
@app_who.route('/date_reported/<int:date_reported_id>')
def url_who_date_reported(date_reported_id: int, page: int = 1):
    date_reported = WhoDateReported.get_by_id(date_reported_id)
    page_info = WebPageContent(
        "Date Reported: " + str(date_reported),
        'WHO',
        "data of all reported countries for WHO date reported " + str(date_reported) + " "
    )
    try:
        page_data = WhoData.get_by_date_reported(date_reported, page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'who/date_reported/one/who_date_reported_one.html',
        who_date_reported=date_reported,
        page_data=page_data,
        page_info=page_info)


@app_who.route('/date_reported/<int:date_reported_id>/cases_new/page/<int:page>')
@app_who.route('/date_reported/<int:date_reported_id>/cases_new')
def url_who_date_reported_cases_new(date_reported_id: int, page: int = 1):
    date_reported = WhoDateReported.get_by_id(date_reported_id)
    page_info = WebPageContent(
        "Date Reported: " + str(date_reported),
        'WHO',
        "data of all reported countries for WHO date reported " + str(date_reported) + " "
    )
    try:
        page_data = WhoData.get_by_date_reported_order_by_cases_new(date_reported, page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'who/date_reported/cases/who_date_reported_one_cases_new.html',
        who_date_reported=date_reported,
        page_data=page_data,
        page_info=page_info)


@app_who.route('/date_reported/<int:date_reported_id>/cases_cumulative/page/<int:page>')
@app_who.route('/date_reported/<int:date_reported_id>/cases_cumulative')
def url_who_date_reported_cases_cumulative(date_reported_id: int, page: int = 1):
    date_reported = WhoDateReported.get_by_id(date_reported_id)
    page_info = WebPageContent(
        "Date Reported: " + str(date_reported),
        'WHO',
        "data of all reported countries for WHO date reported " + str(date_reported) + " "
    )
    try:
        page_data = WhoData.get_by_date_reported_order_by_cases_cumulative(date_reported, page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'who/date_reported/cases/who_date_reported_one_cases_cumulative.html',
        who_date_reported=date_reported,
        page_data=page_data,
        page_info=page_info)


@app_who.route('/date_reported/<int:date_reported_id>/deaths_new/page/<int:page>')
@app_who.route('/date_reported/<int:date_reported_id>/deaths_new')
def url_who_date_reported_deaths_new(date_reported_id: int, page: int = 1):
    date_reported = WhoDateReported.get_by_id(date_reported_id)
    page_info = WebPageContent(
        "Date Reported: " + str(date_reported),
        'WHO',
        "data of all reported countries for WHO date reported " + str(date_reported) + " "
    )
    try:
        page_data = WhoData.get_by_date_reported_order_by_deaths_new(date_reported, page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'who/date_reported/deaths/who_date_reported_one_deaths_new.html',
        who_date_reported=date_reported,
        page_data=page_data,
        page_info=page_info)


@app_who.route('/date_reported/<int:date_reported_id>/deaths_cumulative/page/<int:page>')
@app_who.route('/date_reported/<int:date_reported_id>/deaths_cumulative')
def url_who_date_reported_deaths_cumulative(date_reported_id: int, page: int = 1):
    date_reported = WhoDateReported.get_by_id(date_reported_id)
    page_info = WebPageContent(
        "Date Reported: " + str(date_reported) ,
        'WHO',
        "data of all reported countries for WHO date reported " + str(date_reported) + " "
    )
    try:
        page_data = WhoData.get_by_date_reported_order_by_deaths_cumulative(date_reported, page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'who/date_reported/deaths/who_date_reported_one_deaths_cumulative.html',
        who_date_reported=date_reported,
        page_data=page_data,
        page_info=page_info)


@app_who.route('/region/all/page/<int:page>')
@app_who.route('/region/all')
def url_who_region_all(page: int = 1):
    page_info = WebPageContent('WHO', "Region", "All")
    try:
        page_data = WhoCountryRegion.get_all(page)
    except OperationalError:
        flash("No regions in the database.")
        page_data = None
    return render_template(
        'who/region/all/who_region_all.html',
        page_data=page_data,
        page_info=page_info)


@app_who.route('/region/<int:region_id>/page/<int:page>')
@app_who.route('/region/<int:region_id>')
def url_who_region(region_id: int, page: int = 1):
    who_region = None
    page_info = WebPageContent("Countries", "WHO Region")
    try:
        who_region = WhoCountryRegion.get_by_id(region_id)
        page_data = WhoCountry.get_by_location_group(who_region, page)
        page_info.title = str(who_region)
        page_info.subtitle = "WHO Region"
        page_info.subtitle_info = "Countries of WHO Region " + str(who_region)
    except OperationalError:
        flash("No countries of that region in the database.")
        page_data = None
    return render_template(
        'who/region/one/who_region_one.html',
        who_region=who_region,
        page_data=page_data,
        page_info=page_info)


@app_who.route('/country/all/page/<int:page>')
@app_who.route('/country/all')
def url_who_country_all(page: int = 1):
    page_info = WebPageContent('WHO', "Countries", "All")
    try:
        page_data = WhoCountry.get_all(page)
    except OperationalError:
        flash("No regions in the database.")
        page_data = None
    return render_template(
        'who/country/all/who_country_all.html',
        page_data=page_data,
        page_info=page_info)


@app_who.route('/country/<int:country_id>/page/<int:page>')
@app_who.route('/country/<int:country_id>')
def url_who_country(country_id: int, page: int = 1):
    who_country = WhoCountry.get_by_id(country_id)
    page_data = WhoData.get_by_location(who_country, page)
    page_info = WebPageContent(who_country.location,
           "Country " + who_country.location,
           "Data per Day in Country " + str(who_country))
    return render_template(
        'who/country/one/who_country_one.html',
        who_country=who_country,
        page_data=page_data,
        page_info=page_info)


@app_who.route('/country/<int:country_id>/cases_new/page/<int:page>')
@app_who.route('/country/<int:country_id>/cases_new')
def url_who_country_cases_new(country_id: int, page: int = 1):
    who_country = WhoCountry.get_by_id(country_id)
    page_data = WhoData.get_by_location_order_by_cases_new(who_country, page)
    page_info = WebPageContent(who_country.location,
           "Country " + who_country.location,
           "Data per Day in Country " + str(who_country))
    return render_template(
        'who/country/cases/who_country_one_cases_new.html',
        who_country=who_country,
        page_data=page_data,
        page_info=page_info)


@app_who.route('/country/<int:country_id>/cases_cumulative/page/<int:page>')
@app_who.route('/country/<int:country_id>/cases_cumulative')
def url_who_country_cases_cumulative(country_id: int, page: int = 1):
    who_country = WhoCountry.get_by_id(country_id)
    page_data = WhoData.get_by_location_order_by_cases_cumulative(who_country, page)
    page_info = WebPageContent(who_country.location,
           "Country " + who_country.location,
           "Data per Day in Country " + str(who_country))
    return render_template(
        'who/country/cases/who_country_one_cases_cumulative.html',
        who_country=who_country,
        page_data=page_data,
        page_info=page_info)


@app_who.route('/country/<int:country_id>/deaths_new/page/<int:page>')
@app_who.route('/country/<int:country_id>/deaths_new')
def url_who_country_deaths_new(country_id: int, page: int = 1):
    who_country = WhoCountry.get_by_id(country_id)
    page_data = WhoData.get_by_location_order_by_deaths_new(who_country, page)
    page_info = WebPageContent(who_country.location,
           "Country " + who_country.location,
           "Data per Day in Country " + str(who_country))
    return render_template(
        'who/country/deaths/who_country_one_deaths_new.html',
        who_country=who_country,
        page_data=page_data,
        page_info=page_info)


@app_who.route('/country/<int:country_id>/deaths_cumulative/page/<int:page>')
@app_who.route('/country/<int:country_id>/deaths_cumulative')
def url_who_country_deaths_cumulative(country_id: int, page: int = 1):
    who_country = WhoCountry.get_by_id(country_id)
    page_data = WhoData.get_by_location_order_by_deaths_cumulative(who_country, page)
    page_info = WebPageContent(who_country.location,
           "Country " + who_country.location,
           "Data per Day in Country " + str(who_country))
    return render_template(
        'who/country/deaths/who_country_one_deaths_cumulative.html',
        who_country=who_country,
        page_data=page_data,
        page_info=page_info)


@app_who.route('/germany/page/<int:page>')
@app_who.route('/germany')
def url_who_germany(page: int = 1):
    page_info = WebPageContent('WHO', "Germany")
    who_country_germany = WhoCountry.find_by_location_code("DE")
    if who_country_germany is None:
        flash('country: Germany not found in Database', category='error')
        return redirect(url_for('who.url_who_info'))
    page_data = WhoData.get_by_location(who_country_germany, page)
    return render_template(
        'who/country/germany/who_country_germany.html',
        who_country=who_country_germany,
        page_data=page_data,
        page_info=page_info)


@app_who.route('/delete_last_day')
def url_who_delete_last_day():
    app.logger.info("url_who_delete_last_day [start]")
    flash("url_who_delete_last_day [start]")
    who_service.delete_last_day()
    flash("url_who_delete_last_day [done]")
    app.logger.info("url_who_delete_last_day [done]")
    return redirect(url_for('who.url_who_info'))


@app_who.route('/mytest')
def url_who_mytest():
    flash("url_who_mytest - START: WhoImport.countries()")
    app.logger.info("url_who_mytest - START: WhoImport.countries()")
    i = 0
    for c in WhoImport.countries():
        i += 1
        line = " | " + str(i) + " | " + c.countries.country_code + " | " + c.countries.country + " | " + c.countries.who_region + " | "
        app.logger.info(line)
    flash("url_who_mytest - DONE: WhoImport.countries()")
    app.logger.info("url_who_mytest - DONE: WhoImport.countries()")
    flash("url_who_mytest - START: WhoImport.get_new_dates_as_array()")
    app.logger.info("url_who_mytest - START: WhoImport.get_new_dates_as_array()")
    i = 0
    for date_reported in WhoImport.get_new_dates_as_array():
        i += 1
        line = " | " + str(i) + " | " + date_reported + " | "
        app.logger.info(line)
    joungest_datum = WhoDateReported.get_joungest_datum()
    app.logger.info(joungest_datum)
    i = 0
    for who_data in WhoData.get_data_for_one_day(joungest_datum):
        i += 1
        line = " | " + str(i) + " | " + str(who_data.date_reported) + " | " + who_data.country.country + " | "
        app.logger.info(line)
    flash("url_who_mytest - DONE: WhoImport.get_new_dates_as_array()")
    app.logger.info("url_who_mytest - DONE: WhoImport.get_new_dates_as_array()")
    return redirect(url_for('who.url_who_info'))

# ----------------------------------------------------------------------------------------------------------------
#  Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


@celery.task(bind=True)
def task_who_import_files(self):
    # logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    app.logger.info("------------------------------------------------------------")
    app.logger.info(" Received: task_who_import_files [OK] ")
    app.logger.info("------------------------------------------------------------")
    who_service.import_file()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_who_import_files)"
    return result


@celery.task(bind=True)
def task_who_full_update_dimension_tables(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_who_full_update_dimension_tables [OK] ")
    logger.info("------------------------------------------------------------")
    who_service.full_update_dimension_tables()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_who_full_update_dimension_tables)"
    return result


@celery.task(bind=True)
def task_who_update_dimension_tables(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_who_update_dimension_tables [OK] ")
    logger.info("------------------------------------------------------------")
    who_service.update_dimension_tables()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_who_update_dimension_tables)"
    return result


@celery.task(bind=True)
def task_who_full_update_fact_table(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_who_full_update_fact_table [OK] ")
    logger.info("------------------------------------------------------------")
    who_service.full_update_fact_table()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_who_full_update_fact_table)"
    return result


@celery.task(bind=True)
def task_who_update_fact_table(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_who_update_fact_table [OK] ")
    logger.info("------------------------------------------------------------")
    who_service.update_fact_table()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_who_update_fact_table)"
    return result


@celery.task(bind=True)
def task_who_full_update(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_who_full_update [OK] ")
    logger.info("------------------------------------------------------------")
    who_service.full_update()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_who_full_update)"
    return result


@celery.task(bind=True)
def task_who_update(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_who_update [OK] ")
    logger.info("------------------------------------------------------------")
    who_service.update()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_who_update)"
    return result


# ----------------------------------------------------------------------------------------------------------------
#  URL Routes for Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


@app_who.route('/files/download')
@login_required
def url_download_files():
    app.logger.info("url_download_files [start]")
    who_service.download()
    flash("who_service.download_files() [done]")
    app.logger.info("url_download_files [done]")
    return redirect(url_for('who.url_who_info'))


@app_who.route('/task/files/import')
@login_required
def url_task_who_import_files():
    app.logger.info("url_task_who_import_files [start]")
    task_who_import_files.apply_async()
    flash("task_who_import_files [start]")
    flash(message="long running background task started", category="warning")
    app.logger.warn("async task_who_import_files [start]")
    app.logger.info("url_task_who_import_files [done]")
    return redirect(url_for('who.url_who_info'))


@app_who.route('/task/update/full/dimension_tables')
@login_required
def url_task_who_full_update_dimension_tables():
    app.logger.info("url_task_who_full_update_dimension_tables [start]")
    task_who_full_update_dimension_tables.apply_async()
    flash("task_who_full_update_dimension_tables [start]")
    flash(message="long running background task started", category="warning")
    app.logger.warn("async task_who_full_update_dimension_tables [start]")
    app.logger.info("url_task_who_full_update_dimension_tables [done]")
    return redirect(url_for('who.url_who_info'))


@app_who.route('/task/update/dimension_tables')
@login_required
def url_task_who_update_dimension_tables():
    app.logger.info("url_task_who_update_dimension_tables [start]")
    task_who_update_dimension_tables.apply_async()
    flash("task_who_update_dimension_tables [start]")
    flash(message="long running background task started", category="warning")
    app.logger.warn("async task_who_update_dimension_tables [start]")
    app.logger.info("url_task_who_update_dimension_tables [done]")
    return redirect(url_for('who.url_who_info'))


@app_who.route('/task/update/full/fact-table')
@login_required
def url_task_who_full_update_fact_table():
    app.logger.info("url_task_who_full_update_fact_table [start]")
    task_who_full_update_fact_table.apply_async()
    flash("task_who_full_update_fact_table [start]")
    flash(message="long running background task started", category="warning")
    app.logger.warn("async task_who_full_update_fact_table [start]")
    app.logger.info("url_task_who_full_update_fact_table [done]")
    return redirect(url_for('who.url_who_info'))


@app_who.route('/task/update/fact-table')
@login_required
def url_task_who_update_fact_table():
    app.logger.info("url_task_who_update_fact_table [start]")
    task_who_update_fact_table.apply_async()
    flash("task_who_update_fact_table [start]")
    flash(message="long running background task started", category="warning")
    app.logger.warn("async task_who_update_fact_table [start]")
    app.logger.info("url_task_who_update_fact_table [done]")
    return redirect(url_for('who.url_who_info'))


@app_who.route('/task/update/full')
@login_required
def url_task_who_full_update():
    app.logger.info("url_task_who_full_update [start]")
    who_service.download()
    flash("who_service.run_download_only() [done]")
    task_who_full_update.apply_async()
    flash("task_who_full_update [start]")
    flash(message="long running background task started", category="warning")
    app.logger.warn("async task_who_full_update [start]")
    app.logger.info("url_task_who_full_update [done]")
    return redirect(url_for('who.url_who_info'))


@app_who.route('/task/update')
@login_required
def url_task_who_update():
    app.logger.info("url_task_who_update [start]")
    who_service.download()
    flash("who_service.run_download_only() [done]")
    task_who_update.apply_async()
    flash("task_who_update [start]")
    flash(message="long running background task started", category="warning")
    app.logger.warn("async task_who_update [start]")
    app.logger.info("url_task_who_update [done]")
    return redirect(url_for('who.url_who_info'))


# ---------------------------------------------------------------------------------------------------------------
#  Url Routes Frontend TESTS
# ---------------------------------------------------------------------------------------------------------------


@app_who.route('/test/who_import/countries')
@login_required
def url_who_test_who_import_countries():
    flash("url_who_mytest - START: WhoImport.countries()")
    app.logger.info("url_who_mytest - START: WhoImport.countries()")
    i = 0
    for c in WhoImport.countries():
        i += 1
        line = " | " + str(i) + " | " + c.countries.country_code + " | " + c.countries.country + " | " + c.countries.who_region + " | "
        app.logger.info(line)
    flash("url_who_mytest - DONE: WhoImport.countries()")
    return redirect(url_for('who.url_who_info'))


@app_who.route('/test/who_import/get_new_dates_as_array')
@login_required
def url_who_test_who_import_get_new_dates_as_array():
    app.logger.info("url_who_mytest - DONE: WhoImport.countries()")
    flash("url_who_mytest - START: WhoImport.get_new_dates_as_array()")
    app.logger.info("url_who_mytest - START: WhoImport.get_new_dates_as_array()")
    app.logger.info("WhoImport.get_new_dates_as_array():")
    i = 0
    for date_reported in WhoImport.get_new_dates_as_array():
        i += 1
        line = " | " + str(i) + " | " + date_reported + " | "
        app.logger.info(line)
    flash("url_who_mytest - DONE: WhoImport.get_new_dates_as_array()")
    app.logger.info("url_who_mytest - DONE: WhoImport.get_new_dates_as_array()")
    return redirect(url_for('who.url_who_info'))


@app_who.route('/test/who_data/get_datum_of_all_who_data')
@login_required
def url_who_test_who_data_get_datum_of_all_who_data():
    app.logger.info("url_who_test_who_data_get_datum_of_all_who_data - DONE: WhoData.get_datum_of_all_who_data()")
    flash("url_who_test_who_data_get_datum_of_all_who_data - START: WhoData.get_datum_of_all_who_data()")
    for datum in WhoData.get_datum_of_all_data():
        app.logger.info(str(datum))
    flash("url_who_test_who_data_get_datum_of_all_who_data - DONE: WhoData.get_datum_of_all_who_data()")
    app.logger.info("url_who_test_who_data_get_datum_of_all_who_data - DONE: WhoData.get_datum_of_all_who_data()")
    return redirect(url_for('who.url_who_info'))


@app_who.route('/test/who_data/get_datum_of_all_who_import')
@login_required
def url_who_test_who_data_get_datum_of_all_who_import():
    app.logger.info("url_who_test_who_data_get_datum_of_all_who_import - START: WhoImport.get_datum_of_all_who_import()")
    flash("url_who_test_who_data_get_datum_of_all_who_import - START: WhoImport.get_datum_of_all_who_import()")
    for datum in WhoImport.get_datum_of_all_who_import():
        app.logger.info(str(datum))
    flash("url_who_test_who_data_get_datum_of_all_who_import - DONE: WhoImport.get_datum_of_all_who_import()")
    app.logger.info("url_who_test_who_data_get_datum_of_all_who_import - DONE: WhoImport.get_datum_of_all_who_import()")
    return redirect(url_for('who.url_who_info'))


@app_who.route('/test/who_service/service_update/who_import_get_new_dates_as_array')
@login_required
def url_who_test_who_service_who_import_get_new_dates_as_array():
    app.logger.info("url_who_test_who_import_get_new_dates_as_array - START: WhoService.who_import_get_new_dates_as_array()")
    flash("url_who_test_who_import_get_new_dates_as_array - START: WhoService.who_import_get_new_dates_as_array()")
    for datum in who_service.service_update.who_import_get_new_dates_as_array():
        app.logger.info(str(datum))
    flash("url_who_test_who_import_get_new_dates_as_array - DONE: WhoService.who_import_get_new_dates_as_array()")
    app.logger.info("url_who_test_who_import_get_new_dates_as_array - DONE: WhoService.who_import_get_new_dates_as_array()")
    return redirect(url_for('who.url_who_info'))

