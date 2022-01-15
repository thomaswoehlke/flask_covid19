import os

from project.data.database import app, db
from project.data_all_notifications.notifications_model import Notification
from project.data_ecdc.model.ecdc_model_data import EcdcData
from project.data_ecdc.model.ecdc_model_date_reported import EcdcDateReported
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
from project.data_vaxx.model.vaxx_model_data import VaccinationData
from project.data_vaxx.model.vaxx_model_date_reported import \
    VaccinationDateReported
from project.data_vaxx.model.vaxx_model_import import VaccinationImport
from project.data_who.model.who_model_data import WhoData
from project.data_who.model.who_model_date_reported import WhoDateReported
from project.data_who.model.who_model_import import WhoImport
from project.data_who.model.who_model_location import WhoCountry
from project.data_who.model.who_model_location_group import WhoCountryRegion
from project.web_user.user_model import WebUser


class DatabaseTableRowCountService:

    def __init__(self, database):
        self.__database = database
        self.limit_nr = 20
        self.file_path_parent = "data" + os.sep + "db"
        self.file_path = self.file_path_parent + os.sep + "flask_covid19.sql"
        app.logger.info(" ready: [web] Admin Service ")

    def database_table_row_count(self):
        app.logger.info(
            " DatabaseTableRowCountService.database_table_row_count() [begin]")
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
            Notification,
            WebUser,
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
        app.logger.info(
            " DatabaseTableRowCountService.database_table_row_count() [begin]"
        )
        app.logger.info("------------------------------------------------------------")
        return tables_and_rows
