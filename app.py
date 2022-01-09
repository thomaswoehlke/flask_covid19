from project.app_web import app, db, run_web, celery
from project.app_web.web.web_dispachter_service import all_dispachter_matrix_service
from project.app_web.web.web_dispachter_service import app_admin_service
from project.app_web.web.web_dispachter_service import ecdc_service
from project.app_web.web.web_dispachter_service import owid_service
from project.app_web.web.web_dispachter_service import rki_service
from project.app_web.web.web_dispachter_service import vaccination_service
from project.app_web.web.web_dispachter_service import web_service
from project.app_web.web.web_dispachter_service import who_service
from project.app_web.web.web_dispachter_service import task_service


def create_app():
    # run_web()
    return app


@app.cli.command("db-create-user")
def create_user():
    """[Admin] create user"""
    with app.app_context():
        db.create_all()
        web_service.create_user(db)


@app.cli.command("all-download")
def all_download():
    """[ALL] download"""
    with app.app_context():
        all_dispachter_matrix_service.download()


@app.cli.command("all-import")
def all_import():
    """[ALL] import file"""
    with app.app_context():
        all_dispachter_matrix_service.import_file()


@app.cli.command("all-update")
def all_update():
    """[ALL] update"""
    with app.app_context():
        all_dispachter_matrix_service.update()


@app.cli.command("all-update-full")
def all_full_update():
    """[ALL] full update"""
    with app.app_context():
        all_dispachter_matrix_service.full_update()


@app.cli.command("all-update-full-dimensions")
def all_full_update_dimension_tables():
    """[ALL] full update dimension tables"""
    with app.app_context():
        all_dispachter_matrix_service.full_update_dimension_tables()


@app.cli.command("all-update-dimensions")
def all_update_dimension_tables():
    """[ALL] update dimension tables"""
    with app.app_context():
        all_dispachter_matrix_service.update_dimension_tables()


@app.cli.command("all-update-full-data")
def all_full_update_fact_table():
    """[ALL] full update fact table"""
    with app.app_context():
        all_dispachter_matrix_service.full_update_fact_table()


@app.cli.command("all-update-data")
def all_update_fact_table():
    """[ALL] full update fact table"""
    with app.app_context():
        all_dispachter_matrix_service.update_fact_table()


@app.cli.command("who-download")
def who_download():
    """[WHO] download"""
    with app.app_context():
        who_service.download()


@app.cli.command("who-import")
def who_import_file():
    """[WHO] import file"""
    with app.app_context():
        who_service.import_file()


@app.cli.command("who-update-full")
def who_full_update():
    """[WHO] full update"""
    with app.app_context():
        who_service.full_update()
    app.logger.info("------------------------------------------------------------")
    app.logger.info(" [WHO] who-update-full [done]")
    app.logger.info("------------------------------------------------------------")
    pass


@app.cli.command("who-update")
def who_update():
    """[WHO] update"""
    with app.app_context():
        who_service.update()


@app.cli.command("who-delete-last-day")
def who_delete_last_day():
    """[WHO] delete last day"""
    with app.app_context():
        who_service.delete_last_day()


@app.cli.command("ecdc-download")
def ecdc_download():
    """[ECDC] download"""
    with app.app_context():
        ecdc_service.download()


@app.cli.command("ecdc-import")
def ecdc_import_file():
    """[ECDC] import file"""
    with app.app_context():
        ecdc_service.import_file()


@app.cli.command("ecdc-update-full")
def ecdc_full_update():
    """[ECDC] full update"""
    with app.app_context():
        ecdc_service.full_update()


@app.cli.command("owid-download")
def owid_download():
    """[OWID] download"""
    with app.app_context():
        owid_service.download()


@app.cli.command("owid-import")
def owid_import_file():
    """[OWID] import file"""
    with app.app_context():
        owid_service.import_file()


@app.cli.command("owid-update-full")
def owid_full_update():
    """[OWID] full update"""
    with app.app_context():
        owid_service.full_update()


@app.cli.command("owid-update")
def owid_update():
    """[OWID] update"""
    with app.app_context():
        owid_service.update()


@app.cli.command("owid-delete-last-day")
def owid_delete_last_day():
    """[OWID] delete last day"""
    with app.app_context():
        owid_service.delete_last_day()


@app.cli.command("rki-download")
def rki_download():
    """[RKI] download"""
    with app.app_context():
        rki_service.download()


@app.cli.command("rki-import")
def rki_import_file():
    """[RKI] import file"""
    with app.app_context():
        rki_service.import_file()


@app.cli.command("rki-update-full")
def rki_full_update():
    """[RKI] full update"""
    with app.app_context():
        rki_service.full_update()


@app.cli.command("rki-update")
def rki_update():
    """[RKI] update"""
    with app.app_context():
        rki_service.update()


@app.cli.command("rki-update-clean-brokenup")
def rki_update_clean_brokenup():
    """[RKI] update clean brokenup"""
    with app.app_context():
        rki_service.update_clean_brokenup()


@app.cli.command("rki-delete-last-day")
def rki_delete_last_day():
    """[RKI] delete last day"""
    with app.app_context():
        rki_service.delete_last_day()


@app.cli.command("rki-update-full-dimensions")
def rki_full_update_dimension_tables():
    """[RKI] full update dimension tables"""
    with app.app_context():
        rki_service.full_update_dimension_tables()


@app.cli.command("rki-update-dimensions")
def rki_update_dimension_tables():
    """[RKI] update dimension tables"""
    with app.app_context():
        rki_service.update_dimension_tables()


@app.cli.command("rki-update-full-data")
def rki_full_update_fact_table():
    """[RKI] full update fact table"""
    with app.app_context():
        rki_service.full_update_fact_table()


@app.cli.command("rki-update-data")
def rki_update_fact_table():
    """[RKI] update fact table"""
    with app.app_context():
        rki_service.update_fact_table()


@app.cli.command("vaccination-download")
def vaccination_download():
    """[vaccination] download"""
    with app.app_context():
        vaccination_service.download()


@app.cli.command("vaccination-import")
def vaccination_import_file():
    """[vaccination] import file"""
    with app.app_context():
        vaccination_service.import_file()


@app.cli.command("vaccination-update-full")
def vaccination_full_update():
    """[vaccination] full update"""
    with app.app_context():
        vaccination_service.full_update()


@app.cli.command("db-dump")
def admin_database_dump():
    """[Admin] database dump"""
    with app.app_context():
        app_admin_service.database_dump()


@app.cli.command("db-dump-reimport")
def admin_database_dump_reimport():
    """[Admin] database dump reimport"""
    with app.app_context():
        app_admin_service.database_dump_reimport()


@app.cli.command("db-drop-and-create")
def admin_database_drop_and_create():
    """[Admin] database drop and create"""
    with app.app_context():
        app_admin_service.database_drop_and_create()


@app.cli.command("db-count")
def admin_database_table_row_count():
    """[Admin] database table row count"""
    with app.app_context():
        app_admin_service.database_table_row_count()


@app.cli.command("db-import-status")
def admin_database_import_status():
    """[Admin] database import-status"""
    with app.app_context():
        app_admin_service.database_import_status()


@app.cli.command("all-notifications-count")
def all_task_notifications_count():
    """[ALL] task notifications count"""
    with app.app_context():
        nr = task_service.notifications_count()
        app.logger.info("task notifications count: " + str(nr))


@app.cli.command("all-notifications-list")
def all_task_notifications_find():
    """[ALL] task notifications find"""
    app.logger.info("task notifications find: ")
    with app.app_context():
        for task in task_service.notifications_find():
            app.logger.info(str(task))


# ---------------------------------------------------------------------------------
#  MAIN
# ---------------------------------------------------------------------------------

if __name__ == "__main__":
    run_web()
