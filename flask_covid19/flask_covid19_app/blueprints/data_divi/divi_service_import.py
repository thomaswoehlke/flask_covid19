import sys
import csv

from flask_covid19_conf.database import db, app
from app_all.all_service_mixins import AllServiceMixinImport
from app_all.all_config import BlueprintConfig
from flask_covid19_app.blueprints.data_divi.divi_model_import import DiviImport


class DiviServiceImport(AllServiceMixinImport):
    def __init__(self, database, config: BlueprintConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" DIVI Service Import [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" DIVI Service Import [ready]")
        app.logger.debug("------------------------------------------------------------")

    def import_file(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" import DIVI [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" import into TABLE: "+self.cfg.tablename+" <--- from FILE "+self.cfg.cvsfile_path)
        app.logger.info("------------------------------------------------------------")
        if sys.platform == 'linux':
            keyDate_reported ='\ufeffDate_reported'
        else:
            keyDate_reported = 'ï»¿Date_reported'
        DiviImport.remove_all()
        with open(self.cfg.cvsfile_path, newline='\n') as csv_file:
            file_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
            k = 0
            for row in file_reader:
                o = DiviImport(
                    date_reported=row[keyDate_reported],
                    country_code=row['Country_code'],
                    country=row['Country'],
                    divi_region=row['divi_region'],
                    new_cases=row['New_cases'],
                    cumulative_cases=row['Cumulative_cases'],
                    new_deaths=row['New_deaths'],
                    cumulative_deaths=row['Cumulative_deaths']
                )
                db.session.add(o)
                k += 1
                if (k % 2000) == 0:
                    db.session.commit()
                    app.logger.info(" import DIVI  ... " + str(k) + " rows")
            db.session.commit()
            app.logger.info(" import DIVI  ... " + str(k) + " rows total")
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" imported into TABLE: "+self.cfg.tablename+"  <--- from FILE "+self.cfg.cvsfile_path)
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" import DIVI [done]")
        app.logger.info("------------------------------------------------------------")
        return self
