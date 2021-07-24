from flask import render_template, redirect, url_for, flash, Blueprint
from sqlalchemy.exc import OperationalError
from flask_admin.contrib.sqla import ModelView
from celery import states
from flask_login import login_required

from app_config.database import app, admin, db, celery
from app_web.web_dispachter_matrix_service import rki_service
from data_rki.rki_model import RkiData, RkiMeldedatum, RkiBundesland, RkiLandkreis
from data_rki.rki_model import RkiAltersgruppe
from data_rki.rki_model_import import RkiImport
from data_rki.rki_model_flat import RkiFlat
from app_web.web_model_transient import WebPageContent

from data_rki.rki_service_test import RkiTestService

drop_and_create_data_again = True

app_rki = Blueprint('rki', __name__, template_folder='templates', url_prefix='/rki')


admin.add_view(ModelView(RkiImport, db.session, category="RKI"))
admin.add_view(ModelView(RkiFlat, db.session, category="RKI"))
admin.add_view(ModelView(RkiMeldedatum, db.session, category="RKI"))
admin.add_view(ModelView(RkiBundesland, db.session, category="RKI"))
admin.add_view(ModelView(RkiLandkreis, db.session, category="RKI"))
admin.add_view(ModelView(RkiAltersgruppe, db.session, category="RKI"))
admin.add_view(ModelView(RkiData, db.session, category="RKI"))


# ---------------------------------------------------------------------------------------------------------------
#  Url Routes Frontend
# ---------------------------------------------------------------------------------------------------------------


class RkiUrls:

    @staticmethod
    @app_rki.route('')
    @app_rki.route('/')
    def url_rki_root():
        return redirect(url_for('rki.url_rki_info'))

    @staticmethod
    @app_rki.route('/info')
    def url_rki_info():
        page_info = WebPageContent('RKI', "Info")
        return render_template(
            'rki/rki_info.html',
            page_info=page_info)

    @staticmethod
    @app_rki.route('/imported/page/<int:page>')
    @app_rki.route('/imported')
    def url_rki_imported(page=1):
        page_info = WebPageContent('RKI', "Last Import")
        try:
            page_data = RkiImport.get_all(page)
        except OperationalError:
            flash("No data in the database.")
            page_data = None
        return render_template(
            'rki/imported/rki_imported.html',
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_rki.route('/flat/page/<int:page>')
    @app_rki.route('/flat')
    def url_rki_flat(page=1):
        page_info = WebPageContent('RKI', "flat")
        try:
            page_data = RkiFlat.get_all(page)
        except OperationalError:
            flash("No data in the database.")
            page_data = None
        return render_template(
            'rki/flat/rki_flat.html',
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_rki.route('/test/page/<int:page>')
    @app_rki.route('/test')
    def url_rki_test(page=1):
        page_info = WebPageContent('RKI', "TEST")
        try:
            page_data = RkiImport.get_all(page)
        except OperationalError:
            flash("No data in the database.")
            page_data = None
        return render_template(
            'rki/test/rki_test.html',
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_rki.route('/date_reported/all/page/<int:page>')
    @app_rki.route('/date_reported/all')
    def url_rki_date_reported_all(page: int = 1):
        page_info = WebPageContent('RKI', "Date Reported", "All")
        try:
            page_data = RkiMeldedatum.get_all(page)
        except OperationalError:
            flash("No date_reported in the database.")
            page_data = None
        return render_template(
            'rki/date_reported/all/rki_date_reported_all.html',
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_rki.route('/date_reported/<int:date_reported_id>/page/<int:page>')
    @app_rki.route('/date_reported/<int:date_reported_id>')
    def url_rki_date_reported_one(date_reported_id: int, page: int = 1):
        page_info = WebPageContent('RKI', "Date Reported", "All")
        try:
            date_reported = RkiMeldedatum.get_by_id(date_reported_id)
            page_data = RkiData.get_by_date_reported(date_reported, page)
        except OperationalError:
            flash("No date_reported in the database.")
            page_data = None
        return render_template(
            'rki/date_reported/one/rki_date_reported_one.html',
            date_reported=date_reported,
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_rki.route('/bundesland/all/page/<int:page>')
    @app_rki.route('/bundesland/all')
    def url_rki_bundesland_all(page: int = 1):
        page_info = WebPageContent('RKI', "Bundesland", "All")
        try:
            page_data = RkiBundesland.get_all(page)
        except OperationalError:
            flash("No date_reported in the database.")
            page_data = None
        return render_template(
            'rki/bundesland/all/rki_bundesland_all.html',
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_rki.route('/bundesland/<int:bundesland_id>/page/<int:page>')
    @app_rki.route('/bundesland/<int:bundesland_id>')
    def url_rki_bundesland_one(bundesland_id: int, page: int = 1):
        page_info = WebPageContent('RKI', "Bundesland", "One")
        try:
            location_group = RkiBundesland.get_by_id(bundesland_id)
            page_data = RkiLandkreis.get_by_location_group(location_group, page)
            page_info = WebPageContent('RKI', "Bundesland", location_group.location_group)
        except OperationalError:
            flash("No date_reported in the database.")
            page_data = None
        return render_template(
            'rki/bundesland/one/rki_bundesland_one.html',
            location_group=location_group,
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_rki.route('/landkreis/<int:landkreis_id>/page/<int:page>')
    @app_rki.route('/landkreis/<int:landkreis_id>')
    def url_rki_landkreis_one(landkreis_id: int, page: int = 1):
        page_info = WebPageContent('RKI', "Landkreis", "One")
        try:
            location = RkiLandkreis.get_by_id(landkreis_id)
            page_data = RkiData.get_by_location(location, page)
            page_info = WebPageContent('RKI', location.location_code + " " + location.location)
        except OperationalError:
            flash("No date_reported in the database.")
            page_data = None
        return render_template(
            'rki/landkreis/one/rki_landkreis_one.html',
            location=location,
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_rki.route('/altersgruppe/all/page/<int:page>')
    @app_rki.route('/altersgruppe/all')
    def url_rki_altersgruppe_all(page: int = 1):
        page_info = WebPageContent('RKI', "Altersgruppe", "All")
        try:
            page_data = RkiAltersgruppe.get_all(page)
        except OperationalError:
            flash("No date_reported in the database.")
            page_data = None
        return render_template(
            'rki/altersgruppe/all/rki_altersgruppe_all.html',
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_rki.route('/delete_last_day')
    def url_rki_delete_last_day():
        app.logger.info("url_rki_delete_last_day [start]")
        flash("url_rki_delete_last_day [start]")
        rki_service.delete_last_day()
        flash("url_rki_delete_last_day [done]")
        app.logger.info("url_rki_delete_last_day [done]")
        return redirect(url_for('rki.url_rki_date_reported_all'))


rki_urls = RkiUrls()

# ------------------------------------------------------------------------
#  Celery TASKS
# ------------------------------------------------------------------------


class RkiTasks:

    @staticmethod
    @celery.task(bind=True)
    def task_rki_import(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            rki_service.import_file()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_rki_import_only)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_rki_full_update_dimension_tables(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            rki_service.full_update_dimension_tables()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_rki_full_update_dimension_tables)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_rki_update_dimension_tables(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            rki_service.update_dimension_tables()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_rki_update_dimension_tables)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_rki_full_update_fact_table(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            rki_service.full_update_fact_table()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_rki_full_update_fact_table)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_rki_update_fact_table(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            rki_service.update_fact_table()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_rki_update_fact_table)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_rki_full_update(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            rki_service.full_update()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_rki_full_update)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_rki_update(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            rki_service.update()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_rki_update)"
        return result


rki_tasks = RkiTasks()

# ------------------------------------------------------------------------
#  URL Routes for Celery TASKS
# ------------------------------------------------------------------------


class RkiTaskUrls:

    @staticmethod
    @app_rki.route('/task/download')
    def url_task_rki_download():
        app.logger.info(" [RKI] url_task_rki_download [start]")
        flash(" [RKI] url_task_rki_download [start]")
        rki_service.download()
        flash(" [RKI] url_task_rki_download [done]")
        app.logger.info(" [RKI] url_task_rki_download [done]")
        return redirect(url_for('rki.url_rki_info'))

    @staticmethod
    @app_rki.route('/task/import')
    def url_task_rki_import():
        app.logger.info(" [RKI] url_task_rki_import [start]")
        rki_tasks.task_rki_import.apply_async()
        flash(" [RKI] task_rki_import started")
        flash(message="long running background task started", category="warning")
        app.logger.warn(" [RKI] task_rki_import [async start]")
        return redirect(url_for('rki.url_rki_info'))

    @staticmethod
    @app_rki.route('/task/update/full/dimension-tables')
    def url_task_rki_full_update_dimension_tables():
        app.logger.info(" [RKI] url_task_rki_full_update_dimensiontables [start]")
        rki_tasks.task_rki_full_update_dimension_tables.apply_async()
        flash(" [RKI] task_rki_full_update_dimension_tables started")
        flash(message="long running background task started", category="warning")
        app.logger.warn(" [RKI] task_rki_full_update_dimensiontables [async start]")
        return redirect(url_for('rki.url_rki_info'))

    @staticmethod
    @app_rki.route('/task/update/dimension-tables')
    def url_task_rki_update_dimension_tables():
        app.logger.info(" [RKI] url_task_rki_update_dimension_tables [start]")
        rki_tasks.task_rki_update_dimension_tables.apply_async()
        flash(" [RKI] task_rki_update_dimension_tables started")
        flash(message="long running background task started", category="warning")
        app.logger.warn(" [RKI] url_task_rki_update_dimension_tables [async start]")
        return redirect(url_for('rki.url_rki_info'))

    @staticmethod
    @app_rki.route('/task/update/full/fact-table')
    def url_task_rki_full_update_fact_table():
        app.logger.info(" [RKI] url_task_rki_full_update_fact_table [start]")
        rki_tasks.task_rki_full_update_fact_table.apply_async()
        flash(" [RKI] task_rki_full_update_fact_table started")
        flash(message=" [RKI] long running background task started", category="warning")
        app.logger.warn(" [RKI] url_task_rki_full_update_fact_table [async start]")
        return redirect(url_for('rki.url_rki_info'))

    @staticmethod
    @app_rki.route('/task/update/fact-table')
    def url_task_rki_update_fact_table():
        app.logger.info(" [RKI] url_task_rki_update_fact_table [start]")
        rki_tasks.task_rki_update_fact_table.apply_async()
        flash(" [RKI] task_rki_update_fact_table started")
        flash(message=" [RKI] long running background task started", category="warning")
        app.logger.warn(" [RKI] url_task_rki_update_fact_table [async start]")
        return redirect(url_for('rki.url_rki_info'))

    @staticmethod
    @app_rki.route('/task/full/update')
    def url_task_rki_full_update():
        app.logger.info(" [RKI] url_task_rki_full_update [start]")
        flash(" [RKI] url_task_rki_download [start]")
        rki_service.download()
        flash(" [RKI] url_task_rki_download [done]")
        rki_tasks.task_rki_full_update.apply_async()
        flash(" [RKI] task_rki_full_update started")
        flash(message=" [RKI] long running background task started", category="warning")
        app.logger.warn(" [RKI] task_rki_full_update [async start]")
        app.logger.info(" [RKI] url_task_rki_full_update [done]")
        return redirect(url_for('rki.url_rki_info'))

    @staticmethod
    @app_rki.route('/task/update')
    def url_task_rki_update():
        app.logger.info(" [RKI] url_task_rki_update [start]")
        flash(" [RKI] url_task_rki_download [start]")
        rki_service.download()
        flash(" [RKI] url_task_rki_download [done]")
        rki_tasks.task_rki_update.apply_async()
        flash(" [RKI] task_rki_update started")
        flash(message=" [RKI] long running background task started", category="warning")
        app.logger.warn(" [RKI] task_rki_update [async start]")
        app.logger.info(" [RKI] url_task_rki_update [done]")
        return redirect(url_for('rki.url_rki_info'))


rki_task_urls = RkiTaskUrls()
rki_test_service = RkiTestService(db, rki_service)


# ---------------------------------------------------------------------------------------------------------------
#  Url Routes Frontend TESTS TESTS
# ---------------------------------------------------------------------------------------------------------------


class RkiTestUrls:

    @staticmethod
    @app_rki.route('/test/full_update_dimension_tables')
    @login_required
    def url_rki_test_full_update_dimension_tables():
        app.logger.info(" [RKI] url_rki_test_full_update_dimension_tables - START")
        flash(" [RKI] url_rki_test_full_update_dimension_tables - START")
        return redirect(url_for('rki.url_rki_info'))

    @staticmethod
    @app_rki.route('/test/update_dimension_tables')
    @login_required
    def url_rki_test_update_dimension_tables():
        app.logger.info(" [RKI] url_rki_test_update_dimension_tables - START")
        flash(" [RKI] url_rki_test_update_dimension_tables - START")
        return redirect(url_for('rki.url_rki_info'))

    @staticmethod
    @app_rki.route('/test/full_update_fact_table')
    @login_required
    def url_rki_test_full_update_fact_table():
        app.logger.info(" [RKI] url_rki_test_full_update_fact_table - START")
        flash(" [RKI] url_rki_test_full_update_fact_table - START")
        return redirect(url_for('rki.url_rki_info'))

    @staticmethod
    @app_rki.route('/test/update_fact_table')
    @login_required
    def url_rki_test_update_fact_table():
        app.logger.info(" [RKI] url_rki_test_update_fact_table - START")
        flash(" [RKI] url_rki_test_update_fact_table - START")
        return redirect(url_for('rki.url_rki_info'))

    @staticmethod
    @app_rki.route('/test/rki_import/countries')
    @login_required
    def url_rki_test_rki_import_countries():
        app.logger.info(" [RKI] url_rki_test_rki_import_countries - START")
        flash(" [RKI] url_rki_test_rki_import_countries - START")
        i = 0
        for c in RkiImport.countries():
            i += 1
            line = " | " + str(i) + " | " + c.countries.iso_code + " | " + c.countries.location + " | " + c.countries.continent + " | "
            app.logger.info(line)
        app.logger.info(" [RKI] url_rki_test_rki_import_countries - DONE")
        flash(" [RKI] url_rki_test_rki_import_countries - DONE")
        return redirect(url_for('rki.url_rki_info'))

    @staticmethod
    @app_rki.route('/test/rki_import/get_new_dates_reported_as_array')
    @login_required
    def url_rki_test_rki_import_get_new_dates_reported_as_array():
        app.logger.info(" [RKI] url_rki_test_rki_import_get_new_dates_reported_as_array - START")
        flash(" [RKI] url_rki_test_rki_import_get_new_dates_reported_as_array - START")
        i = 0
        for date_reported in RkiImport.get_new_dates_reported_as_array():
            i += 1
            line = " | " + str(i) + " | " + date_reported + " | "
            app.logger.info(line)
        app.logger.info(" [RKI] url_rki_test_rki_import_get_new_dates_reported_as_array - DONE")
        flash(" [RKI] url_rki_test_rki_import_get_new_dates_reported_as_array - DONE")
        return redirect(url_for('rki.url_rki_info'))

    @staticmethod
    @app_rki.route('/test/rki_data/get_datum_of_all_data')
    @login_required
    def url_rki_test_rki_data_get_datum_of_all_data():
        app.logger.info(" [RKI] url_rki_test_rki_data_get_datum_of_all_data - START")
        flash(" [RKI] url_rki_test_rki_data_get_datum_of_all_data - START")
        for datum in RkiData.get_datum_of_all_data():
            app.logger.info(str(datum))
        app.logger.info(" [RKI] url_rki_test_rki_data_get_datum_of_all_data - DONE")
        flash(" [RKI] url_rki_test_rki_data_get_datum_of_all_data - DONE")
        return redirect(url_for('rki.url_rki_info'))

    @staticmethod
    @app_rki.route('/test/rki_import/get_datum_of_all_import')
    @login_required
    def url_rki_test_rki_import_get_datum_of_all_import():
        app.logger.info(" [RKI] url_rki_test_rki_import_get_datum_of_all_import - START")
        flash(" [RKI] url_rki_test_rki_import_get_datum_of_all_import - START")
        for datum in RkiImport.get_datum_of_all_import():
            app.logger.info(str(datum))
        app.logger.info(" [RKI] url_rki_test_rki_import_get_datum_of_all_import - DONE")
        flash(" [RKI] url_rki_test_rki_import_get_datum_of_all_import - DONE")
        return redirect(url_for('rki.url_rki_info'))

    @staticmethod
    @app_rki.route('/test/rki_service/service_update/rki_import_get_new_dates_as_array')
    @login_required
    def url_rki_test_rki_service_service_update_rki_import_get_new_dates_as_array():
        app.logger.info(" [RKI] url_rki_test_rki_service_service_update_rki_import_get_new_dates_as_array - START")
        flash(" [RKI] url_rki_test_rki_service_service_update_rki_import_get_new_dates_as_array - START")
        for datum in rki_service.service_update.rki_import_get_new_dates_as_array():
            app.logger.info(str(datum))
        app.logger.info(" [RKI] url_rki_test_rki_service_service_update_rki_import_get_new_dates_as_array - DONE")
        flash(" [RKI] url_rki_test_rki_service_service_update_rki_import_get_new_dates_as_array - DONE")
        return redirect(url_for('rki.url_rki_info'))

    @staticmethod
    @app_rki.route('/test/rki_test_service/full_update_dimension_tables')
    @login_required
    def url_rki_test_rki_test_service_full_update_dimension_tables():
        app.logger.info(" [RKI] url_rki_test_rki_test_service_full_update_dimension_tables - START: rki_test_service.full_update_dimension_tables()")
        flash(" [RKI] url_rki_test_rki_test_service_full_update_dimension_tables - START: rki_test_service.full_update_dimension_tables()")
        rki_test_service.full_update_dimension_tables()
        app.logger.info(" [RKI] url_rki_test_rki_test_service_full_update_dimension_tables - DONE: rki_test_service.full_update_dimension_tables()")
        flash(" [RKI] url_rki_test_rki_test_service_full_update_dimension_tables - DONE: rki_test_service.full_update_dimension_tables()")
        return redirect(url_for('rki.url_rki_info'))


rki_test_urls = RkiTestUrls()
