import os
import sys

from flask import Flask, Blueprint
# from flask_caching import Cache
from flask_cors import CORS
from flask_bs4 import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from logging.config import dictConfig
from flask_admin import Admin
from celery import Celery

# https://flask-caching.readthedocs.io/en/latest/
# https://www.howtoforge.de/anleitung/wie-installiere-ich-memcached-auf-ubuntu-2004-lts/

cache_config_simple = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 120,
    "CACHE_KEY_PREFIX": 'flask_covid19_'
}

cache_config_MemcachedCache = {
    "DEBUG": True,
    "CACHE_TYPE": "MemcachedCache",
    "CACHE_MEMCACHED_SERVERS": "127.0.0.1:11211",
    "CACHE_DEFAULT_TIMEOUT": 120,
    "CACHE_KEY_PREFIX": 'flask_covid19_'
}

#cache = Cache()
app_cors = CORS()
app_bootstrap = Bootstrap()
login_manager = LoginManager()


def create_app():
    my_app = Flask('covid19')
    app_cors.init_app(my_app)
    app_bootstrap.init_app(my_app)
    login_manager.login_view = 'usr.login'
    login_manager.init_app(my_app)
    my_app.config.from_object("config")
    # my_db_url = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    # my_db_url = 'mysql://{user}:{pw}@{url}/{db}'.format(
    my_db_url = 'mariadb+mariadbconnector://{user}:{pw}@{url}/{db}'.format(
        user=my_app.config['SQLALCHEMY_DATABASE_USER'],
        pw=my_app.config['SQLALCHEMY_DATABASE_PW'],
        url=my_app.config['SQLALCHEMY_DATABASE_HOST'],
        db=my_app.config['SQLALCHEMY_DATABASE_DB'])
    my_app.config['SQLALCHEMY_DATABASE_URI'] = my_db_url
    my_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning
    my_app.config['FLASK_ADMIN_SWATCH'] = 'superhero'
    # cache.init_app(my_app, config=cache_config_MemcachedCache)
    # with my_app.app_context():
    #    cache.clear()
    return my_app


def create_db(my_app):
    my_db = SQLAlchemy(my_app)
    my_db.create_all()
    return my_db


def create_db_test(my_app):
    my_db = SQLAlchemy(my_app)
    my_db.create_all()
    return my_db


def create_admin(my_app):
    my_admin = Admin(
        my_app,
        name='covid19 | admin',
        template_mode='bootstrap4')
    return my_admin


def create_celery():
    root_dir = os.getcwd()
    if sys.platform == 'linux':
        if root_dir.endswith("src"):
            root_dir.replace(os.sep + 'src', '')
    os.chdir(root_dir)
    app.logger.info(os.getcwd())
    celery = Celery("flask_covid19_celery")
    #   app.import_name,
    #    backend=app.config['MY_CELERY_RESULT_BACKEND'],
    #    broker=app.config['CELERY_BROKER_URL'],
    #    worker_send_task_events=app.config['CELERY_CONF_WORKER_SEND_TASK_EVENTS'],
    #    task_send_sent_event=app.config['CELERY_CONF_TASK_SEND_SENT_EVENT'],
    #    broker_transport_options={'visibility_timeout': 18000, 'max_retries': 5},
    #    set_as_current=False,
    #    standalone_mode=True
    #)
    # setup folder for message broking
    for f in ['./broker/out', './broker/processed']:
        if not os.path.exists(f):
            os.makedirs(f)
    celery.conf.update(app.config)
    celery.conf.update({
        'broker_url': 'filesystem://',
        'broker_transport_options': {
            'data_folder_in': './broker/out',
            'data_folder_out': './broker/out',
            'data_folder_processed': './broker/processed'
        }})
    #class ContextTask(celery.Task):
    #    def __call__(self, *args, **kwargs):
    #        with app.app_context():
    #            return self.run(*args, **kwargs)
    #
    #celery.Task = ContextTask
    return celery

my_logging_config = {
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
dictConfig(my_logging_config)


app = create_app()
db = create_db(app)
admin = create_admin(app)
celery = create_celery()
root_dir = os.getcwd()

#if root_dir.endswith(os.sep + 'src'):
#    root_dir = root_dir.replace(os.sep + 'src', '')

# TODO: #209 remove deprecated database.ITEMS_PER_PAGE
ITEMS_PER_PAGE = app.config['SQLALCHEMY_ITEMS_PER_PAGE']
