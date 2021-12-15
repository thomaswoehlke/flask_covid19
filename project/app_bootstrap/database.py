import os
import sys
from logging.config import dictConfig

from celery import Celery
from flask import Flask
from flask_admin import Admin
from flask_bs4 import Bootstrap
from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from project.app_bootstrap import config
from project.app_bootstrap import pytestconfig

# from flask_caching import Cache


class Covid19Application:
    def __init__(self, testing=False):
        self.app = Flask("flask_covid19")
        self.app_cors = CORS()
        if testing:
            self.app.config.from_object(pytestconfig)
        else:
            self.app.config.from_object(config)
        self.__init_db()
        self.__init_login()
        self.__init_bootstrap()
        self.__init_admin()
        self.__init_loging()
        oo_list = [self.db, self.app_cors, self.login_manager, self.app_bootstrap]
        for oo in oo_list:
            oo.init_app(self.app)
        self.root_dir = os.getcwd()
        self.create_celery()
        self.__print_config()

    def __init_db(self):
        self.db = SQLAlchemy()
        self.database_type = self.app.config["SQLALCHEMY_DATABASE_TYPE"]
        self.db_uri = self.__create_db_uri(self.database_type)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = self.db_uri
        self.app.config[
            "SQLALCHEMY_TRACK_MODIFICATIONS"
        ] = False  # silence the deprecation warning
        self.items_per_page = self.app.config["SQLALCHEMY_ITEMS_PER_PAGE"]
        return self

    def __int_cache(self):
        # self.cache = Cache()
        self.config_cache_simple = {
            "DEBUG": True,
            "CACHE_TYPE": "SimpleCache",
            "CACHE_DEFAULT_TIMEOUT": 120,
            "CACHE_KEY_PREFIX": "flask_covid19_",
        }
        self.config_cache_memcached = {
            "DEBUG": True,
            "CACHE_TYPE": "MemcachedCache",
            "CACHE_MEMCACHED_SERVERS": "127.0.0.1:11211",
            "CACHE_DEFAULT_TIMEOUT": 120,
            "CACHE_KEY_PREFIX": "flask_covid19_",
        }
        # self.cache.init_app(self.app, config=self.config_cache_memcached)
        # with self.app.app_context():
        #    self.cache.clear()
        return self

    def __init_bootstrap(self):
        self.app_bootstrap = Bootstrap()
        self.app.config["BOOTSTRAP_SERVE_LOCAL"] = True
        self.app.config["BOOTSTRAP_USE_CDN"] = False
        self.app.config["BOOTSTRAP_CUSTOM_CSS"] = True
        return self

    def __init_login(self):
        self.login_manager = LoginManager()
        self.login_manager.login_view = "usr.login"
        return self

    def __init_admin(self):
        self.app.config["FLASK_ADMIN_SWATCH"] = "darkly"
        self.admin = Admin(self.app, name="covid19 | admin", template_mode="bootstrap5")
        return self

    def __init_loging(self):
        self.logging_config = {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                }
            },
            "handlers": {
                "wsgi": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://flask.logging.wsgi_errors_stream",
                    "formatter": "default",
                }
            },
            "root": {"level": "INFO", "handlers": ["wsgi"]},
        }
        dictConfig(self.logging_config)
        return self

    def __create_db_uri(self, database_type: str):
        if database_type == "mariadb":
            return "mariadb+mariadbconnector://{user}:{pw}@{url}/{db}".format(
                user=self.app.config["SQLALCHEMY_DATABASE_USER"],
                pw=self.app.config["SQLALCHEMY_DATABASE_PW"],
                url=self.app.config["SQLALCHEMY_DATABASE_HOST"],
                db=self.app.config["SQLALCHEMY_DATABASE_DB"],
            )
        if database_type == "postgresql":
            return "postgresql+psycopg2://{user}:{pw}@{url}/{db}".format(
                user=self.app.config["SQLALCHEMY_DATABASE_USER"],
                pw=self.app.config["SQLALCHEMY_DATABASE_PW"],
                url=self.app.config["SQLALCHEMY_DATABASE_HOST"],
                db=self.app.config["SQLALCHEMY_DATABASE_DB"],
            )
        if database_type == "mysql":
            return "mysql://{user}:{pw}@{url}/{db}".format(
                user=self.app.config["SQLALCHEMY_DATABASE_USER"],
                pw=self.app.config["SQLALCHEMY_DATABASE_PW"],
                url=self.app.config["SQLALCHEMY_DATABASE_HOST"],
                db=self.app.config["SQLALCHEMY_DATABASE_DB"],
            )
        return None

    def get_db(self):
        self.__init_db()
        return self.db

    def create_db(self):
        self.db.create_all()
        return self

    def __create_celery_broker_paths(self):
        broker_path = self.root_dir + os.sep + "broker" + os.sep
        self.broker_out = broker_path + "out"
        self.broker_procesed = broker_path + "processed"
        for f in [self.broker_out, self.broker_procesed]:
            if not os.path.exists(f):
                os.makedirs(f)
        return self

    def __init_celery(self):
        self.__create_celery_broker_paths()
        if sys.platform == "linux":
            if self.root_dir.endswith("project"):
                self.root_dir.replace(os.sep + "project", "")
            os.chdir(self.root_dir)
        else:
            os.chdir(self.root_dir)
        self.app.logger.info(os.getcwd())
        celery = Celery("flask_covid19_celery")
        self.__create_celery_broker_paths()
        celery.conf.update(self.app.config)
        if sys.platform == "linux":
            self.broker_url = "filesystem://"
            self.broker_transport_options = {
                "data_folder_in": self.broker_out,
                "data_folder_out": self.broker_out,
                "data_folder_processed": self.broker_procesed,
            }
            self.conf_update = {
                "broker_url": self.broker_url,
                "broker_transport_options": self.broker_transport_options,
            }
            celery.conf.update(self.conf_update)
        else:
            self.broker_url = "filesystem://"
            self.broker_transport_options = {
                "data_folder_in": self.broker_out,
                "data_folder_out": self.broker_out,
                "data_folder_processed": self.broker_procesed,
            }
            self.conf_update = {
                "broker_url": self.broker_url,
                "broker_transport_options": self.broker_transport_options,
            }
            celery.conf.update(self.conf_update)
        return celery

    def create_celery(self):
        return self.__init_celery()

    def __print_config(self):
        self.app.logger.debug("-------------------------------------------------------")
        for key in self.app.config.keys():
            self.app.logger.debug(" " + str(key) + " " + str(self.app.config[key]))
        self.app.logger.debug("-------------------------------------------------------")


covid19_application = Covid19Application()
app = covid19_application.app
db = covid19_application.db
admin = covid19_application.admin
root_dir = covid19_application.root_dir
login_manager = covid19_application.login_manager
items_per_page = covid19_application.items_per_page
celery = covid19_application.create_celery()
