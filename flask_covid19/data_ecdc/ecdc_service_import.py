import csv

from app_config.database import db, app
from data_all.all_service_import_mixins import AllServiceMixinImport
from data_all.all_config import BlueprintConfig
from data_all.all_model_date_reported_factory import BlueprintDateReportedFactory
from data_ecdc.ecdc_model_import import EcdcImport, EcdcImportFactory
from data_ecdc.ecdc_model_flat import EcdcFlat, EcdcFlatFactory


class EcdcServiceImport(AllServiceMixinImport):
    def __init__(self, database, config: BlueprintConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" ECDC Service Import [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ready: [ECDC] Service Import")
        app.logger.debug("------------------------------------------------------------")

    def import_file(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [ECDC] import [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [ECDC] import into TABLE: "+self.cfg.tablename+" <--- from FILE "+self.cfg.cvsfile_path)
        app.logger.info("------------------------------------------------------------")
        k = 0
        EcdcImport.remove_all()
        EcdcFlat.remove_all()
        with open(self.cfg.cvsfile_path, newline='') as csv_file:
            file_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
            for row in file_reader:
                date_rep = row['dateRep']
                d = BlueprintDateReportedFactory.create_new_object_for_ecdc(my_date_reported=date_rep)
                o = EcdcImportFactory.create_new(date_reported=date_rep, d=d, row=row)
                db.session.add(o)
                oo = EcdcFlatFactory.create_new(d=d, row=row)
                db.session.add(oo)
                k = k + 1
                if (k % 1000) == 0:
                    db.session.commit()
                    app.logger.info(" [ECDC] import  ...  " + str(k) + " rows")
                if self.cfg.reached_limit_import_for_testing(row_number=k):
                    break
            db.session.commit()
            app.logger.info(" [ECDC] import  ...  " + str(k) + " rows total")
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [ECDC] imported into TABLE: "+self.cfg.tablename+" <--- from FILE "+self.cfg.cvsfile_path)
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [ECDC] import [done]")
        app.logger.info("------------------------------------------------------------")
        return self
