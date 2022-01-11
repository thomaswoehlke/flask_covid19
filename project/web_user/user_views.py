import flask

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from sqlalchemy.exc import OperationalError

from project.data.database import app, db
from project.data.database import admin, login_manager
from project.web_user.user_model import LoginForm
from project.web_user.user_model import User
from project.web.web.web_model_transient import WebPageContent

app_web_user = Blueprint(
    "web_user", __name__,
    template_folder="templates",
    url_prefix="/app/web_user"
)

admin.add_view(ModelView(User, db.session, category="USR"))


# ------------------------------------------------------------------------------------
# URLs Login and Logout
# ------------------------------------------------------------------------------------


class AppUserUrls:
    def __init__(self):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info(" ready: [USR] UserUrls ")
        app.logger.debug("-----------------------------------------------------------")
        with app.app_context():
            db.create_all()
            if User.count() == 0:
                app.logger.debug("---------------------------------------------------")
                app.logger.info(" User.count() == 0")
                login = app.config["USER_ADMIN_LOGIN"]
                name = app.config["USER_ADMIN_USERNAME"]
                pw = app.config["USER_ADMIN_PASSWORD"]
                user = User.create_new(email=login, name=name, password_hash=pw)
                app.logger.info(user)
                db.session.add(user)
                db.session.commit()
                app.logger.debug("---------------------------------------------------")
            else:
                app.logger.debug("---------------------------------------------------")
                app.logger.info(" User.count() > 0")
                app.logger.debug("---------------------------------------------------")

    @staticmethod
    @app_web_user.route("/login", methods=["GET"])
    def login_form():
        page_info = WebPageContent("web_user", "Login")
        if current_user.is_authenticated:
            return redirect(url_for("web_user.profile"))
        form = LoginForm()
        return flask.render_template("app_web_user/login.html", form=form,
                                     page_info=page_info)

    @staticmethod
    @app_web_user.route("/login", methods=["POST"])
    def login():
        page_info = WebPageContent("USR", "Login")
        if current_user.is_authenticated:
            return redirect(url_for("web_user.profile"))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash("Invalid username or password")
                return redirect(url_for("web_user.login"))
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for("web_user.profile"))
        return flask.render_template("app_web_user/login.html", form=form,
                                     page_info=page_info)

    @staticmethod
    @app_web_user.route("/profile")
    @login_required
    def profile():
        page_info = WebPageContent("USR", "profile")
        return flask.render_template("app_web_user/profile.html", page_info=page_info)

    @staticmethod
    @app_web_user.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("web_user.login"))

    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)

    @staticmethod
    @login_manager.unauthorized_handler
    def unauthorized():
        flash("not authorized")
        return redirect(url_for("web_user.login"))

    # ---------------------------------------------------------------------------------
    #  Url Routes Frontend
    # ---------------------------------------------------------------------------------

    @staticmethod
    @app_web_user.route("/info/page/<int:page>")
    @app_web_user.route("/info")
    @login_required
    def url_user_info(page=1):
        page_info = WebPageContent("USR", "Info")
        try:
            page_data = User.get_all_as_page(page)
        except OperationalError:
            flash("No data in the database.")
            page_data = None
        return render_template(
            "app_web_user/user_info.html", page_data=page_data, page_info=page_info
        )

    @staticmethod
    @app_web_user.route("/tasks")
    @login_required
    def url_user_tasks():
        page_info = WebPageContent("USR", "Tasks")
        return render_template("app_web_user/user_tasks.html", page_info=page_info)


app_user_urls = AppUserUrls()
