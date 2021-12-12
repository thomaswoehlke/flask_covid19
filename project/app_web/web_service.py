from project.app_config.database import app


class WebService:
    def __init__(self, database, user_service):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" [app_web] Web Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.__user_service = user_service
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ready: [app_web] Web Service ")
        app.logger.debug("------------------------------------------------------------")

    def create_user(self, database):
        app.logger.info(" ")
        app.logger.info("#############################################################")
        app.logger.info("#                create-user                                #")
        app.logger.info("#############################################################")
        app.logger.info(" ")
        self.__user_service.prepare_default_user_login(database)
        app.logger.info(" ")

    def prepare_run_web(self, database):
        app.logger.info(" ")
        app.logger.info("#############################################################")
        app.logger.info("#                Covid19 Data - WEB                         #")
        app.logger.info("#############################################################")
        app.logger.info(" ")
        self.__database = database
        self.__user_service.prepare_default_user_login(database)
        app.logger.info(" ")

    def prepare_run_mq(self, database):
        app.logger.info(" ")
        app.logger.info("#############################################################")
        app.logger.info("#                Covid19 Data - MQ (Celery WORKER)          #")
        app.logger.info("#############################################################")
        app.logger.info(" ")
        self.__database = database
        self.__user_service.prepare_default_user_login(database)
        app.logger.info(" ")

    def prepare_start_redis(self):
        app.logger.info("-------------------------------------------------------------")
        app.logger.info("#                start REDIS-Server                         #")
        app.logger.info("-------------------------------------------------------------")
