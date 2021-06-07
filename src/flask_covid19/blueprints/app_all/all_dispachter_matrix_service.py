from database import app
from flask_covid19 import WhoService, OwidService, RkiService, VaccinationService, EcdcService, DiviService
from flask_covid19.blueprints.app_all.all_service_mixins import AllServiceMixin, AllServiceMixinUpdateFull


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
                who_service, vaccination_service, divi_service, owid_service, rki_service
            ],
            'import_file': [
                who_service, vaccination_service, owid_service, rki_service
            ],
            'full_update_dimension_tables': [
                who_service, vaccination_service, owid_service, rki_service
            ],
            'update_dimension_tables': [
                who_service, vaccination_service, owid_service, rki_service
            ],
            'full_update_fact_table': [
                who_service, vaccination_service, owid_service, rki_service
            ],
            'update_fact_table': [
                who_service, vaccination_service, owid_service, rki_service
            ],
            'full_update_star_schema': [
                who_service, vaccination_service, owid_service, rki_service
            ],
            'update_star_schema': [
                who_service, vaccination_service, owid_service, rki_service
            ],
            'full_update': [
                who_service, vaccination_service, owid_service, rki_service
            ],
            'update': [
                who_service, vaccination_service, owid_service, rki_service
            ],
            'delete_last_day': [
                who_service, vaccination_service, owid_service, rki_service
            ],
            'delete_last_location_group': [
                who_service, owid_service, rki_service
            ],
        }
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" Dispachter Matrix Service [ready] ")

    def download(self):
        app.logger.info(" ")
        app.logger.info(" AllDataServiceDispachterMatrix.download [start]")
        app.logger.info(" ")
        for service in self.__services_for['download']:
            service.download()
        app.logger.info(" ")
        app.logger.info(" AllDataServiceDispachterMatrix.download [done] ")
        app.logger.info(" ")
        return self

    def import_file(self):
        app.logger.info(" ")
        app.logger.info(" AllDataServiceDispachterMatrix.import_file [start]")
        app.logger.info(" ")
        for service in self.__services_for['import_file']:
            service.import_file()
        app.logger.info(" ")
        app.logger.info(" AllDataServiceDispachterMatrix.import_file [done] ")
        app.logger.info(" ")
        return self

    def full_update_dimension_tables(self):
        app.logger.info(" ")
        app.logger.info(" AllDataServiceDispachterMatrix.full_update_dimension_tables [start] ")
        app.logger.info(" ")
        for service in self.__services_for['full_update_dimension_tables']:
            service.full_update_dimension_tables()
        app.logger.info(" ")
        app.logger.info(" AllDataServiceDispachterMatrix.full_update_dimension_tables [done] ")
        app.logger.info(" ")
        return self

    def update_dimension_tables(self):
        app.logger.info(" ")
        app.logger.info(" AllDataServiceDispachterMatrix.update_dimension_tables [start] ")
        app.logger.info(" ")
        for service in self.__services_for['update_dimension_tables']:
            service.update_dimension_tables()
        app.logger.info(" ")
        app.logger.info(" AllDataServiceDispachterMatrix.update_dimension_tables [done] ")
        app.logger.info(" ")
        return self

    def full_update_fact_table(self):
        app.logger.info(" ")
        app.logger.info(" AllDataServiceDispachterMatrix.full_update_fact_table [start] ")
        app.logger.info(" ")
        for service in self.__services_for['full_update_fact_table']:
            service.full_update_fact_table()
        app.logger.info(" ")
        app.logger.info(" AllDataServiceDispachterMatrix.full_update_fact_table ")
        app.logger.info(" ")
        return self

    def update_fact_table(self):
        app.logger.info(" ")
        app.logger.info(" AllDataServiceDispachterMatrix.update_fact_table [start] ")
        app.logger.info(" ")
        for service in self.__services_for['update_fact_table']:
            service.update_fact_table()
        app.logger.info(" ")
        app.logger.info(" AllDataServiceDispachterMatrix.update_fact_table [done] ")
        app.logger.info(" ")
        return self

    def full_update_star_schema(self):
        app.logger.info(" ")
        app.logger.info(" AllDataServiceDispachterMatrix.full_update_star_schema [start] ")
        app.logger.info(" ")
        for service in self.__services_for['full_update_star_schema']:
            service.full_update_star_schema()
        app.logger.info(" ")
        app.logger.info(" AllDataServiceDispachterMatrix.full_update_star_schema [done] ")
        app.logger.info(" ")
        return self

    def update_star_schema(self):
        app.logger.info(" ")
        app.logger.info(" AllDataServiceDispachterMatrix.update_star_schema [start] ")
        app.logger.info(" ")
        for service in self.__services_for['update_star_schema']:
            service.update_star_schema()
        app.logger.info(" ")
        app.logger.info(" AllDataServiceDispachterMatrix.update_star_schema [done] ")
        app.logger.info(" ")
        return self

    def full_update(self):
        app.logger.info(" ")
        app.logger.info(" AllDataServiceDispachterMatrix.full_update [start] ")
        app.logger.info(" ")
        for service in self.__services_for['full_update']:
            service.full_update()
        app.logger.info(" ")
        app.logger.info(" AllDataServiceDispachterMatrix.full_update [done] ")
        app.logger.info(" ")
        return self

    def update(self):
        app.logger.info(" ")
        app.logger.info(" AllDataServiceDispachterMatrix.update [start] ")
        app.logger.info(" ")
        for service in self.__services_for['update']:
            service.update()
        app.logger.info(" ")
        app.logger.info(" AllDataServiceDispachterMatrix.update [done] ")
        app.logger.info(" ")
        return self

    def delete_last_day(self):
        app.logger.info(" ")
        app.logger.info(" AllDataServiceDispachterMatrix.delete_last_day [start] ")
        app.logger.info(" ")
        for service in self.__services_for['delete_last_day']:
            service.delete_last_day()
        app.logger.info(" ")
        app.logger.info(" AllDataServiceDispachterMatrix.delete_last_day [done] ")
        app.logger.info(" ")
        return self

    def delete_last_location_group(self):
        app.logger.info(" ")
        app.logger.info(" AllDataServiceDispachterMatrix.delete_last_location_group [start] ")
        app.logger.info(" ")
        for service in self.__services_for['delete_last_location_group']:
            service.delete_last_location_group()
        app.logger.info(" ")
        app.logger.info(" AllDataServiceDispachterMatrix.delete_last_location_group [done] ")
        app.logger.info(" ")
        return self