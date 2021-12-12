from app_web import run_mq
from app_web.web_views import app
from app_web.web_views import celery

# Celery: https://docs.celeryproject.org/en/stable/userguide/index.html

# ---------------------------------------------------------------------------------
#  MAIN
# ---------------------------------------------------------------------------------

if __name__ == "__main__":
    run_mq()
