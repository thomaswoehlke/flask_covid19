import os
import subprocess
import pandas as pd

from project.data.database import app, db


class WebAdminService:

    def __init__(self, database):
        self.__database = database
        self.limit_nr = 20
        self.file_path_parent = "data" + os.sep + "db"
        self.file_path = self.file_path_parent + os.sep + "flask_covid19.sql"
        app.logger.info(" ready: [web] Admin Service ")

    def database_dump(self):
        app.logger.info("-----------------------------------------------------------")
        app.logger.info(" WebAdminService.database_dump() [begin]")
        app.logger.info("-----------------------------------------------------------")
        app.logger.info(os.getcwd())
        user = app.config["SQLALCHEMY_DATABASE_USER"]
        pwd = app.config["SQLALCHEMY_DATABASE_PW"]
        url = app.config["SQLALCHEMY_DATABASE_HOST"]
        database = app.config["SQLALCHEMY_DATABASE_DB"]
        db_type = app.config["SQLALCHEMY_DATABASE_TYPE"]
        cmd = "mkdir -p " + self.file_path_parent
        app.logger.info(" start: " + str(cmd))
        returncode = self.__run_ome_shell_command(cmd)
        app.logger.info(" result: " + str(returncode))
        if db_type == "postgresql":
            cmd = (
                "pg_dump --if-exists --clean --no-tablespaces "
                + " --on-conflict-do-nothing --rows-per-insert=1000 --column-inserts "
                + " --quote-all-identifiers --no-privileges"
                + " -U {} -h {} {} > {}".format(
                    user,
                    url,
                    database,
                    self.file_path
                )
            )

        if db_type == "mariadb":
            cmd = (
                'mysqldump -h {} -u {} --password="{}" {} > {}'.format(
                    url,
                    user,
                    pwd,
                    database,
                    self.file_path
                )
            )
        app.logger.info(" start: " + str(cmd))
        returncode = self.__run_ome_shell_command(cmd)
        app.logger.info(" result: " + str(returncode))
        app.logger.info("-----------------------------------------------------------")
        app.logger.info(" WebAdminService.database_dump() [done]")
        app.logger.info("-----------------------------------------------------------")
        return self

    @classmethod
    def __run_ome_shell_command(cls, cmd):
        args = [cmd]
        app.logger.info(" start: " + str(cmd))
        returncode = 0
        try:
            result = subprocess.run(
                args, shell=True, check=True, capture_output=True, encoding="UTF-8"
            )
            returncode = result.returncode
        except subprocess.CalledProcessError as error:
            app.logger.warning(
                "---------------------------------------------------------"
            )
            app.logger.warning("  WARN:  WebAdminService.__run_ome_shell_command")
            app.logger.warning(
                "---------------------------------------------------------"
            )
            app.logger.warning("  cmd:    :::" + cmd + ":::")
            app.logger.warning("  erro:   :::" + str(error) + ":::")
            app.logger.warning(
                "---------------------------------------------------------"
            )
        return returncode

    def database_dump_reimport(self):
        app.logger.info(" WebAdminService.database_dump_reimport() [begin]")
        app.logger.info("-----------------------------------------------------------")
        user = app.config["SQLALCHEMY_DATABASE_USER"]
        url = app.config["SQLALCHEMY_DATABASE_HOST"]
        database = app.config["SQLALCHEMY_DATABASE_DB"]
        db_type = app.config["SQLALCHEMY_DATABASE_TYPE"]
        one_cmd = ""
        if db_type == "postgresql":
            one_cmd = (
                "psql -U {} -h {} {} < {}".format(
                    user,
                    url,
                    database,
                    self.file_path
                )
            )
        if db_type == "mariadb":
            one_cmd = (
                "mysql -h {} -u {} {} < {}".format(
                    url,
                    user,
                    database,
                    self.file_path
                )
            )
        cmd_list = [one_cmd]
        for cmd in cmd_list:
            returncode = self.__run_ome_shell_command(cmd)
            msg = "[ returncode: {} ] {}".format(
                str(returncode),
                cmd
            )
            app.logger.info(msg)
        app.logger.info(" WebAdminService.database_dump_reimport() [done]")
        app.logger.info("-----------------------------------------------------------")
        return self

    def database_drop_and_create(self):
        app.logger.info(" WebAdminService.database_drop_and_create() [begin]")
        app.logger.info("-----------------------------------------------------------")
        with app.app_context():
            self.__database.drop_all()
            self.__database.create_all()
        app.logger.info("")
        app.logger.info(" WebAdminService.database_drop_and_create() [begin]")
        app.logger.info("-----------------------------------------------------------")
        return self
