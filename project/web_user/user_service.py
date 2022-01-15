from project.data.database import app
from project.web_user.user_model import LoginForm
from project.web_user.user_model import WebUser


class WebUserService:
    def __init__(self, database):
        self.__database = database
        app.logger.info(" ready: [web] WebUser Service ")

    def set_database(self, database):
        self.__database = database

    def get_user_from_login_form(self, form: LoginForm):
        user = WebUser()
        user.email = form.email
        user.password = form.password
        return user

    def prepare_default_user_login(self, database):
        app.logger.info(" WebUserService.prepare_default_user_login()")
        self.__database = database
        if WebUser.count() == 0:
            app.logger.debug("-------------------------------------------------------")
            app.logger.info(" WebUser.count() == 0")
            login = app.config["USER_ADMIN_LOGIN"]
            name = app.config["USER_ADMIN_USERNAME"]
            pw = app.config["USER_ADMIN_PASSWORD"]
            user = WebUser.create_new(email=login, name=name, password_hash=pw)
            app.logger.info(user)
            self.__database.session.add(user)
            self.__database.session.commit()
            app.logger.debug("-------------------------------------------------------")
        else:
            app.logger.debug("-------------------------------------------------------")
            app.logger.info(" WebUser.count() > 0")
            app.logger.debug("-------------------------------------------------------")

