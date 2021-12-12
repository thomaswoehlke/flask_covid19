#!/usr/bin/env python
from project.data_all.all_config import BlueprintConfig
from project.data_all.all_service_download import AllDownloadService
from project.data_all.all_service_download_mixins import AllServiceMixinDownload


class DownloadFilesService(AllServiceMixinDownload):
    def __init__(self):
        print("------------------------------------------------------------")
        print(" WHO Service [init]")
        print("------------------------------------------------------------")

        who_cfg = BlueprintConfig.create_config_for_who()
        vaccination_cfg = BlueprintConfig.create_config_for_rki_vaccination()
        owid_cfg = BlueprintConfig.create_config_for_owid()
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
            self.rki_download,
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
