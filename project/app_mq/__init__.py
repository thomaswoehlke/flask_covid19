import os
import subprocess

from app_web.web_dispachter_matrix_service import web_service
from app_web.web_views import app
from app_web.web_views import celery


def run_mq():
    web_service.prepare_run_mq()
    # with app.app_context():
    #    cache.clear()
    # start_redis()
    # args = ['worker']
    # celery.start(args)
    app.logger.info(os.getcwd())
    my_cmds = ["celery --app mq.celery worker --pool eventlet --loglevel INFO"]
    for my_cmd in my_cmds:
        retcode = subprocess.call(my_cmd, shell=True)
