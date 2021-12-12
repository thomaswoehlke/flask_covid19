import os
import socket
import subprocess
from operator import eq

import project.app_config
import project.app_web
import project.data_all
from project.app_web.web_dispachter_matrix_service import web_service
from project.app_web.web_views import app
from project.app_web.web_views import celery
from project.app_web.web_views import db


def run_web():
    with app.app_context():
        db.create_all()
        # cache.clear()
        web_service.prepare_run_web(db)
        app.logger.info(os.getcwd())
        debug = app.config["FLASK_APP_DEBUGGER_ACTIVE"]
        port = app.config["PORT"]
        # host = app.config['HOST']
        # if host == None or host == '':
        host = socket.gethostname()
        app.logger.info(host)
        load_dotenv = True
        app.run(host=host, port=port, debug=debug, load_dotenv=load_dotenv)


def run_mq():
    with app.app_context():
        db.create_all()
        # cache.clear()
        web_service.prepare_run_mq(db)
        app.logger.info(os.getcwd())
        my_cmds = ["celery --app app.celery worker --pool eventlet --loglevel INFO"]
        for my_cmd in my_cmds:
            app.logger.info(my_cmd)
            subprocess.call(my_cmd, shell=True)