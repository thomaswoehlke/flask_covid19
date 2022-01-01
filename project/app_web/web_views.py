from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import url_for
from project.app_bootstrap.database import app, db, celery
from project.app_web.admin.app_admin_views import blueprint_app_admin
from project.app_web.user.user_views import blueprint_app_user
from project.app_web.web.web_model_transient import WebPageContent
from project.data_all.all_views import blueprint_app_all
from project.data_ecdc.ecdc_views import app_ecdc
from project.data_owid.owid_views import app_owid, app_owid_report
from project.data_rki.rki_views import app_rki
from project.data_vaccination.vaccination_views import app_vaccination
from project.data_who.who_views import app_who
from project.app_web.web.web_dispachter_service import app_admin_service

blueprint_application = Blueprint(
    "app_web", __name__, template_folder="templates", url_prefix="/"
)

app.register_blueprint(blueprint_application, url_prefix="/")

app.register_blueprint(blueprint_app_user, url_prefix="/app/usr")
app.register_blueprint(blueprint_app_admin, url_prefix="/app/admin")
app.register_blueprint(blueprint_app_all, url_prefix="/app/all")

app.register_blueprint(app_who, url_prefix="/who")
app.register_blueprint(app_owid, url_prefix="/owid")
app.register_blueprint(app_owid_report, url_prefix="/owid/report")
app.register_blueprint(app_ecdc, url_prefix="/ecdc")
app.register_blueprint(app_vaccination, url_prefix="/vaccination")
app.register_blueprint(app_rki, url_prefix="/rki/")


#######################################################################################
#
# WEB
#


class BlueprintApplicationUrls:
    def __init__(self):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info(" ready: [WEB] ApplicationUrls ")
        app.logger.debug("-----------------------------------------------------------")

    @staticmethod
    @app.route("/home")
    def url_home():
        page_info = WebPageContent("Home", "Covid19 Data")
        return render_template("app_application/page_home.html", page_info=page_info)

    @staticmethod
    @app.route("/")
    def url_root():
        return redirect(url_for("url_home"))

    @staticmethod
    @app.route("/admin")
    def url_admin_index():
        page_info = WebPageContent("Admin", "Covid19 Admin")
        return render_template("app_application/index.html", page_info=page_info)

    @staticmethod
    @app.route("/status")
    def url_database_table_row_count():
        page_info = WebPageContent("Admin", "Status")
        database_table_row_count = app_admin_service.database_table_row_count()
        return render_template(
            "app_application/status/status.html",
            page_info=page_info,
            database_table_row_count=database_table_row_count
        )


blueprint_application_urls = BlueprintApplicationUrls()
