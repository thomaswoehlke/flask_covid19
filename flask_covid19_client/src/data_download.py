#!/usr/bin/env python

import os
import wget
import subprocess

os.system("pip install pandas")
os.system("pip install scipy")
os.system("pip install matplotlib")
os.system("pip install wget")

root_dir = os.getcwd()


class BlueprintConfig:
    def __init__(self, slug: str,
                 category: str,
                 cvsfile_subpath: str,
                 sub_category: str,
                 cvsfile_name: str,
                 cvsfile_backup_name: str,
                 url_src: str):
        self.limit_nr = 20
        self.data_path = root_dir + os.sep + "data"
        self.data_path_tmp = self.data_path
        self.slug = slug,
        self.category = category
        self.cvsfile_subpath = cvsfile_subpath
        self.sub_category = sub_category
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
        os.makedirs(name=self.cvsfile_parentent_path, exist_ok=True)

    @classmethod
    def create_config_for_who(cls):
        return BlueprintConfig(
            slug='who',
            category='WHO',
            cvsfile_subpath='who',
            sub_category='Cases and Deaths',
            cvsfile_name="WHO.csv",
            cvsfile_backup_name='WHO_backup.csv',
            url_src="https://covid19.who.int/WHO-COVID-19-global-data.csv"
        )

    @classmethod
    def create_config_for_vaccination(cls):
        return BlueprintConfig(
            slug='vaccination',
            category='RKI',
            cvsfile_subpath='vaccination',
            sub_category='Vaccination',
            cvsfile_name="Vaccination.tsv",
            cvsfile_backup_name='Vaccination_backup.tsv',
            url_src="https://impfdashboard.de/static/data/germany_vaccinations_timeseries_v2.tsv"
        )

    @classmethod
    def create_config_for_owid(cls):
        return BlueprintConfig(
            slug='owid',
            category='OWID',
            cvsfile_subpath='owid',
            sub_category='Our World in Data',
            cvsfile_name="OWID.csv",
            cvsfile_backup_name='OWID_backup.csv',
            url_src="https://covid.ourworldindata.org/data/owid-covid-data.csv"
        )

    @classmethod
    def create_config_for_ecdc(cls):
        return BlueprintConfig(
            slug='ecdc',
            category='ECDC',
            cvsfile_subpath='ecdc',
            sub_category='European Centre for Disease Prevention and Control',
            cvsfile_name="ECDC.csv",
            cvsfile_backup_name='ECDC_backup.csv',
            url_src="https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/"
        )

    @classmethod
    def create_config_for_rki(cls):
        return BlueprintConfig(
            slug='rki',
            category='RKI',
            cvsfile_subpath='rki',
            sub_category='Cases',
            cvsfile_name="RKI.csv",
            cvsfile_backup_name='RKI_backup.csv',
            url_src="https://www.arcgis.com/sharing/rest/content/items/f10774f1c63e40168479a1feb6c7ca74/data"
        )
        

class AllServiceMixinDownload:

    def download(self):
        return self

        
class AllDownloadService(AllServiceMixinDownload):
    def __init__(self, config: BlueprintConfig):
        print("------------------------------------------------------------")
        print(" DownloadService [init]")
        print("------------------------------------------------------------")
        self.cfg = config
        print("------------------------------------------------------------")
        print(" ready: [" + self.cfg.category + "] Download Service")
        print("------------------------------------------------------------")

    def __prepare_download(self):
        os.makedirs(self.cfg.data_path, exist_ok=True)
        if os.path.isfile(self.cfg.cvsfile_path):
            os.remove(self.cfg.cvsfile_path)
        return self

    def __download_with_wget(self):
        data_file = wget.download(url=self.cfg.url_src, out=self.cfg.cvsfile_path)
        print(data_file)
        return self

    def __download_with_subprocess_and_os_native_wget(self):
        orig_workdir = os.getcwd()
        os.chdir(self.cfg.data_path)
        my_cmds = [
            'wget ' + self.cfg.url_src + ' -O ' + self.cfg.download_path + ' -o ' + self.cfg.download_path + '.log',
            'mv -f ' + self.cfg.download_path + ' ' + self.cfg.cvsfile_path,
            'mv -f ' + self.cfg.download_path + '.log ' + self.cfg.cvsfile_path + '.log'
        ]
        for my_cmd in my_cmds:
            retcode = subprocess.call(my_cmd, shell=True)
            if retcode == 0:
                print(' [' + self.cfg.category + '] download result: OK ' + my_cmd)
            else:
                print(' [' + self.cfg.category + '] download result: NOT OK: ' + my_cmd)
        os.chdir(orig_workdir)
        return self

    def download(self):
        print("------------------------------------------------------------")
        print(" [" + self.cfg.category + "] download - [begin] ")
        print("------------------------------------------------------------")
        print(" "+self.cfg.msg_job)
        print("------------------------------------------------------------")
        self.__prepare_download()
        if self.cfg.slug[0] in ['who', 'ecdc', 'divi', 'vaccination', 'owid', 'rki']:
            self.__download_with_subprocess_and_os_native_wget()
        else:
            self.__download_with_wget()
        print("------------------------------------------------------------")
        print(" [" + self.cfg.category + "] download - [done] ")
        print("------------------------------------------------------------")
        return self


class DownloadFilesService(AllServiceMixinDownload):
    def __init__(self):
        print("------------------------------------------------------------")
        print(" WHO Service [init]")
        print("------------------------------------------------------------")
        
        who_cfg = BlueprintConfig.create_config_for_who()
        vaccination_cfg = BlueprintConfig.create_config_for_vaccination()
        owid_cfg =  BlueprintConfig.create_config_for_owid()
        ecdc_cfg = BlueprintConfig.create_config_for_ecdc()
        rki_cfg = BlueprintConfig.create_config_for_rki()
        
        self.who_download = AllDownloadService(who_cfg)
        self.vaccination_download = AllDownloadService(vaccination_cfg)
        self.owid_download = AllDownloadService(owid_cfg)
        self.ecdc_download = AllDownloadService(ecdc_cfg)
        self.rki_download = AllDownloadService(rki_cfg)

        self.download_services = [
          self.who_download, 
          self.vaccination_download, 
          self.owid_download, 
          self.ecdc_download, 
          self.rki_download
        ]
      
        print("------------------------------------------------------------")
        print(" ready: [WHO] Service")
        print("------------------------------------------------------------")

    def download(self):
        print("------------------------------------------------------------")
        print(" start: download")
        print("------------------------------------------------------------")
        for download_service in self.download_services:
          download_service.download()
        print("------------------------------------------------------------")
        print(" done: download")
        print("------------------------------------------------------------")
        return self


files_downloader = DownloadFilesService()
files_downloader.download()

