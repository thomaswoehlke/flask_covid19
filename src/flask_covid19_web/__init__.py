import os
from flask_covid19.blueprints.app_web.web_dispachter_matrix_service import web_service
from flask_covid19.blueprints.app_web.web_views import app, celery # , cache


def run_web():
    web_service.prepare_run_web()
    app.logger.info(os.getcwd())
    debug = app.config['FLASK_APP_DEBUGGER_ACTIVE']
    port = app.config['PORT']
    host = None
    load_dotenv = True
    app.run(
        host=host,
        port=port,
        debug=debug,
        load_dotenv=load_dotenv
    )
