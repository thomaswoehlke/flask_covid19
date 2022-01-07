import os
import string
import subprocess

from pandas import Index

from project.app_bootstrap.database import app, db
from project.app_web.user.user_model import User
from project.data_all.task.all_task_model import Task
from project.data_ecdc.model.ecdc_model import EcdcDateReported
from project.data_ecdc.model.ecdc_model_data import EcdcData
from project.data_ecdc.model.ecdc_model_import import EcdcImport
from project.data_ecdc.model.ecdc_model_location import EcdcCountry
from project.data_ecdc.model.ecdc_model_location_group import EcdcContinent
from project.data_owid.model.owid_model_data import OwidData
from project.data_owid.model.owid_model_date_reported import OwidDateReported
from project.data_owid.model.owid_model_import import OwidImport
from project.data_owid.model.owid_model_location import OwidCountry
from project.data_owid.model.owid_model_location_group import OwidContinent
from project.data_rki.model.rki_model_altersgruppe import RkiAltersgruppe
from project.data_rki.model.rki_model_data import RkiData
from project.data_rki.model.rki_model_data_location_group import RkiBundesland
from project.data_rki.model.rki_model_date_reported import RkiMeldedatum
from project.data_rki.model.rki_model_import import RkiImport
from project.data_vaccination.model.vaccination_model_data import VaccinationData
from project.data_vaccination.model.vaccination_model_date_reported import (
    VaccinationDateReported,
)
from project.data_vaccination.model.vaccination_model_import import VaccinationImport
from project.data_who.model.who_model_data import WhoData
from project.data_who.model.who_model_date_reported import WhoDateReported
from project.data_who.model.who_model_import import WhoImport
from project.data_who.model.who_model_location import WhoCountry
from project.data_who.model.who_model_location_group import WhoCountryRegion

from project.data_owid.services.owid_service import OwidService
from project.data_rki.services.rki_service import RkiService
from project.data_ecdc.services.ecdc_service import EcdcService
from project.data_vaccination.services.vaccination_service import VaccinationService
from project.data_who.services.who_service import WhoService

import pandas as pd


owid_service = OwidService(db)
rki_service = RkiService(db)
ecdc_service = EcdcService(db)
vaccination_service = VaccinationService(db)
who_service = WhoService(db)

class AdminService:
    def __init__(self, database):
        app.logger.debug("-----------------------------------------------------------")
        app.logger.debug(" Admin Service [init]")
        app.logger.debug("-----------------------------------------------------------")
        self.__database = database
        self.limit_nr = 20
        self.file_path_parent = "data" + os.sep + "db"
        self.file_path = self.file_path_parent + os.sep + "flask_covid19.sql"
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info(" ready: [app_web] Admin Service ")

    def database_dump(self):
        app.logger.info(" AdminService.database_dump() [begin]")
        app.logger.info("-----------------------------------------------------------")
        app.logger.info(os.getcwd())
        user = app.config["SQLALCHEMY_DATABASE_USER"]
        pwd = app.config["SQLALCHEMY_DATABASE_PW"]
        url = app.config["SQLALCHEMY_DATABASE_HOST"]
        db = app.config["SQLALCHEMY_DATABASE_DB"]
        db_type = app.config["SQLALCHEMY_DATABASE_TYPE"]
        cmd = "mkdir -p " + self.file_path_parent
        app.logger.info(" start: " + str(cmd))
        returncode = self.__run_ome_shell_command(cmd)
        app.logger.info(" result: " + str(returncode))
        if db_type == "postgresql":
            cmd = (
                "pg_dump --if-exists --clean --no-tablespaces "
                + " --on-conflict-do-nothing --rows-per-insert=1000 --column-inserts "
                + " --quote-all-identifiers --no-privileges -U "
                + user
                + " -h "
                + url
                + " "
                + db
                + " > "
                + self.file_path
            )
        if db_type == "mariadb":
            cmd = (
                "mysqldump -h "
                + url
                + " -u "
                + user
                + ' --password="'
                + pwd
                + '" '
                + db
                + " > "
                + self.file_path
            )
        app.logger.info(" start: " + str(cmd))
        returncode = self.__run_ome_shell_command(cmd)
        app.logger.info(" result: " + str(returncode))
        app.logger.info(" AdminService.database_dump() [done]")
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
            app.logger.warning("  WARN:  AdminService.__run_ome_shell_command")
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
        app.logger.info(" AdminService.database_dump_reimport() [begin]")
        app.logger.info("-----------------------------------------------------------")
        user = app.config["SQLALCHEMY_DATABASE_USER"]
        url = app.config["SQLALCHEMY_DATABASE_HOST"]
        db = app.config["SQLALCHEMY_DATABASE_DB"]
        db_type = app.config["SQLALCHEMY_DATABASE_TYPE"]
        one_cmd = ""
        if db_type == "postgresql":
            one_cmd = (
                "psql -U " + user + " -h " + url + " " + db + " < " + self.file_path
            )
        if db_type == "mariadb":
            one_cmd = (
                "mysql -h " + url + " -u " + user + " " + db + " < " + self.file_path
            )
        cmd_list = [one_cmd]
        for cmd in cmd_list:
            returncode = self.__run_ome_shell_command(cmd)
            msg = "[ returncode: " + str(returncode) + "] " + cmd
            app.logger.info(msg)
        app.logger.info(" AdminService.database_dump_reimport() [done]")
        app.logger.info("-----------------------------------------------------------")
        return self

    def database_drop_and_create(self):
        app.logger.info(" AdminService.database_drop_and_create() [begin]")
        app.logger.info("-----------------------------------------------------------")
        with app.app_context():
            self.__database.drop_all()
            self.__database.create_all()
        app.logger.info("")
        app.logger.info(" AdminService.database_drop_and_create() [begin]")
        app.logger.info("-----------------------------------------------------------")
        return self

    def database_table_row_count(self):
        app.logger.info(" AdminService.database_table_row_count() [begin]")
        app.logger.info("-----------------------------------------------------------")
        table_classes = [
            WhoData,
            WhoImport,
            WhoCountryRegion,
            WhoCountry,
            OwidData,
            OwidImport,
            OwidCountry,
            OwidContinent,
            EcdcData,
            EcdcImport,
            EcdcCountry,
            EcdcContinent,
            VaccinationData,
            VaccinationImport,
            RkiData,
            RkiImport,
            RkiAltersgruppe,
            RkiBundesland,
            Task,
            User,
            WhoDateReported,
            OwidDateReported,
            VaccinationDateReported,
            RkiMeldedatum,
            EcdcDateReported,
        ]
        table_classes.sort(key=str)
        tables_and_rows = {}
        with app.app_context():
            for table_class in table_classes:
                key = table_class.__name__
                tables_and_rows[key] = table_class.count()
                a = 30 - len(key)
                b = 7 - len(str(tables_and_rows[key]))
                msg = " | " + key
                for i in range(a):
                    msg += " "
                msg += " | "
                for i in range(b):
                    msg += " "
                msg += str(tables_and_rows[key]) + " | "
                app.logger.info(msg)
        app.logger.info("")
        app.logger.info(" AdminService.database_table_row_count() [begin]")
        app.logger.info("------------------------------------------------------------")
        return tables_and_rows

    def database_import_status(self):
        app.logger.info(" AdminService.database_import_status() [begin]")
        app.logger.info("-----------------------------------------------------------")
        with app.app_context():
            t = {
                'WHO': {
                    'data_class': WhoData.__name__,
                    'import_class': WhoImport.__name__,
                    'data_count': WhoData.count(),
                    'import_count': WhoImport.count(),
                    'file_count': who_service.count_file_rows()
                },
                'OWID': {
                    'data_class': OwidData.__name__,
                    'import_class': OwidImport.__name__,
                    'data_count': OwidData.count(),
                    'import_count': OwidImport.count(),
                    'file_count': owid_service.count_file_rows()
                },
                'ECDC': {
                    'data_class': EcdcData.__name__,
                    'import_class': EcdcImport.__name__,
                    'data_count': EcdcData.count(),
                    'import_count': EcdcImport.count(),
                    'file_count': ecdc_service.count_file_rows()
                },
                'Vaccination': {
                    'data_class': VaccinationData.__name__,
                    'import_class': VaccinationImport.__name__,
                    'data_count': VaccinationData.count(),
                    'import_count': VaccinationImport.count(),
                    'file_count': vaccination_service.count_file_rows()
                },
                'RKI': {
                    'data_class': RkiData.__name__,
                    'import_class': RkiImport.__name__,
                    'data_count': RkiData.count(),
                    'import_count': RkiImport.count(),
                    'file_count': rki_service.count_file_rows()
                }
            }
            df = pd.DataFrame.from_dict(t, orient='index')
            app.logger.info(df)
        app.logger.info("")
        app.logger.info(" AdminService.database_import_status() [done]")
        app.logger.info("------------------------------------------------------------")
        return t
