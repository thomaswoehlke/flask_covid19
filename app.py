import click

import project.app_config
import project.app_web
import project.data_all
from project.app_web.web_dispachter_matrix_service import web_service
from project.app_web.web_dispachter_matrix_service import all_dispachter_matrix_service

from project.app_web.web_dispachter_matrix_service import who_service
from project.app_web.web_dispachter_matrix_service import owid_service
from project.app_web.web_dispachter_matrix_service import ecdc_service
from project.app_web.web_dispachter_matrix_service import vaccination_service
from project.app_web.web_dispachter_matrix_service import rki_service

from project.app_web import celery
from project.app_web import run_web
from project.app_web import app, db


def create_app():
    # run_web()
    return app


@app.cli.command("app-create-user")
def create_user():
    with app.app_context():
        db.create_all()
        # cache.clear()
        web_service.create_user(db)


@app.cli.command("all-download")
def all_download():
    with app.app_context():
        all_dispachter_matrix_service.download()


@app.cli.command("all-import")
def all_download():
    with app.app_context():
        all_dispachter_matrix_service.import_file()


@app.cli.command("all-update")
def all_full_update():
    with app.app_context():
        all_dispachter_matrix_service.update()


@app.cli.command("all-update-full")
def all_full_update():
    with app.app_context():
        all_dispachter_matrix_service.full_update()


@app.cli.command("all-delete-last-day")
def all_delete_last_day():
    with app.app_context():
        all_dispachter_matrix_service.delete_last_day()


@app.cli.command("who-download")
def who_download():
    with app.app_context():
        who_service.download()


@app.cli.command("who-import")
def who_import_file():
    with app.app_context():
        who_service.import_file()


@app.cli.command("who-update")
def who_full_update():
    with app.app_context():
        who_service.full_update()


@app.cli.command("who-update-full")
def who_update():
    with app.app_context():
        who_service.update()


@app.cli.command("who-delete-last-day")
def who_delete_last_day():
    with app.app_context():
        who_service.delete_last_day()


@app.cli.command("owid-download")
def owid_download():
    with app.app_context():
        owid_service.download()


@app.cli.command("owid-import")
def owid_import_file():
    with app.app_context():
        owid_service.import_file()


@app.cli.command("owid-update-full")
def owid_full_update():
    with app.app_context():
        owid_service.full_update()


@app.cli.command("owid-update")
def owid_update():
    with app.app_context():
        owid_service.update()


@app.cli.command("owid-delete-last-day")
def owid_delete_last_day():
    with app.app_context():
        owid_service.delete_last_day()


# ---------------------------------------------------------------------------------
#  MAIN
# ---------------------------------------------------------------------------------

if __name__ == "__main__":
    run_web()
