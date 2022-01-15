from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import login_required

from project.data.database import app, db
from project.web.model.web_model_transient import WebPageContent
from project.data_all_notifications.notifications_model import Notification
from project.data_all_notifications.notifications_service import NotificationService

notification_service = NotificationService(db)

app_notification = Blueprint(
    "data_all_notifications", __name__,
    template_folder="templates", url_prefix="/app/all_notifications"
)


class NotificationUrls:
    def __init__(self):
        app.logger.info(" ready: [ALL] NotificationUrls ")

    @staticmethod
    @app_notification.route("/notification/page/<int:page>")
    @app_notification.route("/notification")
    @login_required
    def url_all_notification(page=1):
        page_info = WebPageContent("All", "Notifications")
        page_data = Notification.notifications_get(page)
        return render_template(
            "data_all_notification/data_all_notification.html",
            page_data=page_data,
            page_info=page_info)

    @staticmethod
    @app_notification.route("/notification/mark_read")
    @login_required
    def url_all_notification_mark_read():
        data = Notification.notifications_find_asc(10)
        for o in data:
            o.read()
            db.session.add(o)
        db.session.commit()
        return redirect(url_for("data_all_notifications.url_all_notification"))


notification_urls = NotificationUrls()