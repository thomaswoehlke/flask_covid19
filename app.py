import flask_covid19.data_all
import flask_covid19.app_config
import flask_covid19.app_web

from flask_covid19.app_web import run_web, celery

# ---------------------------------------------------------------------------------
#  MAIN
# ---------------------------------------------------------------------------------

if __name__ == '__main__':
    run_web()
