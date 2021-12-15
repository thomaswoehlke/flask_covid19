import datetime

from project.app_bootstrap.database import app
from project.app_bootstrap.database import db
from project.data_all.all_task_model import Task


class TaskService:
    def __init__(self, database):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.debug(" [Task] Service [init]")
        app.logger.debug("-----------------------------------------------------------")
        self.__database = database
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info(" ready: [Task] Service")
        app.logger.debug("-----------------------------------------------------------")
