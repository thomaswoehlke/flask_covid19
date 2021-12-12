import project.app_config
import project.app_web
import project.data_all
from project.app_web import celery
from project.app_web import run_web
from project.app_web import app


def create_app():
    return app


# ---------------------------------------------------------------------------------
#  MAIN
# ---------------------------------------------------------------------------------

if __name__ == "__main__":
    run_web()
