from celery import states
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required
from project.app_bootstrap.database import admin
from project.app_bootstrap.database import app
from project.app_bootstrap.database import celery
from project.app_bootstrap.database import db
from project.app_web.web_dispachter_matrix_service import owid_service
from project.app_web.web_model_transient import WebPageContent
from project.data_owid.owid_model_data import OwidData
from project.data_owid.owid_model_date_reported import OwidDateReported
from project.data_owid.owid_model_flat import OwidFlat
from project.data_owid.owid_model_import import OwidImport
from project.data_owid.owid_model_location import OwidCountry
from project.data_owid.owid_model_location_group import OwidContinent
from project.data_owid.owid_service_test import OwidTestService
from sqlalchemy.exc import OperationalError

app_owid = Blueprint("owid", __name__, template_folder="templates", url_prefix="/owid ")

admin.add_view(ModelView(OwidImport, db.session, category="OWID"))
admin.add_view(ModelView(OwidFlat, db.session, category="OWID"))
admin.add_view(ModelView(OwidDateReported, db.session, category="OWID"))
admin.add_view(ModelView(OwidContinent, db.session, category="OWID"))
admin.add_view(ModelView(OwidCountry, db.session, category="OWID"))
admin.add_view(ModelView(OwidData, db.session, category="OWID"))

owid_test_service = OwidTestService(db, owid_service)

# ---------------------------------------------------------------------------------------------------------------
#  Url Routes Frontend
# ---------------------------------------------------------------------------------------------------------------


class OwidUrls:
    def __init__(self):
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ready: [OWID] OwidUrls ")
        app.logger.debug("------------------------------------------------------------")

    @staticmethod
    @app_owid.route("")
    @app_owid.route("/")
    def url_owid_root():
        return redirect(url_for("owid.url_owid_info"))

    @staticmethod
    @app_owid.route("/info")
    def url_owid_info():
        page_info = WebPageContent("OWID", "Info")
        return render_template("owid/owid_info.html", page_info=page_info)

    @staticmethod
    @app_owid.route("/imported/page/<int:page>")
    @app_owid.route("/imported")
    def url_owid_imported(page=1):
        page_info = WebPageContent("OWID", "Last Import")
        try:
            page_data = OwidImport.get_all(page)
        except OperationalError:
            flash("No data in the database.")
            page_data = None
        return render_template(
            "owid/imported/owid_imported.html", page_data=page_data, page_info=page_info
        )

    @staticmethod
    @app_owid.route("/flat/page/<int:page>")
    @app_owid.route("/flat")
    def url_owid_flat(page=1):
        page_info = WebPageContent("OWID", "flat")
        try:
            page_data = OwidImport.get_all(page)
        except OperationalError:
            flash("No data in the database.")
            page_data = None
        return render_template(
            "owid/flat/owid_flat.html", page_data=page_data, page_info=page_info
        )

    @staticmethod
    @app_owid.route("/date_reported/all/page/<int:page>")
    @app_owid.route("/date_reported/all")
    def url_owid_date_reported_all(page: int = 1):
        page_info = WebPageContent("OWID", "Date Reported", "All")
        try:
            page_data = OwidDateReported.get_all(page)
        except OperationalError:
            flash("No regions in the database.")
            page_data = None
        return render_template(
            "owid/date_reported/all/owid_date_reported_all.html",
            page_data=page_data,
            page_info=page_info,
        )

    @staticmethod
    @app_owid.route("/date_reported/<int:date_reported_id>/page/<int:page>")
    @app_owid.route("/date_reported/<int:date_reported_id>")
    def url_owid_date_reported_one(date_reported_id: int, page: int = 1):
        date_reported = OwidDateReported.get_by_id(date_reported_id)
        page_info = WebPageContent(
            "Date Reported: " + str(date_reported),
            "OWID",
            "data of all reported countries for OWID date reported "
            + str(date_reported)
            + " ",
        )
        try:
            page_data = OwidData.get_by_date_reported(date_reported, page)
        except OperationalError:
            flash("No data in the database.")
            page_data = None
        return render_template(
            "owid/date_reported/one/owid_date_reported_one.html",
            owid_date_reported=date_reported,
            page_data=page_data,
            page_info=page_info,
        )

    @staticmethod
    @app_owid.route("/date_reported/<int:date_reported_id>/cases_new/page/<int:page>")
    @app_owid.route("/date_reported/<int:date_reported_id>/cases_new")
    def url_owid_date_reported_one_cases_new(date_reported_id: int, page: int = 1):
        date_reported = OwidDateReported.get_by_id(date_reported_id)
        page_info = WebPageContent(
            "Date Reported: " + str(date_reported),
            "OWID",
            "data of all reported countries for OWID date reported "
            + str(date_reported)
            + " ",
        )
        try:
            page_data = OwidData.find_by_date_reported_order_by_cases_new(
                date_reported, page
            )
        except OperationalError:
            flash("No data in the database.")
            page_data = None
        return render_template(
            "owid/date_reported/cases/owid_date_reported_one_cases_new.html",
            owid_date_reported=date_reported,
            page_data=page_data,
            page_info=page_info,
        )

    @staticmethod
    @app_owid.route(
        "/date_reported/<int:date_reported_id>/cases_cumulative/page/<int:page>"
    )
    @app_owid.route("/date_reported/<int:date_reported_id>/cases_cumulative")
    def url_owid_date_reported_one_cases_cumulative(
        date_reported_id: int, page: int = 1
    ):
        date_reported = OwidDateReported.get_by_id(date_reported_id)
        page_info = WebPageContent(
            "Date Reported: " + str(date_reported),
            "OWID",
            "data of all reported countries for OWID date reported "
            + str(date_reported)
            + " ",
        )
        try:
            page_data = OwidData.find_by_date_reported_order_by_cases_cumulative(
                date_reported, page
            )
        except OperationalError:
            flash("No data in the database.")
            page_data = None
        return render_template(
            "owid/date_reported/cases/owid_date_reported_one_cases_cumulative.html",
            owid_date_reported=date_reported,
            page_data=page_data,
            page_info=page_info,
        )

    @staticmethod
    @app_owid.route("/date_reported/<int:date_reported_id>/deaths_new/page/<int:page>")
    @app_owid.route("/date_reported/<int:date_reported_id>/deaths_new")
    def url_owid_date_reported_one_deaths_new(date_reported_id: int, page: int = 1):
        date_reported = OwidDateReported.get_by_id(date_reported_id)
        page_info = WebPageContent(
            "Date Reported: " + str(date_reported),
            "OWID",
            "data of all reported countries for OWID date reported "
            + str(date_reported)
            + " ",
        )
        try:
            page_data = OwidData.find_by_date_reported_order_by_deaths_new(
                date_reported, page
            )
        except OperationalError:
            flash("No data in the database.")
            page_data = None
        return render_template(
            "owid/date_reported/deaths/owid_date_reported_one_deaths_new.html",
            owid_date_reported=date_reported,
            page_data=page_data,
            page_info=page_info,
        )

    @staticmethod
    @app_owid.route(
        "/date_reported/<int:date_reported_id>/deaths_cumulative/page/<int:page>"
    )
    @app_owid.route("/date_reported/<int:date_reported_id>/deaths_cumulative")
    def url_owid_date_reported_one_deaths_cumulative(
        date_reported_id: int, page: int = 1
    ):
        date_reported = OwidDateReported.get_by_id(date_reported_id)
        page_info = WebPageContent(
            "Date Reported: " + str(date_reported),
            "OWID",
            "data of all reported countries for OWID date reported "
            + str(date_reported)
            + " ",
        )
        try:
            page_data = OwidData.find_by_date_reported_order_by_deaths_cumulative(
                date_reported, page
            )
        except OperationalError:
            flash("No data in the database.")
            page_data = None
        return render_template(
            "owid/date_reported/deaths/owid_date_reported_one_deaths_cumulative.html",
            owid_date_reported=date_reported,
            page_data=page_data,
            page_info=page_info,
        )

    @staticmethod
    @app_owid.route("/continent/all/page/<int:page>")
    @app_owid.route("/continent/all")
    def url_owid_continent_all(page: int = 1):
        page_info = WebPageContent("Continents " "OWID", "all")
        try:
            page_data = OwidContinent.get_all(page)
        except OperationalError:
            flash("No data in the database.")
            page_data = None
        return render_template(
            "owid/continent/all/owid_continent_all.html",
            page_data=page_data,
            page_info=page_info,
        )

    @staticmethod
    @app_owid.route("/continent/<int:continent_id>/page/<int:page>")
    @app_owid.route("/continent/<int:continent_id>")
    def url_owid_continent_one(continent_id: int, page: int = 1):
        owid_continent_one = OwidContinent.get_by_id(continent_id)
        page_info = WebPageContent(
            "continent: " + owid_continent_one.location_group,
            "OWID",
            "countries for OWID continent " + owid_continent_one.location_group + " ",
        )
        try:
            page_data = OwidCountry.get_countries_for_continent(
                owid_continent_one, page
            )
        except OperationalError:
            flash("No data in the database.")
            page_data = None
        return render_template(
            "owid/continent/one/owid_continent_one.html",
            owid_continent=owid_continent_one,
            page_data=page_data,
            page_info=page_info,
        )

    @staticmethod
    @app_owid.route("/country/all/page/<int:page>")
    @app_owid.route("/country/all")
    def url_owid_country_all(page: int = 1):
        page_info = WebPageContent("Countries " "OWID", "all")
        try:
            page_data = OwidCountry.get_all(page)
        except OperationalError:
            flash("No data in the database.")
            page_data = None
        return render_template(
            "owid/country/all/owid_country_all.html",
            page_data=page_data,
            page_info=page_info,
        )

    @staticmethod
    @app_owid.route("/country/<int:country_id>/page/<int:page>")
    @app_owid.route("/country/<int:country_id>")
    def url_owid_country_one(country_id: int, page: int = 1):
        owid_country_one = OwidCountry.get_by_id(country_id)
        page_info = WebPageContent(
            "country: " + owid_country_one.location,
            "OWID",
            "on continent " + owid_country_one.location_group.location_group + " ",
        )
        try:
            page_data = OwidData.get_by_location(owid_country_one, page)
        except OperationalError:
            flash("No data in the database.")
            page_data = None
        return render_template(
            "owid/country/one/owid_country_one.html",
            owid_country=owid_country_one,
            page_data=page_data,
            page_info=page_info,
        )

    @staticmethod
    @app_owid.route("/country/germany/page/<int:page>")
    @app_owid.route("/country/germany")
    def url_owid_country_one_germany(page: int = 1):
        owid_country_germany = OwidCountry.get_germany()
        page_data = None
        if owid_country_germany is None:
            flash("country: Germany not found in Database", category="error")
            return redirect(url_for("owid.url_owid_info"))
        my_location = owid_country_germany.location
        my_region = owid_country_germany.location_group.location_group
        try:
            page_data = OwidData.get_by_location(owid_country_germany, page)
            if page_data is None:
                flash("country: Germany not found in Database", category="error")
                return redirect(url_for("owid.url_owid_info"))
        except OperationalError:
            flash("No data in the database.")
        page_info = WebPageContent(
            "country: " + my_location, "OWID", "on continent " + my_region + " "
        )
        return render_template(
            "owid/country/germany/owid_country_one_germany.html",
            owid_country=owid_country_germany,
            page_data=page_data,
            page_info=page_info,
        )

    @staticmethod
    @app_owid.route("/delete_last_day")
    def url_owid_delete_last_day():
        app.logger.info("url_owid_delete_last_day [start]")
        flash("url_owid_delete_last_day [start]")
        owid_service.delete_last_day()
        flash("url_owid_delete_last_day [done]")
        app.logger.info("url_owid_delete_last_day [done]")
        return redirect(url_for("owid.url_owid_date_reported_all"))

    @staticmethod
    @app_owid.route("/data/explorer")
    def url_owid_data_explorer():
        app.logger.info("url_owid_data_explorer [start]")
        page_info = WebPageContent("Data Explorer " "OWID", "all")
        try:
            page_countries = OwidCountry.find_all_for_data_explorer()
            page_data = None
        except OperationalError:
            flash("No data in the database.")
            page_data = None
        app.logger.info("url_owid_data_explorer [done]")
        return render_template(
            "owid/data/explorer.html",
            page_data=page_data,
            page_countries=page_countries,
            page_info=page_info,
        )


owid_urls = OwidUrls()

# ----------------------------------------------------------------------------------------------------------------
#  Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


class OwidTasks:
    def __init__(self):
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ready: [OWID] OwidTasks ")
        app.logger.debug("------------------------------------------------------------")

    @staticmethod
    @celery.task(bind=True)
    def task_owid_import(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" Received: [OWID] task_owid_import [OK] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
            owid_service.import_file()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_owid_import)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_owid_full_update_dimension_tables(self):
        self.update_state(state=states.STARTED)
        app.logger.info("------------------------------------------------------------")
        app.logger.info(
            " Received: [OWID] task_owid_full_update_dimension_tables [OK] "
        )
        app.logger.info("------------------------------------------------------------")
        owid_service.full_update_dimension_tables()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_owid_full_update_dimension_tables)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_owid_update_dimension_tables(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" Received: [OWID] task_owid_update_dimension_tables [OK] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
            owid_service.update_dimension_tables()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_owid_update_dimension_tables)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_owid_full_update_fact_table(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" Received: [OWID] task_owid_full_update_fact_table [OK] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
            owid_service.full_update_fact_table()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_owid_full_update_fact_table)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_owid_update_fact_table(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" Received: [OWID] task_owid_update_fact_table [OK] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
            owid_service.update_fact_table()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_owid_update_fact_table)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_owid_full_update(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" Received: [OWID] task_owid_full_update [OK] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
            owid_service.full_update()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_owid_full_update)"
        return result

    @staticmethod
    @celery.task(bind=True)
    def task_owid_update(self):
        self.update_state(state=states.STARTED)
        with app.app_context():
            app.logger.info(
                "------------------------------------------------------------"
            )
            app.logger.info(" Received: [OWID] task_owid_update [OK] ")
            app.logger.info(
                "------------------------------------------------------------"
            )
            owid_service.update()
        self.update_state(state=states.SUCCESS)
        result = "OK (task_owid_update)"
        return result


owid_tasks = OwidTasks()

# ----------------------------------------------------------------------------------------------------------------
#  URL Routes for Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


class OwidTaskUrls:
    def __init__(self):
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ready: [OWID] OwidTaskUrls ")
        app.logger.debug("------------------------------------------------------------")

    @staticmethod
    @app_owid.route("/task/download/only")
    def url_task_owid_download():
        app.logger.info("url_owid_task_download_only [start]")
        owid_service.download()
        flash("owid_service.run_download_only [done]")
        app.logger.info("url_owid_task_download_only [done]")
        return redirect(url_for("owid.url_owid_info"))

    @staticmethod
    @app_owid.route("/task/import/only")
    def url_task_owid_import():
        app.logger.info("url_task_owid_import_only [start]")
        owid_tasks.task_owid_import.apply_async()
        flash("task_owid_import started")
        flash(message="long running background task started", category="warning")
        app.logger.warn("started task_owid_import_only")
        app.logger.info("url_task_owid_import_only [done]")
        return redirect(url_for("owid.url_owid_info"))

    @staticmethod
    @app_owid.route("/task/full/update/dimension-tables")
    def url_task_owid_full_update_dimension_tables():
        app.logger.info("url_task_owid_full_update_dimension_tables [start]")
        owid_tasks.task_owid_full_update_dimension_tables.apply_async()
        flash("task_owid_full_update_dimension_tables started")
        flash(message="long running background task started", category="warning")
        app.logger.warn("started task_owid_full_update_dimension_tables")
        app.logger.info("url_task_owid_full_update_dimension_tables [start]")
        return redirect(url_for("owid.url_owid_info"))

    @staticmethod
    @app_owid.route("/task/update/dimension-tables")
    def url_task_owid_update_dimension_tables():
        app.logger.info("url_task_owid_update_dimension_tables [start]")
        owid_tasks.task_owid_update_dimension_tables.apply_async()
        flash("task_owid_update_dimension_tables started")
        flash(message="long running background task started", category="warning")
        app.logger.warn("started task_owid_update_dimension_tables")
        app.logger.info("url_task_owid_update_dimension_tables [done]")
        return redirect(url_for("owid.url_owid_info"))

    @staticmethod
    @app_owid.route("/task/full/update/fact-table")
    def url_task_owid_full_update_fact_table():
        app.logger.info("url_task_owid_update_fact_table_incremental_only [start]")
        owid_tasks.task_owid_full_update_fact_table.apply_async()
        flash("task_owid_full_update_fact_table started")
        flash(message="long running background task started", category="warning")
        app.logger.info("url_task_owid_update_fact_table_incremental_only [done]")
        return redirect(url_for("owid.url_owid_info"))

    @staticmethod
    @app_owid.route("/task/update/fact-table")
    def url_task_owid_update_fact_table():
        app.logger.info("url_task_owid_update_fact_table_initial_only [start]")
        owid_tasks.task_owid_update_fact_table.apply_async()
        flash("task_owid_update_fact_table started")
        flash(message="long running background task started", category="warning")
        app.logger.info("url_task_owid_update_fact_table_initial_only [done]")
        return redirect(url_for("owid.url_owid_info"))

    @staticmethod
    @app_owid.route("/task/full/update")
    def url_task_owid_full_update():
        app.logger.info("url_task_owid_full_update [start]")
        owid_service.download()
        flash("owid_service.run_download_only [done]")
        owid_tasks.task_owid_full_update.apply_async()
        flash("task_owid_full_update started")
        flash(
            message="long running background task started: task_owid_full_update",
            category="warning",
        )
        app.logger.info("url_task_owid_full_update [done]")
        return redirect(url_for("owid.url_owid_info"))

    @staticmethod
    @app_owid.route("/task/update")
    def url_task_owid_update():
        app.logger.info("url_task_owid_update [start]")
        owid_service.download()
        flash("owid_service.run_download_only [done]")
        owid_tasks.task_owid_update.apply_async()
        flash("task_owid_update started")
        flash(message="long running background task started", category="warning")
        app.logger.info("url_task_owid_update [done]")
        return redirect(url_for("owid.url_owid_info"))


owid_task_urls = OwidTaskUrls()

# ---------------------------------------------------------------------------------------------------------------
#  Url Routes Frontend TESTS
# ---------------------------------------------------------------------------------------------------------------


class OwidTestUrls:
    def __init__(self):
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ready: [OWID] OwidTestUrls ")
        app.logger.debug("------------------------------------------------------------")

    @staticmethod
    @app_owid.route("/test/update_dimension_tables_only")
    @login_required
    def url_owid_test_update_dimension_tables_only():
        app.logger.info("test_update_dimension_tables_only - START")
        flash("test_update_dimension_tables_only - START")
        return redirect(url_for("owid.url_owid_info"))

    @staticmethod
    @app_owid.route("/test/update_fact_table_incremental_only")
    @login_required
    def url_owid_test_update_fact_table_incremental_only():
        app.logger.info("update_fact_table_incremental_only - START")
        flash("update_fact_table_incremental_only - START")
        return redirect(url_for("owid.url_owid_info"))

    @staticmethod
    @app_owid.route("/test/update_fact_table_initial_only")
    @login_required
    def url_owid_test_update_fact_table_initial_only():
        app.logger.info("update_fact_table_initial_only - START")
        flash("update_fact_table_initial_only - START")
        return redirect(url_for("owid.url_owid_info"))

    @staticmethod
    @app_owid.route("/test/owid_import/countries")
    @login_required
    def url_owid_test_owid_import_countries():
        app.logger.info("url_owid_test_owid_import_countries - START")
        flash("url_owid_test_owid_import_countries - START")
        i = 0
        for c in OwidImport.countries():
            i += 1
            line = (
                " | "
                + str(i)
                + " | "
                + c.countries.iso_code
                + " | "
                + c.countries.location
                + " | "
                + c.countries.continent
                + " | "
            )
            app.logger.info(line)
        app.logger.info("url_owid_test_owid_import_countries - DONE")
        flash("url_owid_test_owid_import_countries - DONE")
        return redirect(url_for("owid.url_owid_info"))

    @staticmethod
    @app_owid.route("/test/owid_import/get_new_dates_as_array")
    @login_required
    def url_owid_test_owid_import_get_new_dates_as_array():
        app.logger.info("url_owid_test_owid_import_get_new_dates_as_array - START")
        flash("url_owid_test_owid_import_get_new_dates_as_array - START")
        i = 0
        for date_reported in OwidImport.get_new_dates_reported_as_array():
            i += 1
            line = " | " + str(i) + " | " + date_reported + " | "
            app.logger.info(line)
        app.logger.info("url_owid_test_owid_import_get_new_dates_as_array - DONE")
        flash("url_owid_test_owid_import_get_new_dates_as_array - DONE")
        return redirect(url_for("owid.url_owid_info"))

    @staticmethod
    @app_owid.route("/test/owid_data/get_datum_of_all_owid_data")
    @login_required
    def url_owid_test_owid_data_get_datum_of_all_owid_data():
        app.logger.info("url_owid_test_owid_data_get_datum_of_all_owid_data - START")
        flash("url_owid_test_owid_data_get_datum_of_all_owid_data - START")
        for datum in OwidData.get_datum_of_all_data():
            app.logger.info(str(datum))
        app.logger.info("url_owid_test_owid_data_get_datum_of_all_owid_data - DONE")
        flash("url_owid_test_owid_data_get_datum_of_all_owid_data - DONE")
        return redirect(url_for("owid.url_owid_info"))

    @staticmethod
    @app_owid.route("/test/owid_data/get_datum_of_all_owid_import")
    @login_required
    def url_owid_test_owid_data_get_datum_of_all_owid_import():
        app.logger.info("url_owid_test_owid_data_get_datum_of_all_owid_import - START")
        flash("url_owid_test_owid_data_get_datum_of_all_owid_import - START")
        for datum in OwidImport.get_datum_of_all_import():
            app.logger.info(str(datum))
        app.logger.info("url_owid_test_owid_data_get_datum_of_all_owid_import - DONE")
        flash("url_owid_test_owid_data_get_datum_of_all_owid_import - DONE")
        return redirect(url_for("owid.url_owid_info"))

    @staticmethod
    @app_owid.route("/test/owid_service/owid_import/get_new_dates_as_array")
    @login_required
    def url_owid_test_owid_service_owid_import_get_new_dates_as_array():
        app.logger.info(
            "url_owid_test_owid_service_owid_import_get_new_dates_as_array - START"
        )
        flash("url_owid_test_owid_service_owid_import_get_new_dates_as_array - START")
        for datum in owid_service.service_update.owid_import_get_new_dates_as_array():
            app.logger.info(str(datum))
        app.logger.info(
            "url_owid_test_owid_service_owid_import_get_new_dates_as_array - DONE"
        )
        flash("url_owid_test_owid_service_owid_import_get_new_dates_as_array - DONE")
        return redirect(url_for("owid.url_owid_info"))

    @staticmethod
    @app_owid.route("/test/owid_test_service/update_dimension_tables")
    @login_required
    def url_owid_test_full_update_dimension_tables():
        app.logger.info("url_owid_test_full_update_dimension_tables - START")
        flash("owid_test_service.full_update_dimension_tables() - START")
        owid_test_service.full_update_dimension_tables()
        app.logger.info("owid_test_service.full_update_dimension_tables() - DONE")
        flash("url_owid_test_full_update_dimension_tables - DONE")
        return redirect(url_for("owid.url_owid_info"))


owid_test_urls = OwidTestUrls()
