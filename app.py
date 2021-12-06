import flask_covid19.app_config
import flask_covid19.app_web
import flask_covid19.data_all
from flask_covid19.app_web import celery
from flask_covid19.app_web import run_web

# ---------------------------------------------------------------------------------
#  MAIN
# ---------------------------------------------------------------------------------

if __name__ == "__main__":
    run_web()
