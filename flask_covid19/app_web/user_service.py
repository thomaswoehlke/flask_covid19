from app_config.database import app
from app_web.user_model import User, LoginForm


class UserService:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" User Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" [app_web] User Service [ready]")
        app.logger.debug("------------------------------------------------------------")

    def get_user_from_login_form(self, form: LoginForm):
        user = User()
        user.email = form.email
        user.password = form.password
        return user

    def prepare_default_user_login(self):
        app.logger.info(" UserService.prepare_default_user_login()")
        if User.count() == 0:
            app.logger.info("User.count() == 0")
            login = app.config['USER_ADMIN_LOGIN']
            name = app.config['USER_ADMIN_USERNAME']
            pw = app.config['USER_ADMIN_PASSWORD']
            user = User.create_new(email=login, name=name, password_hash=pw)
            self.__database.session.add(user)
            self.__database.session.commit()
        else:
            app.logger.info("User.count() > 0")


