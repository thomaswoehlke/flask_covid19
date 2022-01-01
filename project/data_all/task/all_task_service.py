from project.app_bootstrap.database import app
from project.data_all.task.all_task_model import Task


class TaskService:
    def __init__(self, database):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.debug(" [Task] Service [init]")
        app.logger.debug("-----------------------------------------------------------")
        self.__database = database
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info(" ready: [Task] Service")
        app.logger.debug("-----------------------------------------------------------")

    def notifications_count(self):
        return Task.notifications_count()

    def notifications_find(self):
        return Task.notifications_find()
