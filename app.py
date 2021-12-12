import click

import project.app_config
import project.app_web
import project.data_all
from project.app_web.web_dispachter_matrix_service import web_service
from project.app_web import celery
from project.app_web import run_web
from project.app_web import app, db


def create_app():
    # run_web()
    return app


@app.cli.command("create-user")
def create_user():
    with app.app_context():
        db.create_all()
        # cache.clear()
        web_service.create_user(db)

# ---------------------------------------------------------------------------------
#  MAIN
# ---------------------------------------------------------------------------------

if __name__ == "__main__":
    run_web()
