import sys
import csv
from app_config.database import db, app
from data_all.all_service_mixins import AllServiceMixinImport
from data_all.all_config import BlueprintConfig
from app_web.web_model_factory import BlueprintDateReportedFactory
from data_who.who_model_import_factories import WhoFlatFactory, WhoImportFactory
from data_who.who_model_import import WhoImport, WhoFlat


class WhoServiceImport(AllServiceMixinImport):
    def __init__(self, database, config: BlueprintConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" WHO Service Import [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" [WHO] Service Import [ready]")
        app.logger.debug("------------------------------------------------------------")

    def import_file(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [WHO] import [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [WHO] import into TABLE: "+self.cfg.tablename+" <--- from FILE "+self.cfg.cvsfile_path)
        app.logger.info("------------------------------------------------------------")
        if sys.platform == 'linux':
            keyDate_reported ='\ufeffDate_reported'
        else:
            keyDate_reported = 'ï»¿Date_reported'
        WhoImport.remove_all()
        WhoFlat.remove_all()
        with open(self.cfg.cvsfile_path, newline='\n') as csv_file:
            file_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
            k = 0
            for row in file_reader:
                date_reported = row[keyDate_reported]
                d = BlueprintDateReportedFactory.create_new_object_for_who(my_date_reported=date_reported)
                o = WhoImportFactory.create_new(date_reported=date_reported, d=d, row=row)
                db.session.add(o)
                my_data = {
                    'new_cases': int(row['New_cases']),
                    'cumulative_cases': int(row['Cumulative_cases']),
                    'new_deaths': int(row['New_deaths']),
                    'cumulative_deaths': int(row['Cumulative_deaths']),
                }
                oo = WhoFlatFactory.create_new(date_reported=date_reported, d=d, row=row, my_data=my_data)
                db.session.add(oo)
                k += 1
                if (k % 2000) == 0:
                    db.session.commit()
                    app.logger.info(" [WHO] import  ... " + str(k) + " rows")
                if self.cfg.reached_limit_import_for_testing(row_number=k):
                    break
            db.session.commit()
            app.logger.info(" [WHO] import  ... " + str(k) + " rows total")
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [WHO] imported into TABLE: "+self.cfg.tablename+" <--- from FILE "+self.cfg.cvsfile_path)
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [WHO] import [done]")
        app.logger.info("------------------------------------------------------------")
        return self
