import os
import subprocess
import wget

from project.data.database import app
from project.data_all.services.all_service_config import AllServiceConfig
from project.data_all.services.all_service_mixins import AllServiceMixinDownload


class AllDownloadService(AllServiceMixinDownload):
    def __init__(self, database, config: AllServiceConfig):
        self.__database = database
        self.cfg = config
        app.logger.info(" ready: [" + self.cfg.category + "] Download Service")

    def __prepare_download(self):
        os.makedirs(self.cfg.data_path, exist_ok=True)
        if os.path.isfile(self.cfg.cvsfile_path):
            os.remove(self.cfg.cvsfile_path)
        return self

    def __download_with_wget(self):
        data_file = wget.download(url=self.cfg.url_src, out=self.cfg.cvsfile_path)
        app.logger.info(data_file)
        return self

    def __download_with_subprocess_and_os_native_wget(self):
        orig_workdir = os.getcwd()
        os.chdir(self.cfg.data_path)
        my_cmds = [
            "wget "
            + self.cfg.url_src
            + " -O "
            + self.cfg.download_path
            + " -o "
            + self.cfg.download_path
            + ".log",
            "touch " + self.cfg.cvsfile_path,
            "cp -f " + self.cfg.cvsfile_path + " " + self.cfg.cvsfile_backup_path,
            "mv -f " + self.cfg.download_path + " " + self.cfg.cvsfile_path,
            "mv -f "
            + self.cfg.download_path
            + ".log "
            + self.cfg.cvsfile_path
            + ".log",
        ]
        for my_cmd in my_cmds:
            retcode = subprocess.call(my_cmd, shell=True)
            if retcode == 0:
                app.logger.info(
                    " [" + self.cfg.category + "] download result: OK " + my_cmd
                )
            else:
                app.logger.warn(
                    " [" + self.cfg.category + "] download result: NOT OK: " + my_cmd
                )
        os.chdir(orig_workdir)
        return self

    def download(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [" + self.cfg.category + "] download - [begin] ")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" " + self.cfg.msg_job)
        app.logger.info("------------------------------------------------------------")
        self.__prepare_download()
        if self.cfg.slug[0] in ["who", "ecdc", "divi", "vaccination", "owid", "rki"]:
            self.__download_with_subprocess_and_os_native_wget()
        else:
            self.__download_with_wget()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [" + self.cfg.category + "] download - [done] ")
        app.logger.info("------------------------------------------------------------")
        return self
