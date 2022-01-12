from project.data.database import app


class WebService:
    def __init__(self, database, user_service):
        self.__database = database
        self.__user_service = user_service
        app.logger.info(" ready: [web] Web Service ")

    def create_user(self, database):
        app.logger.info(" ")
        app.logger.info("############################################################")
        app.logger.info("#                create-user                               #")
        app.logger.info("############################################################")
        app.logger.info(" ")
        self.__user_service.prepare_default_user_login(database)
        app.logger.info(" ")

    def prepare_run_web(self, database):
        app.logger.info(" ")
        app.logger.info("############################################################")
        app.logger.info("#                Covid19 Data - WEB                        #")
        app.logger.info("############################################################")
        app.logger.info(" ")
        self.__database = database
        self.__user_service.prepare_default_user_login(database)
        app.logger.info(" ")

    def prepare_run_mq(self, database):
        app.logger.info(" ")
        app.logger.info("############################################################")
        app.logger.info("#                Covid19 Data - MQ (Celery WORKER)         #")
        app.logger.info("############################################################")
        app.logger.info(" ")
        self.__database = database
        self.__user_service.prepare_default_user_login(database)
        app.logger.info(" ")

    def prepare_start_redis(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info("-                start REDIS-Server                        -")
        app.logger.info("------------------------------------------------------------")
