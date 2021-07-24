from flask import render_template, redirect, url_for, flash, Blueprint
from celery import states
from celery.utils.log import get_task_logger
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required

from app_config.database import app, admin, db, celery
from app_web.web_dispachter_matrix_service import ecdc_service
from data_ecdc.ecdc_service_test import EcdcTestService

from data_ecdc.ecdc_model_import import EcdcImport
from data_ecdc.ecdc_model_flat import EcdcFlat
from data_ecdc.ecdc_model import EcdcDateReported
from data_ecdc.ecdc_model_location_group import EcdcContinent
from data_ecdc.ecdc_model_location import EcdcCountry
from data_ecdc.ecdc_model_data import EcdcData
from app_web.web_model_transient import WebPageContent


app_ecdc = Blueprint('ecdc', __name__, template_folder='templates', url_prefix='/ecdc')

admin.add_view(ModelView(EcdcImport, db.session, category="ECDC"))
admin.add_view(ModelView(EcdcFlat, db.session, category="ECDC"))
admin.add_view(ModelView(EcdcDateReported, db.session, category="ECDC"))
admin.add_view(ModelView(EcdcContinent, db.session, category="ECDC"))
admin.add_view(ModelView(EcdcCountry, db.session, category="ECDC"))
admin.add_view(ModelView(EcdcData, db.session, category="ECDC"))


# ---------------------------------------------------------------------------------------------------------------
#  Url Routes Frontend
# ---------------------------------------------------------------------------------------------------------------


class EcdcUrls:

    @staticmethod
    @app_ecdc.route('')
    @app_ecdc.route('/')
    def url_ecdc_root():
        return redirect(url_for('ecdc.url_ecdc_info'))

    @staticmethod
    @app_ecdc.route('/info')
    def url_ecdc_info():
        page_info = WebPageContent('ECDC', "Info")
        return render_template(
            'ecdc/ecdc_info.html',
            title='Europe',
            page_info=page_info)

    @staticmethod
    @app_ecdc.route('/imported/page/<int:page>')
    @app_ecdc.route('/imported')
    def url_ecdc_imported(page=1):
        page_info = WebPageContent('ECDC', "Last Import")
        page_data = EcdcImport.get_all(page)
        return render_template(
            'ecdc/imported/ecdc_imported.html',
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_ecdc.route('/flat/page/<int:page>')
    @app_ecdc.route('/flat')
    def url_ecdc_flat(page=1):
        page_info = WebPageContent('ECDC', "flat")
        page_data = EcdcFlat.get_all(page)
        return render_template(
            'ecdc/flat/ecdc_flat.html',
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_ecdc.route('/date_reported/all/page/<int:page>')
    @app_ecdc.route('/date_reported/all')
    def url_ecdc_date_reported_all(page=1):
        page_info = WebPageContent('ECDC', "date_reported")
        page_data = EcdcDateReported.get_all(page)
        return render_template(
            'ecdc/date_reported/all/ecdc_date_reported_all.html',
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_ecdc.route('/date_reported/<int:date_reported_id>/page/<int:page>')
    @app_ecdc.route('/date_reported/<int:date_reported_id>')
    def url_ecdc_date_reported_one(date_reported_id, page=1):
        page_info = WebPageContent('ECDC', "date_reported")
        ecdc_date_reported = EcdcDateReported.get_by_id(date_reported_id)
        page_data = EcdcData.get_by_date_reported_order_by_notification_rate(ecdc_date_reported, page)
        return render_template(
            'ecdc/date_reported/one/ecdc_date_reported_one.html',
            ecdc_date_reported=ecdc_date_reported,
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_ecdc.route('/date_reported/notification_rate/<int:date_reported_id>/page/<int:page>')
    @app_ecdc.route('/date_reported/notification_rate/<int:date_reported_id>')
    def url_ecdc_date_reported_one_notification_rate(date_reported_id, page=1):
        page_info = WebPageContent('ECDC', "date_reported")
        ecdc_date_reported = EcdcDateReported.get_by_id(date_reported_id)
        page_data = EcdcData.get_by_date_reported_order_by_notification_rate(ecdc_date_reported, page)
        return render_template(
            'ecdc/date_reported/notification/ecdc_date_reported_one_notification_rate.html',
            ecdc_date_reported=ecdc_date_reported,
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_ecdc.route('/date_reported/deaths_weekly/<int:date_reported_id>/page/<int:page>')
    @app_ecdc.route('/date_reported/deaths_weekly/<int:date_reported_id>')
    def url_ecdc_date_reported_one_deaths_weekly(date_reported_id, page=1):
        page_info = WebPageContent('ECDC', "date_reported")
        ecdc_date_reported = EcdcDateReported.get_by_id(date_reported_id)
        page_data = EcdcData.get_by_date_reported_order_by_deaths(ecdc_date_reported, page)
        return render_template(
            'ecdc/date_reported/deaths/ecdc_date_reported_one_deaths_weekly.html',
            ecdc_date_reported=ecdc_date_reported,
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_ecdc.route('/date_reported/cases_weekly/<int:date_reported_id>/page/<int:page>')
    @app_ecdc.route('/date_reported/cases_weekly/<int:date_reported_id>')
    def url_ecdc_date_reported_one_cases_weekly(date_reported_id, page=1):
        page_info = WebPageContent('ECDC', "date_reported")
        ecdc_date_reported = EcdcDateReported.get_by_id(date_reported_id)
        page_data = EcdcData.get_by_date_reported_order_by_cases(ecdc_date_reported, page)
        return render_template(
            'ecdc/date_reported/cases/ecdc_date_reported_one_cases_weekly.html',
            ecdc_date_reported=ecdc_date_reported,
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_ecdc.route('/continent/all/page/<int:page>')
    @app_ecdc.route('/continent/all')
    def url_ecdc_continent_all(page=1):
        page_info = WebPageContent('ECDC', "continent")
        page_data = EcdcContinent.get_all(page)
        return render_template(
            'ecdc/continent/all/ecdc_continent_all.html',
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_ecdc.route('/continent/<int:continent_id>/page/<int:page>')
    @app_ecdc.route('/continent/<int:continent_id>')
    def url_ecdc_continent_one(continent_id: int, page=1):
        page_info = WebPageContent('ECDC', "continent")
        ecdc_continent = EcdcContinent.get_by_id(continent_id)
        page_data = EcdcCountry.get_by_location_group(ecdc_continent, page)
        return render_template(
            'ecdc/continent/one/ecdc_continent_one.html',
            ecdc_continent=ecdc_continent,
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_ecdc.route('/country/all/page/<int:page>')
    @app_ecdc.route('/country/all')
    def url_ecdc_country_all(page=1):
        page_info = WebPageContent('ECDC', "country")
        page_data = EcdcCountry.get_all(page)
        return render_template(
            'ecdc/country/all/ecdc_country_all.html',
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_ecdc.route('/country/<int:country_id>/page/<int:page>')
    @app_ecdc.route('/country/<int:country_id>')
    def url_ecdc_country_one(country_id, page=1):
        page_info = WebPageContent('ECDC', "country")
        ecdc_country = EcdcCountry.get_by_id(country_id)
        page_data = EcdcData.get_by_location(ecdc_country, page)
        return render_template(
            'ecdc/country/one/ecdc_country_one.html',
            ecdc_country=ecdc_country,
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_ecdc.route('/country/germany/page/<int:page>')
    @app_ecdc.route('/country/germany')
    def url_ecdc_country_germany(page=1):
        page_info = WebPageContent('ECDC', "country: Germany")
        ecdc_country = EcdcCountry.find_germany()
        if ecdc_country is None:
            flash('country: Germany not found in Database', category='error')
            return redirect(url_for('ecdc.url_ecdc_info'))
        page_data = EcdcData.get_by_location(ecdc_country, page)
        return render_template(
            'ecdc/country/germany/ecdc_country_germany.html',
            ecdc_country=ecdc_country,
            page_data=page_data,
            page_info=page_info)


ecdc_urls = EcdcUrls()

# ----------------------------------------------------------------------------------------------------------------
#  Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


class EcdcTasks:

    @staticmethod
    @celery.task(bind=True)
    def task_ecdc_import(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" Received: task_ecdc_import [OK] ")
            app.logger.info("------------------------------------------------------------")
            ecdc_service.import_file()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_ecdc_import)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_ecdc_full_update_dimension_tables(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" Received: task_ecdc_full_update_dimension_tables [OK] ")
            app.logger.info("------------------------------------------------------------")
            ecdc_service.full_update_dimension_tables()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_ecdc_full_update_dimension_tables)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_ecdc_update_dimension_tables(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" Received: task_ecdc_update_dimension_tables [OK] ")
            app.logger.info("------------------------------------------------------------")
            ecdc_service.update_dimension_tables()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_ecdc_update_dimension_tables)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_ecdc_full_update_fact_table(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" Received: task_ecdc_full_update_fact_table [OK] ")
            app.logger.info("------------------------------------------------------------")
            ecdc_service.full_update_fact_table()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_ecdc_full_update_fact_table)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_ecdc_update_fact_table(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" Received: task_ecdc_update_fact_table [OK] ")
            app.logger.info("------------------------------------------------------------")
            ecdc_service.update_fact_table()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_ecdc_update_fact_table)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_ecdc_full_update_fact_table(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" Received: task_ecdc_full_update_fact_table [OK] ")
            app.logger.info("------------------------------------------------------------")
            ecdc_service.full_update_fact_table()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_ecdc_full_update_fact_table)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_ecdc_full_update(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" Received: task_ecdc_full_update [OK] ")
            app.logger.info("------------------------------------------------------------")
            ecdc_service.full_update()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_ecdc_full_update)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_ecdc_update(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" Received: task_ecdc_update [OK] ")
            app.logger.info("------------------------------------------------------------")
            ecdc_service.update()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_ecdc_update)"
        return result


ecdc_tasks = EcdcTasks()

# ----------------------------------------------------------------------------------------------------------------
#  URL Routes for Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


class EcdcTaskUrls:

    @staticmethod
    @app_ecdc.route('/task/download')
    def url_ecdc_task_download():
        app.logger.info("url_ecdc_task_download [start]")
        ecdc_service.download()
        flash("ecdc_service.download done")
        app.logger.info("url_ecdc_task_download [done]")
        return redirect(url_for('ecdc.url_ecdc_info'))

    @staticmethod
    @app_ecdc.route('/task/import')
    def url_ecdc_task_import():
        app.logger.info("url_ecdc_task_import [start]")
        ecdc_tasks.task_ecdc_import.apply_async()
        flash("task_ecdc_import started")
        flash(message="long running background task started", category="warning")
        app.logger.info("url_ecdc_task_import [done]")
        return redirect(url_for('ecdc.url_ecdc_info'))

    @staticmethod
    @app_ecdc.route('/task/update/dimension-tables')
    def url_ecdc_task_update_dimension_tables():
        app.logger.info("url_ecdc_task_update_dimension_tables [start]")
        ecdc_tasks.task_ecdc_update_dimension_tables.apply_async()
        flash("task_ecdc_update_dimension_tables started")
        flash(message="long running background task started", category="warning")
        app.logger.info("url_ecdc_task_update_dimension_tables [done]")
        return redirect(url_for('ecdc.url_ecdc_info'))

    @staticmethod
    @app_ecdc.route('/task/full/update/dimension-tables')
    def url_ecdc_task_full_update_dimension_tables():
        app.logger.info("url_ecdc_task_full_update_dimension_tables [start]")
        ecdc_tasks.task_ecdc_full_update_dimension_tables.apply_async()
        flash("url_ecdc_task_full_update_dimensiontables started")
        flash(message="long running background task started", category="warning")
        app.logger.info("url_ecdc_task_full_update_dimension_tables [done]")
        return redirect(url_for('ecdc.url_ecdc_info'))

    @staticmethod
    @app_ecdc.route('/task/full/update/fact-table')
    def url_task_ecdc_full_update_fact_table():
        app.logger.info("url_task_ecdc_full_update_fact_table [start]")
        ecdc_tasks.task_ecdc_full_update_fact_table.apply_async()
        flash("task_ecdc_full_update_fact_table started")
        flash(message="long running background task started", category="warning")
        app.logger.info("url_task_ecdc_full_update_fact_table [done]")
        return redirect(url_for('ecdc.url_ecdc_info'))

    @staticmethod
    @app_ecdc.route('/task/update/fact-table')
    def url_task_ecdc_update_fact_table():
        app.logger.info("url_task_ecdc_update_fact_table [start]")
        ecdc_tasks.task_ecdc_update_fact_table.apply_async()
        flash("task_ecdc_update_fact_table started")
        flash(message="long running background task started", category="warning")
        app.logger.info("url_task_ecdc_update_fact_table [done]")
        return redirect(url_for('ecdc.url_ecdc_info'))

    @staticmethod
    @app_ecdc.route('/task/full/update')
    def url_task_ecdc_full_update():
        app.logger.info("url_task_ecdc_full_update [start]")
        ecdc_service.download()
        flash("ecdc_service.download done")
        ecdc_tasks.task_ecdc_full_update.apply_async()
        flash("task_ecdc_full_update started")
        flash(message="long running background task started", category="warning")
        app.logger.info("url_task_ecdc_full_update [done]")
        return redirect(url_for('ecdc.url_ecdc_info'))

    @staticmethod
    @app_ecdc.route('/task/update')
    def url_task_ecdc_update():
        app.logger.info("url_task_ecdc_update [start]")
        ecdc_service.download()
        flash("ecdc_service.download done")
        ecdc_tasks.task_ecdc_update.apply_async()
        flash("task_ecdc_update started")
        flash(message="long running background task started", category="warning")
        app.logger.info("url_task_ecdc_update [done]")
        return redirect(url_for('ecdc.url_ecdc_info'))


ecdc_task_urls = EcdcTaskUrls()

ecdc_test_service = EcdcTestService(db, ecdc_service)


# ---------------------------------------------------------------------------------------------------------------
#  Url Routes Frontend  TEST
# ---------------------------------------------------------------------------------------------------------------

class EcdcTestUrls:

    @staticmethod
    @app_ecdc.route('/test/ecdc_import/countries')
    @login_required
    def url_ecdc_test_ecdc_import_countries():
        flash("url_ecdc_test_ecdc_import_countries - START: EcdcImport.countries()")
        app.logger.info("url_ecdc_test_ecdc_import_countries - START: EcdcImport.countries()")
        i = 0
        for c in EcdcImport.countries():
            i += 1
            line = " | " + str(i) + " | " + c.countries.country_code + " | " + c.countries.country + " | " + c.countries.ecdc_region + " | "
            app.logger.info(line)
        flash("url_ecdc_test_ecdc_import_countries - DONE: EcdcImport.countries()")
        return redirect(url_for('ecdc_test.url_ecdc_test_tests'))

    @staticmethod
    @app_ecdc.route('/test/ecdc_import/get_new_dates_as_array')
    @login_required
    def url_ecdc_test_ecdc_import_get_new_dates_as_array():
        app.logger.info("url_ecdc_mytest - DONE: EcdcImport.countries()")
        flash("url_ecdc_mytest - START: EcdcImport.get_new_dates_as_array()")
        app.logger.info("url_ecdc_mytest - START: EcdcImport.get_new_dates_as_array()")
        app.logger.info("EcdcImport.get_new_dates_as_array():")
        i = 0
        for date_reported in EcdcImport.get_new_dates_as_array():
            i += 1
            line = " | " + str(i) + " | " + date_reported + " | "
            app.logger.info(line)
        flash("url_ecdc_mytest - DONE: EcdcImport.get_new_dates_as_array()")
        app.logger.info("url_ecdc_mytest - DONE: EcdcImport.get_new_dates_as_array()")
        return redirect(url_for('ecdc_test.url_ecdc_test_tests'))

    @staticmethod
    @app_ecdc.route('/test/ecdc_data/get_datum_of_all_ecdc_data')
    @login_required
    def url_ecdc_test_ecdc_data_get_datum_of_all_ecdc_data():
        app.logger.info("url_ecdc_test_ecdc_data_get_datum_of_all_ecdc_data - DONE: EcdcData.get_datum_of_all_ecdc_data()")
        flash("url_ecdc_test_ecdc_data_get_datum_of_all_ecdc_data - START: EcdcData.get_datum_of_all_ecdc_data()")
        for datum in EcdcImport.get_datum_of_all_data():
            app.logger.info(str(datum))
        flash("url_ecdc_test_ecdc_data_get_datum_of_all_ecdc_data - DONE: EcdcData.get_datum_of_all_ecdc_data()")
        app.logger.info("url_ecdc_test_ecdc_data_get_datum_of_all_ecdc_data - DONE: EcdcData.get_datum_of_all_ecdc_data()")
        return redirect(url_for('ecdc_test.url_ecdc_test_tests'))

    @staticmethod
    @app_ecdc.route('/test/ecdc_data/get_datum_of_all_ecdc_import')
    @login_required
    def url_ecdc_test_ecdc_data_get_datum_of_all_ecdc_import():
        app.logger.info("url_ecdc_test_ecdc_data_get_datum_of_all_ecdc_import - START: EcdcImport.get_datum_of_all_ecdc_import()")
        flash("url_ecdc_test_ecdc_data_get_datum_of_all_ecdc_import - START: EcdcImport.get_datum_of_all_ecdc_import()")
        for datum in EcdcImport.get_datum_of_all_ecdc_import():
            app.logger.info(str(datum))
        flash("url_ecdc_test_ecdc_data_get_datum_of_all_ecdc_import - DONE: EcdcImport.get_datum_of_all_ecdc_import()")
        app.logger.info("url_ecdc_test_ecdc_data_get_datum_of_all_ecdc_import - DONE: EcdcImport.get_datum_of_all_ecdc_import()")
        return redirect(url_for('ecdc_test.url_ecdc_test_tests'))

    @staticmethod
    @app_ecdc.route('/test/ecdc_service/service_update/ecdc_import_get_new_dates_as_array')
    @login_required
    def url_ecdc_test_ecdc_service_ecdc_import_get_new_dates_as_array():
        app.logger.info("url_ecdc_test_ecdc_import_get_new_dates_as_array - START: EcdcService.ecdc_import_get_new_dates_as_array()")
        flash("url_ecdc_test_ecdc_import_get_new_dates_as_array - START: EcdcService.ecdc_import_get_new_dates_as_array()")
        for datum in ecdc_service.service_update.ecdc_import_get_new_dates_as_array():
            app.logger.info(str(datum))
        flash("url_ecdc_test_ecdc_import_get_new_dates_as_array - DONE: EcdcService.ecdc_import_get_new_dates_as_array()")
        app.logger.info("url_ecdc_test_ecdc_import_get_new_dates_as_array - DONE: EcdcService.ecdc_import_get_new_dates_as_array()")
        return redirect(url_for('ecdc_test.url_ecdc_test_tests'))


ecdc_test_urls = EcdcTestUrls()


