import os
import subprocess
import pandas as pd

from project.data.database import app, db
from project.data_ecdc.ecdc_views import ecdc_service
from project.data_ecdc.model.ecdc_model_data import EcdcData
from project.data_ecdc.model.ecdc_model_import import EcdcImport
from project.data_owid.model.owid_model_data import OwidData
from project.data_owid.model.owid_model_import import OwidImport
from project.data_owid.owid_views import owid_service
from project.data_rki.model.rki_model_data import RkiData
from project.data_rki.model.rki_model_import import RkiImport
from project.data_rki.rki_views import rki_service
from project.data_vaccination.model.vaccination_model_data import VaccinationData
from project.data_vaccination.model.vaccination_model_import import VaccinationImport
from project.data_vaccination.vaccination_views import vaccination_service
from project.data_who.model.who_model_data import WhoData
from project.data_who.model.who_model_import import WhoImport
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
                    'data_class': WhoData.__name__,
                    'data_count': WhoData.count(),
                    'import_class': WhoImport.__name__,
                    'import_count': WhoImport.count(),
                    'file_count': who_service.count_file_rows()
                },
                'OWID': {
                    'data_class': OwidData.__name__,
                    'data_count': OwidData.count(),
                    'import_class': OwidImport.__name__,
                    'import_count': OwidImport.count(),
                    'file_count': owid_service.count_file_rows()
                },
                'ECDC': {
                    'data_class': EcdcData.__name__,
                    'data_count': EcdcData.count(),
                    'import_class': EcdcImport.__name__,
                    'import_count': EcdcImport.count(),
                    'file_count': ecdc_service.count_file_rows()
                },
                'Vaccination': {
                    'data_class': VaccinationData.__name__,
                    'data_count': VaccinationData.count(),
                    'import_class': VaccinationImport.__name__,
                    'import_count': VaccinationImport.count(),
                    'file_count': vaccination_service.count_file_rows()
                },
                'RKI': {
                    'data_class': RkiData.__name__,
                    'data_count': RkiData.count(),
                    'import_class': RkiImport.__name__,
                    'import_count': RkiImport.count(),
                    'file_count': rki_service.count_file_rows()
                }
            }
            df = pd.DataFrame.from_dict(t, orient='index')
            app.logger.info(df)
        app.logger.info("")
        app.logger.info(" WebAdminService.database_import_status() [done]")
        app.logger.info("------------------------------------------------------------")
        return t

