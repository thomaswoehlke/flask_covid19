from project.data.database import app
from project.data_all_notifications.notifications_model import Notification


class NotificationService:
    def __init__(self, database):
        self.__database = database
        app.logger.info(" ready: [Notification] Service")

    def notifications_count(self):
        return Notification.notifications_count()

    def notifications_find(self):
        return Notification.notifications_find()
