import os
import sys

from flask import Flask, Blueprint
#from flask_caching import Cache
from flask_cors import CORS
from flask_bs4 import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from logging.config import dictConfig
from flask_admin import Admin
from celery import Celery

from app_config import config


class Covid19Application:

    def __init__(self):
        self.app = Flask('covid19')
        self.app_cors = CORS()
        self.login_manager = LoginManager()
        # self.cache = Cache()
        self.app.config.from_object(config)
        self.login_manager.login_view = 'usr.login'
        self.db = SQLAlchemy()
        self.database_type = self.app.config['SQLALCHEMY_DATABASE_TYPE']
        self.db_uri = self.__create_db_uri(self.database_type)
        self.app.config['BOOTSTRAP_SERVE_LOCAL'] = True
        self.app.config['BOOTSTRAP_USE_CDN'] = False
        self.app.config['BOOTSTRAP_CUSTOM_CSS'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning
        self.app.config['FLASK_ADMIN_SWATCH'] = 'darkly'
        self.items_per_page = self.app.config['SQLALCHEMY_ITEMS_PER_PAGE']
        self.app_bootstrap = Bootstrap(self.app)
        oo_list = [
            self.db,
            self.app_cors,
            self.login_manager
        ]
        for oo in oo_list:
            oo.init_app(self.app)
        self.config_cache_simple = {
            "DEBUG": True,
            "CACHE_TYPE": "SimpleCache",
            "CACHE_DEFAULT_TIMEOUT": 120,
            "CACHE_KEY_PREFIX": 'flask_covid19_'
        }
        self.config_cache_memcached = {
            "DEBUG": True,
            "CACHE_TYPE": "MemcachedCache",
            "CACHE_MEMCACHED_SERVERS": "127.0.0.1:11211",
            "CACHE_DEFAULT_TIMEOUT": 120,
            "CACHE_KEY_PREFIX": 'flask_covid19_'
        }
        # self.cache.init_app(self.app, config=self.config_cache_memcached)
        # with self.app.app_context():
        #    cache.clear()
        self.logging_config = {
            'version': 1,
            'formatters': {
                'default': {
                    'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                }
            },
            'handlers': {
                'wsgi': {
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://flask.logging.wsgi_errors_stream',
                    'formatter': 'default'
                }
            },
            'root': {
                'level': 'INFO',
                'handlers': ['wsgi']
            }
        }
        dictConfig(self.logging_config)
        self.admin = Admin(
            self.app,
            name='covid19 | admin',
            template_mode='bootstrap5')
        self.root_dir = os.getcwd()
        self.__create_celery_broker_paths()
        self.create_celery()

    def __create_db_uri(self, database_type: str):
        if database_type == 'mariadb':
            return 'mariadb+mariadbconnector://{user}:{pw}@{url}/{db}'.format(
                user=self.app.config['SQLALCHEMY_DATABASE_USER'],
                pw=self.app.config['SQLALCHEMY_DATABASE_PW'],
                url=self.app.config['SQLALCHEMY_DATABASE_HOST'],
                db=self.app.config['SQLALCHEMY_DATABASE_DB'])
        if database_type == 'postgresql':
            return 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
                user=self.app.config['SQLALCHEMY_DATABASE_USER'],
                pw=self.app.config['SQLALCHEMY_DATABASE_PW'],
                url=self.app.config['SQLALCHEMY_DATABASE_HOST'],
                db=self.app.config['SQLALCHEMY_DATABASE_DB'])
        if database_type == 'mysql':
            return 'mysql://{user}:{pw}@{url}/{db}'.format(
                user=self.app.config['SQLALCHEMY_DATABASE_USER'],
                pw=self.app.config['SQLALCHEMY_DATABASE_PW'],
                url=self.app.config['SQLALCHEMY_DATABASE_HOST'],
                db=self.app.config['SQLALCHEMY_DATABASE_DB'])
        return None

    def create_db(self):
        self.db.create_all()
        return self

    def __create_celery_broker_paths(self):
        broker_path = self.root_dir + os.sep + 'broker' + os.sep
        self.broker_out = broker_path + 'out'
        self.broker_procesed = broker_path + 'processed'
        for f in [self.broker_out, self.broker_procesed]:
            if not os.path.exists(f):
                os.makedirs(f)
        return self

    def create_celery(self):
        if sys.platform == 'linux':
            if self.root_dir.endswith("flask_covid19"):
                self.root_dir.replace(os.sep + 'flask_covid19', '')
            os.chdir(self.root_dir)
        else:
            os.chdir(self.root_dir)
        self.app.logger.info(os.getcwd())
        celery = Celery("flask_covid19_celery")
        self.__create_celery_broker_paths()
        celery.conf.update(self.app.config)
        if sys.platform == 'linux':
            self.broker_url = 'filesystem://'
            self.broker_transport_options = {
                'data_folder_in': self.broker_out,
                'data_folder_out': self.broker_out,
                'data_folder_processed': self.broker_procesed
            }
            self.conf_update = {
                'broker_url': self.broker_url,
                'broker_transport_options': self.broker_transport_options
            }
            celery.conf.update(self.conf_update)
        else:
            self.broker_url = 'filesystem://'
            self.broker_transport_options = {
                    'data_folder_in': self.broker_out,
                    'data_folder_out': self.broker_out,
                    'data_folder_processed': self.broker_procesed
                }
            self.conf_update = {
                'broker_url': self.broker_url,
                'broker_transport_options': self.broker_transport_options
            }
            celery.conf.update(self.conf_update)
        return celery


covid19_application = Covid19Application()
app = covid19_application.app
db = covid19_application.db
admin = covid19_application.admin
root_dir = covid19_application.root_dir
login_manager = covid19_application.login_manager
items_per_page = covid19_application.items_per_page
celery = covid19_application.create_celery()
