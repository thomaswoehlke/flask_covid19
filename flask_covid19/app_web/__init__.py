from operator import eq
import os
import socket
import subprocess
import data_all
import app_config
import app_web

from app_web.web_dispachter_matrix_service import web_service
from app_web.web_views import app, celery, db   # , cache


def run_web():
    with app.app_context():
        db.create_all()
        # cache.clear()
        web_service.prepare_run_web(db)
        app.logger.info(os.getcwd())
        debug = app.config['FLASK_APP_DEBUGGER_ACTIVE']
        port = app.config['PORT']
        #host = app.config['HOST']
        #if host == None or host == '':
        host = socket.gethostname()
        app.logger.info(host)
        load_dotenv = True
        app.run(
            host=host,
            port=port,
            debug=debug,
            load_dotenv=load_dotenv
        )


def run_mq():
    with app.app_context():
        db.create_all()
        # cache.clear()
        web_service.prepare_run_mq(db)
        app.logger.info(os.getcwd())
        my_cmds = ['celery --app app.celery worker --pool eventlet --loglevel INFO']
        for my_cmd in my_cmds:
            app.logger.info(my_cmd)
            subprocess.call(my_cmd, shell=True)
