from database import app
from flask_covid19_app import WhoService, OwidService, RkiService, VaccinationService, EcdcService, DiviService
from flask_covid19_app.blueprints.app_all.all_service_mixins import AllServiceMixin

from flask_covid19_app.blueprints.data_ecdc.ecdc_service import EcdcService
from flask_covid19_app.blueprints.data_owid.owid_service import OwidService
from flask_covid19_app.blueprints.data_vaccination.vaccination_service import VaccinationService
from flask_covid19_app.blueprints.data_who.who_service import WhoService
from flask_covid19_app.blueprints.data_divi.divi_service import DiviService
from flask_covid19_app.blueprints.data_rki.rki_service import RkiService


class AllDataServiceDispachterMatrix(AllServiceMixin):
    def __init__(self,
                 who_service: WhoService,
                 owid_service: OwidService,
                 rki_service: RkiService,
                 vaccination_service: VaccinationService,
                 ecdc_service: EcdcService,
                 divi_service: DiviService):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Dispachter Matrix Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__services_for = {
            'download': [
                who_service, vaccination_service, divi_service, ecdc_service, owid_service, rki_service
            ],
            'import_file': [
                who_service, vaccination_service, ecdc_service, owid_service, rki_service
            ],
            'full_update_dimension_tables': [
                who_service, vaccination_service, ecdc_service, owid_service, rki_service
            ],
            'update_dimension_tables': [
                who_service, vaccination_service, ecdc_service, owid_service, rki_service
            ],
            'full_update_fact_table': [
                who_service, vaccination_service, ecdc_service, owid_service, rki_service
            ],
            'update_fact_table': [
                who_service, vaccination_service, ecdc_service, owid_service, rki_service
            ],
            'full_update': [
                who_service, vaccination_service, ecdc_service, owid_service, rki_service
            ],
            'update': [
                who_service, vaccination_service, ecdc_service, owid_service, rki_service
            ],
            'delete_last_day': [
                who_service, owid_service, rki_service
            ],
        }
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" Dispachter Matrix Service [ready] ")
        app.logger.debug("------------------------------------------------------------")

    def download(self):
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" AllDataServiceDispachterMatrix.download [start]")
        app.logger.info(" ")
        for service in self.__services_for['download']:
            service.download()
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" AllDataServiceDispachterMatrix.download [done] ")
        app.logger.debug("------------------------------------------------------------")
        return self

    def import_file(self):
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" AllDataServiceDispachterMatrix.import_file [start]")
        app.logger.debug("------------------------------------------------------------")
        for service in self.__services_for['import_file']:
            service.import_file()
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" AllDataServiceDispachterMatrix.import_file [done] ")
        app.logger.debug("------------------------------------------------------------")
        return self

    def full_update_dimension_tables(self):
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" AllDataServiceDispachterMatrix.full_update_dimension_tables [start] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        for service in self.__services_for['full_update_dimension_tables']:
            service.full_update_dimension_tables()
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" AllDataServiceDispachterMatrix.full_update_dimension_tables [done] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        return self

    def update_dimension_tables(self):
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" AllDataServiceDispachterMatrix.update_dimension_tables [start] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        for service in self.__services_for['update_dimension_tables']:
            service.update_dimension_tables()
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" AllDataServiceDispachterMatrix.update_dimension_tables [done] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        return self

    def full_update_fact_table(self):
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" AllDataServiceDispachterMatrix.full_update_fact_table [start] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        for service in self.__services_for['full_update_fact_table']:
            service.full_update_fact_table()
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" AllDataServiceDispachterMatrix.full_update_fact_table ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        return self

    def update_fact_table(self):
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" AllDataServiceDispachterMatrix.update_fact_table [start] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        for service in self.__services_for['update_fact_table']:
            service.update_fact_table()
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" AllDataServiceDispachterMatrix.update_fact_table [done] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        return self

    def full_update(self):
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" AllDataServiceDispachterMatrix.full_update [start] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        for service in self.__services_for['full_update']:
            service.full_update()
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" AllDataServiceDispachterMatrix.full_update [done] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        return self

    def update(self):
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" AllDataServiceDispachterMatrix.update [start] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        for service in self.__services_for['update']:
            service.update()
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" AllDataServiceDispachterMatrix.update [done] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        return self

    def delete_last_day(self):
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" AllDataServiceDispachterMatrix.delete_last_day [start] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        for service in self.__services_for['delete_last_day']:
            service.delete_last_day()
        app.logger.info(" ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" AllDataServiceDispachterMatrix.delete_last_day [done] ")
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ")
        return self
