import sys
import os
import subprocess

from flask_covid19.blueprints.app_web.web_dispachter_matrix_service import web_service
from flask_covid19.blueprints.app_web.web_views import app, celery # , cache


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
