import flask_covid19_app_all
import flask_covid19_app_web
import flask_covid19_app
import flask_covid19_web
import flask_covid19_mq

from flask_covid19_web import run_web

# ---------------------------------------------------------------------------------
#  MAIN
# ---------------------------------------------------------------------------------

if __name__ == '__main__':
    run_web()
