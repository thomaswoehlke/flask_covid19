from project.app_bootstrap.database import app
from project.data_all_notifications.notifications_model import Notification


class NotificationService:
    def __init__(self, database):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.debug(" [Notification] Service [init]")
        app.logger.debug("-----------------------------------------------------------")
        self.__database = database
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info(" ready: [Notification] Service")
        app.logger.debug("-----------------------------------------------------------")

    def notifications_count(self):
        return Notification.notifications_count()

    def notifications_find(self):
        return Notification.notifications_find()
