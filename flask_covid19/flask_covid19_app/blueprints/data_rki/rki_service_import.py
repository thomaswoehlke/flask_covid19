import csv

from flask_covid19_conf.database import db, app
from flask_covid19_app_all.all_service_mixins import AllServiceMixinImport
from flask_covid19_app_all.all_config import BlueprintConfig
from flask_covid19_app.blueprints.data_rki.rki_model_factories import RkiServiceImportFactory
from flask_covid19_app.blueprints.data_rki.rki_model_import_factories import RkiFlatFactory, RkiImportFactory
from flask_covid19_app.blueprints.data_rki.rki_model_import import RkiImport, RkiFlat


class RkiServiceImport(AllServiceMixinImport):
    def __init__(self, database, config: BlueprintConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Service Import [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Service Import [ready]")
        app.logger.debug("------------------------------------------------------------")

    def import_file(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" RkiServiceImport.import_file()  [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" import into TABLE: "+self.cfg.tablename+" <--- from FILE "+self.cfg.cvsfile_path)
        app.logger.info("------------------------------------------------------------")
        RkiImport.remove_all()
        RkiFlat.remove_all()
        with open(self.cfg.cvsfile_path, newline='\n') as csv_file:
            file_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
            k = 0
            for row in file_reader:
                k += 1
                my_datum = RkiServiceImportFactory.row_str_to_date_fields(row)
                o = RkiImportFactory.create_new(row=row, my_datum=my_datum)
                db.session.add(o)
                my_int_data = RkiServiceImportFactory.row_str_to_int_fields(row)
                oo = RkiFlatFactory.create_new(row=row, my_int_data=my_int_data, my_datum=my_datum)
                db.session.add(oo)
                if (k % 2000) == 0:
                    db.session.commit()
                    app.logger.info(" import RKI ... " + str(k) + " rows")
                if self.cfg.reached_limit_import_for_testing(row_number=k):
                    break
            db.session.commit()
            app.logger.info(" import RKI ... " + str(k) + " rows total")
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" imported into TABLE: "+self.cfg.tablename+" <--- from FILE "+self.cfg.cvsfile_path)
        app.logger.info("------------------------------------------------------------")
        app.logger.info("RkiServiceImport.import_file()  [done]")
        app.logger.info("------------------------------------------------------------")
        return self
