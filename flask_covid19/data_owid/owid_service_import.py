import csv
from app_config.database import db, app


from data_all.all_service_mixins import AllServiceMixinImport
from data_all.all_config import BlueprintConfig
from app_web.web_model_factory import BlueprintDateReportedFactory
from data_owid.owid_model_import import OwidImport
from data_owid.owid_model_flat import OwidFlat
from data_owid.owid_model_import_factories import OwidImportFactory, OwidFlatFactory


class OwidServiceImport(AllServiceMixinImport):
    def __init__(self, database, config: BlueprintConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" OWID Service Import [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" [OWID] Service Import [ready]")
        app.logger.debug("------------------------------------------------------------")

    def import_file(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] import [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] import into TABLE: "+self.cfg.tablename+" <--- from FILE "+self.cfg.cvsfile_path)
        app.logger.info("------------------------------------------------------------")
        OwidImport.remove_all()
        OwidFlat.remove_all()
        with open(self.cfg.cvsfile_path, newline='\n') as csv_file:
            file_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
            k = 0
            for row in file_reader:
                date_reported = row['date']
                d = BlueprintDateReportedFactory.create_new_object_for_owid(my_date_reported=date_reported)
                o = OwidImportFactory.create_new(date_reported=date_reported, d=d, row=row)
                db.session.add(o)
                f = OwidFlatFactory.create_new(d=d, row=row)
                db.session.add(f)
                k += 1
                if (k % 2000) == 0:
                    db.session.commit()
                    app.logger.info(" [OWID] import ... " + str(k) + " rows")
                if self.cfg.reached_limit_import_for_testing(row_number=k):
                    break
            db.session.commit()
            app.logger.info(" [OWID] import ... " + str(k) + " rows total")
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] imported into TABLE: "+self.cfg.tablename+" <--- from FILE "+self.cfg.cvsfile_path)
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [OWID] import [done]")
        app.logger.info("------------------------------------------------------------")
        return self
