import os
import socket
import subprocess

from app_web.web_dispachter_matrix_service import web_service
from app_web.web_views import app, celery  # , cache


def run_web():
    web_service.prepare_run_web()
    app.logger.info(os.getcwd())
    debug = app.config['FLASK_APP_DEBUGGER_ACTIVE']
    port = app.config['PORT']
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
    web_service.prepare_run_mq()
    #with app.app_context():
    #    cache.clear()
    # start_redis()
    # args = ['worker']
    # celery.start(args)
    app.logger.info(os.getcwd())
    my_cmds = ['celery worker --app=mq.celery --pool=eventlet --loglevel=INFO']
    for my_cmd in my_cmds:
        retcode = subprocess.call(my_cmd, shell=True)
