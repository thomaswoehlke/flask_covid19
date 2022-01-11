from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import login_required

from project.app_bootstrap.database import app, db, celery
from project.app_web.web.web_model_transient import WebPageContent
from project.data_all.data_all_notifications.notifications_model import Notification
from project.app_web.admin.app_admin_views import app_web_admin
from project.app_web.user.user_views import app_web_user
from project.data_all.all_views import app_all
from project.data_all.data_all_notifications.notifications_view import app_notification
from project.data_ecdc.ecdc_views import app_ecdc
from project.data_owid.owid_views import app_owid, app_owid_report
from project.data_rki.rki_views import app_rki
from project.data_vaccination.vaccination_views import app_vaccination
from project.data_who.who_views import app_who
from project.app_web.web.web_dispachter_service import admin_service

app_web = Blueprint(
    "app_web", __name__, template_folder="templates", url_prefix="/"
)

app.register_blueprint(app_web_user, url_prefix="/app/app_web_user")
app.register_blueprint(app_web_admin, url_prefix="/app/admin")
app.register_blueprint(app_web, url_prefix="/")
app.register_blueprint(app_notification, url_prefix="/app/all_notifications")
app.register_blueprint(app_all, url_prefix="/app/all")

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


class WebUrls:
    def __init__(self):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info(" ready: [WEB] WebUrls ")
        app.logger.debug("-----------------------------------------------------------")
        with app.app_context():
            task = Notification.create(sector="WEB", task_name="init").read()
            Notification.finish(task_id=task.id)

    @staticmethod
    @app.route("/home")
    def url_home():
        page_info = WebPageContent("Home", "Covid19 Data")
        return render_template(
            "app_web/page_home.html",
            page_info=page_info
        )

    @staticmethod
    @app.route("/")
    def url_root():
        return redirect(url_for("url_home"))

    @staticmethod
    @app.route("/admin")
    @login_required
    def url_admin_index():
        page_info = WebPageContent("Admin", "flask admin")
        return render_template(
            "app_web_admin/index.html",
            page_info=page_info
        )


web_urls = WebUrls()
