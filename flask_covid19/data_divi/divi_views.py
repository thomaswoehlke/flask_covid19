from flask import render_template, redirect, url_for, flash, Blueprint
from sqlalchemy.exc import OperationalError
from celery import states
from celery.utils.log import get_task_logger
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required

from app_config.database import app, admin, db, celery

from app_web.web_dispachter_matrix_service import divi_service
from app_web.web_model_transient import WebPageContent

from data_divi.divi_model import DiviRegion, DiviDateReported, DiviCountry, DiviData
from data_divi.divi_model_import import DiviImport


app_divi = Blueprint('divi', __name__, template_folder='templates', url_prefix='/divi')

admin.add_view(ModelView(DiviImport, db.session, category="DIVI"))
admin.add_view(ModelView(DiviDateReported, db.session, category="DIVI"))
admin.add_view(ModelView(DiviRegion, db.session, category="DIVI"))
admin.add_view(ModelView(DiviCountry, db.session, category="DIVI"))
admin.add_view(ModelView(DiviData, db.session, category="DIVI"))


# ---------------------------------------------------------------------------------------------------------------
#  Url Routes Frontend
# ---------------------------------------------------------------------------------------------------------------

class DiviUrls:

    @staticmethod
    @app_divi.route('')
    @app_divi.route('/')
    def url_divi_root():
        return redirect(url_for('divi.url_divi_info'))

    @staticmethod
    @app_divi.route('/info')
    def url_divi_info():
        page_info = WebPageContent('divi', "Info")
        return render_template(
            'divi/divi_info.html',
            page_info=page_info)

    @staticmethod
    @app_divi.route('/tasks')
    @login_required
    def url_divi_tasks():
        page_info = WebPageContent('divi', "Tasks")
        return render_template(
            'divi/divi_tasks.html',
            page_info=page_info)

    @staticmethod
    @app_divi.route('/imported/page/<int:page>')
    @app_divi.route('/imported')
    @login_required
    def url_divi_imported(page=1):
        page_info = WebPageContent('divi', "Last Import")
        try:
            page_data = DiviImport.get_all(page)
        except OperationalError:
            flash("No data in the database.")
            page_data = None
        return render_template(
            'divi/divi_imported.html',
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_divi.route('/date_reported/all/page/<int:page>')
    @app_divi.route('/date_reported/all')
    def url_divi_date_reported_all(page: int = 1):
        page_info = WebPageContent('divi', "Date Reported", "All")
        try:
            page_data = DiviDateReported.get_all(page)
        except OperationalError:
            flash("No regions in the database.")
            page_data = None
        return render_template(
            'divi/date_reported/divi_date_reported_all.html',
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_divi.route('/date_reported/<int:date_reported_id>/page/<int:page>')
    @app_divi.route('/date_reported/<int:date_reported_id>')
    def url_divi_date_reported(date_reported_id: int, page: int = 1):
        date_reported = DiviDateReported.get_by_id(date_reported_id)
        page_info = WebPageContent(
            "Date Reported: " + date_reported.date_reported,
            'divi',
            "data of all reported countries for divi date reported " + date_reported.date_reported + " "
        )
        try:
            page_data = DiviData.get_data_for_day(date_reported, page)
        except OperationalError:
            flash("No data in the database.")
            page_data = None
        return render_template(
            'divi/date_reported/divi_date_reported_one.html',
            divi_date_reported=date_reported,
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_divi.route('/date_reported/<int:date_reported_id>/cases_new/page/<int:page>')
    @app_divi.route('/date_reported/<int:date_reported_id>/cases_new')
    def url_divi_date_reported_cases_new(date_reported_id: int, page: int = 1):
        date_reported = DiviDateReported.get_by_id(date_reported_id)
        page_info = WebPageContent(
            "Date Reported: " + date_reported.date_reported,
            'divi',
            "data of all reported countries for divi date reported " + date_reported.date_reported + " "
        )
        try:
            page_data = DiviData.get_data_for_day_order_by_cases_new(date_reported, page)
        except OperationalError:
            flash("No data in the database.")
            page_data = None
        return render_template(
            'divi/date_reported/divi_date_reported_one_cases_new.html',
            divi_date_reported=date_reported,
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_divi.route('/date_reported/<int:date_reported_id>/cases_cumulative/page/<int:page>')
    @app_divi.route('/date_reported/<int:date_reported_id>/cases_cumulative')
    def url_divi_date_reported_cases_cumulative(date_reported_id: int, page: int = 1):
        date_reported = DiviDateReported.get_by_id(date_reported_id)
        page_info = WebPageContent(
            "Date Reported: " + date_reported.date_reported,
            'divi',
            "data of all reported countries for divi date reported " + date_reported.date_reported + " "
        )
        try:
            page_data = DiviData.get_data_for_day_order_by_cases_cumulative(date_reported, page)
        except OperationalError:
            flash("No data in the database.")
            page_data = None
        return render_template(
            'divi/date_reported/divi_date_reported_one_cases_cumulative.html',
            divi_date_reported=date_reported,
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_divi.route('/date_reported/<int:date_reported_id>/deaths_new/page/<int:page>')
    @app_divi.route('/date_reported/<int:date_reported_id>/deaths_new')
    def url_divi_date_reported_deaths_new(date_reported_id: int, page: int = 1):
        date_reported = DiviDateReported.get_by_id(date_reported_id)
        page_info = WebPageContent(
            "Date Reported: " + date_reported.date_reported,
            'divi',
            "data of all reported countries for divi date reported " + date_reported.date_reported + " "
        )
        try:
            page_data = DiviData.get_data_for_day_order_by_deaths_new(date_reported, page)
        except OperationalError:
            flash("No data in the database.")
            page_data = None
        return render_template(
            'divi/date_reported/divi_date_reported_one_deaths_new.html',
            divi_date_reported=date_reported,
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_divi.route('/date_reported/<int:date_reported_id>/deaths_cumulative/page/<int:page>')
    @app_divi.route('/date_reported/<int:date_reported_id>/deaths_cumulative')
    def url_divi_date_reported_deaths_cumulative(date_reported_id: int, page: int = 1):
        date_reported = DiviDateReported.get_by_id(date_reported_id)
        page_info = WebPageContent(
            "Date Reported: " + date_reported.date_reported,
            'divi',
            "data of all reported countries for divi date reported " + date_reported.date_reported + " "
        )
        try:
            page_data = DiviData.get_data_for_day_order_by_deaths_cumulative(date_reported, page)
        except OperationalError:
            flash("No data in the database.")
            page_data = None
        return render_template(
            'divi/date_reported/divi_date_reported_one_deaths_cumulative.html',
            divi_date_reported=date_reported,
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_divi.route('/region/all/page/<int:page>')
    @app_divi.route('/region/all')
    def url_divi_region_all(page: int = 1):
        page_info = WebPageContent('divi', "Region", "All")
        try:
            page_data = DiviRegion.get_all(page)
        except OperationalError:
            flash("No regions in the database.")
            page_data = None
        return render_template(
            'divi/region/divi_region_all.html',
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_divi.route('/region/<int:region_id>/page/<int:page>')
    @app_divi.route('/region/<int:region_id>')
    def url_divi_region(region_id: int, page: int = 1):
        divi_region = None
        page_info = WebPageContent("Countries", "divi Region")
        try:
            divi_region = DiviRegion.get_by_id(region_id)
            page_data = DiviCountry.get_divi_countries_for_region(divi_region, page)
            page_info.title = divi_region.region
            page_info.subtitle = "divi Region"
            page_info.subtitle_info = "Countries of divi Region " + divi_region.region
        except OperationalError:
            flash("No countries of that region in the database.")
            page_data = None
        return render_template(
            'divi/region/divi_region_one.html',
            divi_region=divi_region,
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_divi.route('/country/all/page/<int:page>')
    @app_divi.route('/country/all')
    def url_divi_country_all(page: int = 1):
        page_info = WebPageContent('divi', "Countries", "All")
        try:
            page_data = DiviCountry.get_all(page)
        except OperationalError:
            flash("No regions in the database.")
            page_data = None
        return render_template(
            'divi/country/divi_country_all.html',
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_divi.route('/country/<int:country_id>/page/<int:page>')
    @app_divi.route('/country/<int:country_id>')
    def url_divi_country(country_id: int, page: int = 1):
        divi_country = DiviCountry.get_by_id(country_id)
        page_data = DiviData.get_data_for_country(divi_country, page)
        page_info = WebPageContent(divi_country.country,
               "Country " + divi_country.country_code,
               "Data per Day in Country " + divi_country.country +" of divi Region " + divi_country.region.region)
        return render_template(
            'divi/country/divi_country_one.html',
            divi_country=divi_country,
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_divi.route('/country/<int:country_id>/cases_new/page/<int:page>')
    @app_divi.route('/country/<int:country_id>/cases_new')
    def url_divi_country_cases_new(country_id: int, page: int = 1):
        divi_country = DiviCountry.get_by_id(country_id)
        page_data = DiviData.get_data_for_country_order_by_cases_new(divi_country, page)
        page_info = WebPageContent(divi_country.country,
               "Country " + divi_country.country_code,
               "Data per Day in Country " + divi_country.country +" of divi Region " + divi_country.region.region)
        return render_template(
            'divi/country/divi_country_one_cases_new.html',
            divi_country=divi_country,
            page_data=page_data,
            page_info=page_info)


    @app_divi.route('/country/<int:country_id>/cases_cumulative/page/<int:page>')
    @app_divi.route('/country/<int:country_id>/cases_cumulative')
    def url_divi_country_cases_cumulative(country_id: int, page: int = 1):
        divi_country = DiviCountry.get_by_id(country_id)
        page_data = DiviData.get_data_for_country_order_by_cases_cumulative(divi_country, page)
        page_info = WebPageContent(divi_country.country,
               "Country " + divi_country.country_code,
               "Data per Day in Country " + divi_country.country +" of divi Region " + divi_country.region.region)
        return render_template(
            'divi/country/divi_country_one_cases_cumulative.html',
            divi_country=divi_country,
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_divi.route('/country/<int:country_id>/deaths_new/page/<int:page>')
    @app_divi.route('/country/<int:country_id>/deaths_new')
    def url_divi_country_deaths_new(country_id: int, page: int = 1):
        divi_country = DiviCountry.get_by_id(country_id)
        page_data = DiviData.get_data_for_country_order_by_deaths_new(divi_country, page)
        page_info = WebPageContent(divi_country.country,
               "Country " + divi_country.country_code,
               "Data per Day in Country " + divi_country.country +" of divi Region " + divi_country.region.region)
        return render_template(
            'divi/country/divi_country_one_deaths_new.html',
            divi_country=divi_country,
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_divi.route('/country/<int:country_id>/deaths_cumulative/page/<int:page>')
    @app_divi.route('/country/<int:country_id>/deaths_cumulative')
    def url_divi_country_deaths_cumulative(country_id: int, page: int = 1):
        divi_country = DiviCountry.get_by_id(country_id)
        page_data = DiviData.get_data_for_country_order_by_deaths_cumulative(divi_country, page)
        page_info = WebPageContent(divi_country.country,
               "Country " + divi_country.country_code,
               "Data per Day in Country " + divi_country.country +" of divi Region " + divi_country.region.region)
        return render_template(
            'divi/country/divi_country_one_deaths_cumulative.html',
            divi_country=divi_country,
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_divi.route('/germany/page/<int:page>')
    @app_divi.route('/germany')
    def url_divi_germany(page: int = 1):
        page_info = WebPageContent('divi', "Germany")
        divi_country_germany = DiviCountry.get_germany()
        if divi_country_germany is None:
            flash('country: Germany not found in Database', category='error')
            return redirect(url_for('divi.url_divi_tasks'))
        page_data = DiviData.get_data_for_country(divi_country_germany, page)
        return render_template(
            'divi/country/divi_country_germany.html',
            divi_country=divi_country_germany,
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_divi.route('/mytest')
    def url_divi_mytest():
        flash("url_divi_mytest - START: DiviImport.countries()")
        app.logger.info("url_divi_mytest - START: DiviImport.countries()")
        i = 0
        for c in DiviImport.countries():
            i += 1
            line = " | " + str(i) + " | " + c.countries.country_code + " | " + c.countries.country + " | " + c.countries.divi_region + " | "
            app.logger.info(line)
        flash("url_divi_mytest - DONE: DiviImport.countries()")
        app.logger.info("url_divi_mytest - DONE: DiviImport.countries()")
        flash("url_divi_mytest - START: DiviImport.get_new_dates_as_array()")
        app.logger.info("url_divi_mytest - START: DiviImport.get_new_dates_as_array()")
        i = 0
        for date_reported in DiviImport.get_new_dates_as_array():
            i += 1
            line = " | " + str(i) + " | " + date_reported + " | "
            app.logger.info(line)
        joungest_datum = DiviDateReported.get_joungest_datum()
        app.logger.info(joungest_datum)
        i = 0
        for divi_data in DiviData.get_data_for_one_day(joungest_datum):
            i += 1
            line = " | " + str(i) + " | " + str(divi_data.date_reported) + " | " + divi_data.country.country + " | "
            app.logger.info(line)
        flash("url_divi_mytest - DONE: DiviImport.get_new_dates_as_array()")
        app.logger.info("url_divi_mytest - DONE: DiviImport.get_new_dates_as_array()")
        return redirect(url_for('divi.url_divi_tasks'))


divi_urls = DiviUrls()

# ----------------------------------------------------------------------------------------------------------------
#  Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


class DiviTasks:

    @staticmethod
    @celery.task(bind=True)
    def task_divi_download(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" Received: task_divi_download [OK] ")
            app.logger.info("------------------------------------------------------------")
            divi_service.download()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_divi_download)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_divi_import_file(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" Received: task_divi_import_file [OK] ")
            app.logger.info("------------------------------------------------------------")
            divi_service.import_file()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_divi_import_file)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_divi_full_update_dimension_tables(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" Received: task_divi_full_update_dimension_tables [OK] ")
            app.logger.info("------------------------------------------------------------")
            divi_service.full_update_dimension_tables()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_divi_update_dimension_tables)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_divi_update_dimension_tables(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" Received: task_divi_update_dimension_tables [OK] ")
            app.logger.info("------------------------------------------------------------")
            divi_service.update_dimension_tables()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_divi_update_dimension_tables)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_divi_full_update_fact_table(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" Received: task_divi_full_update_fact_table [OK] ")
            app.logger.info("------------------------------------------------------------")
            divi_service.full_update_fact_table()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_divi_full_update_fact_table)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_divi_update_fact_table(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" Received: task_divi_update_fact_table [OK] ")
            app.logger.info("------------------------------------------------------------")
            divi_service.update_fact_table()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_divi_update_fact_table)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_divi_full_update(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" Received: task_divi_full_update [OK] ")
            app.logger.info("------------------------------------------------------------")
            divi_service.full_update()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_divi_full_update)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_divi_update(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" Received: task_divi_update [OK] ")
            app.logger.info("------------------------------------------------------------")
            divi_service.update()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_divi_update)"
        return result


divi_tasks = DiviTasks()

# ----------------------------------------------------------------------------------------------------------------
#  URL Routes for Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


class DiviTaskUrls:

    @staticmethod
    @app_divi.route('/task/download')
    @login_required
    def url_task_divi_download():
        app.logger.info("url_task_divi_download [start]")
        divi_service.download()
        flash("divi_service.download ok")
        app.logger.info("url_task_divi_download [done]")
        return redirect(url_for('divi.url_divi_tasks'))

    @staticmethod
    @app_divi.route('/task/import')
    @login_required
    def url_task_divi_import():
        app.logger.info("url_task_divi_import [start]")
        divi_tasks.task_divi_import_file.apply_async()
        flash("task_divi_import_file started")
        flash(message="long running background task started", category="warning")
        app.logger.info("url_task_divi_import [done]")
        return redirect(url_for('divi.url_divi_tasks'))

    @staticmethod
    @app_divi.route('/task/full/update/dimension-tables')
    @login_required
    def url_task_divi_full_update_dimension_tables():
        app.logger.info("url_task_divi_update_dimension_tables_only [start]")
        divi_tasks.task_divi_full_update_dimension_tables.apply_async()
        flash("task_divi_full_update_dimension_tables started")
        flash(message="long running background task started", category="warning")
        app.logger.info("url_task_divi_update_dimension_tables_only [done]")
        return redirect(url_for('divi.url_divi_tasks'))

    @staticmethod
    @app_divi.route('/task/update/dimension-tables')
    @login_required
    def url_task_divi_update_dimension_tables():
        app.logger.info("url_task_divi_update_dimension_tables [start]")
        divi_tasks.task_divi_update_dimension_tables.apply_async()
        flash("task_divi_update_dimension_tables started")
        flash(message="long running background task started", category="warning")
        app.logger.info("url_task_divi_update_dimension_tables [done]")
        return redirect(url_for('divi.url_divi_tasks'))

    @staticmethod
    @app_divi.route('/task/full/update/fact-table')
    @login_required
    def url_task_divi_full_update_fact_table():
        app.logger.info("url_task_divi_update_fact_table_initial_only [start]")
        divi_tasks.task_divi_full_update_fact_table.apply_async()
        flash("task_divi_full_update_fact_table started")
        flash(message="long running background task started", category="warning")
        app.logger.info("url_divi_task_update_full [done]")
        return redirect(url_for('divi.url_divi_tasks'))

    @staticmethod
    @app_divi.route('/task/update/fact-table')
    @login_required
    def url_task_divi_update_fact_table():
        app.logger.info("url_task_divi_update_fact_table [start]")
        divi_tasks.task_divi_update_fact_table.apply_async()
        flash("task_divi_update_fact_table started")
        flash(message="long running background task started", category="warning")
        app.logger.info("url_task_divi_update_fact_table [done]")
        return redirect(url_for('divi.url_divi_tasks'))

    @staticmethod
    @app_divi.route('/task/full/update')
    @login_required
    def url_task_divi_full_update():
        app.logger.info("url_task_divi_full_update [start]")
        divi_service.download()
        flash("divi_service.download ok")
        divi_tasks.task_divi_full_update.apply_async()
        flash("task_divi_full_update started")
        flash(message="long running background task started", category="warning")
        app.logger.info("url_task_divi_full_update [done]")
        return redirect(url_for('divi.url_divi_tasks'))

    @staticmethod
    @app_divi.route('/task/update')
    @login_required
    def url_task_divi_update():
        app.logger.info("url_task_divi_update [start]")
        divi_service.download()
        flash("divi_service.download ok")
        divi_tasks.task_divi_update.apply_async()
        flash("task_divi_update started")
        flash(message="long running background task started", category="warning")
        app.logger.info("url_task_divi_update [done]")
        return redirect(url_for('divi.url_divi_tasks'))


divi_task_urls = DiviTaskUrls()
