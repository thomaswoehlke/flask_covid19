import os

from app_config.database import root_dir, app
from data_ecdc.ecdc_model_import import EcdcImport
from data_who.who_model_import import WhoImport
from data_vaccination.vaccination_model_import import VaccinationImport
from data_owid.owid_model_import import OwidImport
from data_rki.rki_model_import import RkiImport


class BlueprintConfig:
    def __init__(self, slug: str,
                 category: str,
                 cvsfile_subpath: str,
                 sub_category: str,
                 tablename: str,
                 cvsfile_name: str,
                 cvsfile_backup_name: str,
                 url_src: str,
                 limit_import_for_testing: bool,
                 limit_import_for_testing_threshold: int):
        self.limit_nr = 20
        self.data_path = root_dir + os.sep + "data"
        self.data_path_tmp = self.data_path
        self.slug = slug,
        self.category = category
        self.cvsfile_subpath = cvsfile_subpath
        self.sub_category = sub_category
        self.tablename = tablename
        self.cvsfile_name = cvsfile_name
        self.cvsfile_backup_name = cvsfile_backup_name
        self.url_src = url_src
        self.download_path = self.data_path_tmp + os.sep + self.cvsfile_name
        self.cvsfile_backup_path = self.data_path + os.sep + self.cvsfile_subpath + os.sep + self.cvsfile_backup_name
        self.cvsfile_path = self.data_path + os.sep + self.cvsfile_subpath + os.sep + self.cvsfile_name
        self.cvsfile_parentent_path = self.data_path + os.sep + self.cvsfile_subpath
        self.msg_job = "start downloading FILE: "+self.cvsfile_name+" <--- from "+self.url_src
        self.msg_ok = "downloaded FILE: " + self.cvsfile_path + " <--- from " + self.url_src
        self.msg_error = "Error while downloading: " + self.cvsfile_path + " <--- from " + self.url_src
        self.limit_import_for_testing = limit_import_for_testing
        self.limit_import_for_testing_threshold = limit_import_for_testing_threshold
        os.makedirs(name=self.cvsfile_parentent_path, exist_ok=True)

    def reached_limit_import_for_testing(self, row_number: int):
        if self.limit_import_for_testing:
            return row_number >= self.limit_import_for_testing_threshold
        else:
            return False

    @classmethod
    def create_config_for_who(cls):
        return BlueprintConfig(
            slug='who',
            category='WHO',
            cvsfile_subpath='who',
            sub_category='Cases and Deaths',
            tablename=WhoImport.__tablename__,
            cvsfile_name="WHO.csv",
            cvsfile_backup_name='WHO_backup.csv',
            url_src="https://covid19.who.int/WHO-COVID-19-global-data.csv",
            limit_import_for_testing=app.config['TEST_IMPORT_WHO'],
            limit_import_for_testing_threshold=app.config['TEST_IMPORT_WHO_THRESHOLD']
        )

    @classmethod
    def create_config_for_rki_vaccination(cls):
        return BlueprintConfig(
            slug='vaccination',
            category='RKI',
            cvsfile_subpath='vaccination',
            sub_category='Vaccination',
            tablename=VaccinationImport.__tablename__,
            cvsfile_name="Vaccination.tsv",
            cvsfile_backup_name='Vaccination_backup.tsv',
            url_src="https://impfdashboard.de/static/data/germany_vaccinations_timeseries_v2.tsv",
            limit_import_for_testing=False,
            limit_import_for_testing_threshold=0
        )

    @classmethod
    def create_config_for_owid(cls):
        return BlueprintConfig(
            slug='owid',
            category='OWID',
            cvsfile_subpath='owid',
            sub_category='Our World in Data',
            tablename=OwidImport.__tablename__,
            cvsfile_name="OWID.csv",
            cvsfile_backup_name='OWID_backup.csv',
            url_src="https://covid.ourworldindata.org/data/owid-covid-data.csv",
            limit_import_for_testing=app.config['TEST_IMPORT_OWID'],
            limit_import_for_testing_threshold=app.config['TEST_IMPORT_OWID_THRESHOLD']
        )

    @classmethod
    def create_config_for_ecdc(cls):
        return BlueprintConfig(
            slug='ecdc',
            category='ECDC',
            cvsfile_subpath='ecdc',
            sub_category='European Centre for Disease Prevention and Control',
            tablename=EcdcImport.__tablename__,
            cvsfile_name="ECDC.csv",
            cvsfile_backup_name='ECDC_backup.csv',
            url_src="https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/",
            limit_import_for_testing=app.config['TEST_IMPORT_ECDC'],
            limit_import_for_testing_threshold=app.config['TEST_IMPORT_ECDC_THRESHOLD']
        )

    @classmethod
    def create_config_for_rki(cls):
        return BlueprintConfig(
            slug='rki',
            category='RKI',
            cvsfile_subpath='rki',
            sub_category='Cases',
            tablename=RkiImport.__tablename__,
            cvsfile_name="RKI.csv",
            cvsfile_backup_name='RKI_backup.csv',
            url_src="https://www.arcgis.com/sharing/rest/content/items/f10774f1c63e40168479a1feb6c7ca74/data",
            limit_import_for_testing=app.config['TEST_IMPORT_RKI'],
            limit_import_for_testing_threshold=app.config['TEST_IMPORT_RKI_THRESHOLD']
        )

