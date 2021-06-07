import flask_covid19
import flask_covid19_web
import flask_covid19_mq

from flask_covid19.blueprints.app_web.web_views import celery
from flask_covid19_mq import run_mq

# Celery: https://docs.celeryproject.org/en/stable/userguide/index.html

# ---------------------------------------------------------------------------------
#  MAIN
# ---------------------------------------------------------------------------------

if __name__ == '__main__':
    run_mq()
