from project.app_web import run_mq
from project.app_web.web_views import app
from project.app_web.web_views import celery

# Celery: https://docs.celeryproject.org/en/stable/userguide/index.html

# ---------------------------------------------------------------------------------
#  MAIN
# ---------------------------------------------------------------------------------

if __name__ == "__main__":
    run_mq()
