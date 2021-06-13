from app_web.web_views import app, celery
from flask_covid19_mq import run_mq

# Celery: https://docs.celeryproject.org/en/stable/userguide/index.html

# ---------------------------------------------------------------------------------
#  MAIN
# ---------------------------------------------------------------------------------

if __name__ == '__main__':
    run_mq()
