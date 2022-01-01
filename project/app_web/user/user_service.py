from project.app_bootstrap.database import app
from project.app_web.user.user_model import LoginForm
from project.app_web.user.user_model import User


class UserService:
    def __init__(self, database):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.debug(" User Service [init]")
        app.logger.debug("-----------------------------------------------------------")
        self.__database = database
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info(" ready: [app_web] User Service ")
        app.logger.debug("-----------------------------------------------------------")

    def set_database(self, database):
        self.__database = database

    def get_user_from_login_form(self, form: LoginForm):
        user = User()
        user.email = form.email
        user.password = form.password
        return user

    def prepare_default_user_login(self, database):
        app.logger.info(" UserService.prepare_default_user_login()")
        self.__database = database
        if User.count() == 0:
            app.logger.debug("-------------------------------------------------------")
            app.logger.info(" User.count() == 0")
            login = app.config["USER_ADMIN_LOGIN"]
            name = app.config["USER_ADMIN_USERNAME"]
            pw = app.config["USER_ADMIN_PASSWORD"]
            user = User.create_new(email=login, name=name, password_hash=pw)
            app.logger.info(user)
            self.__database.session.add(user)
            self.__database.session.commit()
            app.logger.debug("-------------------------------------------------------")
        else:
            app.logger.debug("-------------------------------------------------------")
            app.logger.info(" User.count() > 0")
            app.logger.debug("-------------------------------------------------------")

