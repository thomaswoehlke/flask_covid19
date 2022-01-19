import os
import subprocess
import pandas as pd

from project.data.database import app, db
from project.data_ecdc.ecdc_views import ecdc_service
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
from project.data_owid.owid_views import owid_service
from project.data_rki.model.rki_model_altersgruppe import RkiAltersgruppe
from project.data_rki.model.rki_model_data import RkiData
from project.data_rki.model.rki_model_location import RkiLandkreis
from project.data_rki.model.rki_model_location_group import RkiBundesland
from project.data_rki.model.rki_model_date_reported import RkiMeldedatum
from project.data_rki.model.rki_model_import import RkiImport
from project.data_rki.rki_views import rki_service
from project.data_vaxx.model.vaxx_model_data import VaccinationData
from project.data_vaxx.model.vaxx_model_date_reported import VaccinationDateReported
from project.data_vaxx.model.vaxx_model_import import VaccinationImport
from project.data_vaxx.vaxx_views import vaccination_service
from project.data_who.model.who_model_data import WhoData
from project.data_who.model.who_model_date_reported import WhoDateReported
from project.data_who.model.who_model_import import WhoImport
from project.data_who.model.who_model_location import WhoCountry
from project.data_who.model.who_model_location_group import WhoCountryRegion
from project.data_who.who_views import who_service


class DatabaseImportStatusService:

    def __init__(self, database):
        self.__database = database
        self.limit_nr = 20
        app.logger.info(" ready: [web] Admin Service ")

    def database_import_status(self):
        app.logger.info(" WebAdminService.database_import_status() [begin]")
        app.logger.info("-----------------------------------------------------------")
        with app.app_context():
            t = {
                'WHO': {
                    'file_datum': who_service.get_file_date(),
                    'file_count': who_service.count_file_rows(),
                    'import_class': WhoImport.__name__,
                    'import_class_count': WhoImport.count(),
                    'date_reported': WhoDateReported.__name__,
                    'date_reported_count': WhoDateReported.count(),
                    'location': WhoCountry.__name__,
                    'location_count': WhoCountry.count(),
                    'location_group': WhoCountryRegion.__name__,
                    'location_group_count': WhoCountryRegion.count(),
                    'data_class': WhoData.__name__,
                    'data_class_count': WhoData.count(),
                },
                'OWID': {
                    'file_datum': owid_service.get_file_date(),
                    'file_count': owid_service.count_file_rows(),
                    'import_class': OwidImport.__name__,
                    'import_class_count': OwidImport.count(),
                    'date_reported': OwidDateReported.__name__,
                    'date_reported_count': OwidDateReported.count(),
                    'location': OwidCountry.__name__,
                    'location_count': OwidCountry.count(),
                    'location_group': OwidContinent.__name__,
                    'location_group_count': OwidContinent.count(),
                    'data_class': OwidData.__name__,
                    'data_class_count': OwidData.count(),
                },
                'ECDC': {
                    'file_datum': ecdc_service.get_file_date(),
                    'file_count': ecdc_service.count_file_rows(),
                    'data_class': EcdcData.__name__,
                    'data_class_count': EcdcData.count(),
                    'date_reported': EcdcDateReported.__name__,
                    'date_reported_count': EcdcDateReported.count(),
                    'location': EcdcCountry.__name__,
                    'location_count': EcdcCountry.count(),
                    'location_group': EcdcContinent.__name__,
                    'location_group_count': EcdcContinent.count(),
                    'import_class': EcdcImport.__name__,
                    'import_class_count': EcdcImport.count(),
                },
                'Vaccination': {
                    'file_datum': vaccination_service.get_file_date(),
                    'file_count': vaccination_service.count_file_rows(),
                    'import_class': VaccinationImport.__name__,
                    'import_class_count': VaccinationImport.count(),
                    'date_reported': VaccinationDateReported.__name__,
                    'date_reported_count': VaccinationDateReported.count(),
                    'data_class': VaccinationData.__name__,
                    'data_class_count': VaccinationData.count(),
                },
                'RKI': {
                    'file_datum': rki_service.get_file_date(),
                    'file_count': rki_service.count_file_rows(),
                    'import_class': RkiImport.__name__,
                    'import_class_count': RkiImport.count(),
                    'date_reported': RkiMeldedatum.__name__,
                    'date_reported_count': RkiMeldedatum.count(),
                    'location': RkiLandkreis.__name__,
                    'location_count': RkiLandkreis.count(),
                    'location_group': RkiBundesland.__name__,
                    'location_group_count': RkiBundesland.count(),
                    'altersgruppe': RkiAltersgruppe.__name__,
                    'altersgruppe_count': RkiAltersgruppe.count(),
                    'data_class': RkiData.__name__,
                    'data_class_count': RkiData.count(),
                }
            }
            df = pd.DataFrame.from_dict(t, orient='index')
            app.logger.info(df)
        app.logger.info("")
        app.logger.info(" WebAdminService.database_import_status() [done]")
        app.logger.info("------------------------------------------------------------")
        return t

