import csv

from flask_covid19.app_config.database import db, app

from flask_covid19.data_all.all_service_import_mixins import AllServiceMixinImport
from flask_covid19.data_all.all_config import BlueprintConfig
from flask_covid19.data_all.all_model_date_reported_factory import BlueprintDateReportedFactory

from flask_covid19.data_vaccination.vaccination_model_import import VaccinationImport, VaccinationImportFactory
from flask_covid19.data_vaccination.vaccination_model_flat import VaccinationFlat, VaccinationFlatFactory


class VaccinationServiceImport(AllServiceMixinImport):
    def __init__(self, database, config: BlueprintConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Vaccination Service Import [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ready: [Vaccination] Service Import ")
        app.logger.debug("------------------------------------------------------------")

    def import_file(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [Vaccination] import [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [Vaccination] import into TABLE: "+self.cfg.tablename+" <--- from FILE "+self.cfg.cvsfile_path)
        app.logger.info("------------------------------------------------------------")
        VaccinationImport.remove_all()
        VaccinationFlat.remove_all()
        k = 0
        with open(self.cfg.cvsfile_path, newline='\n') as csv_file:
            file_reader = csv.DictReader(csv_file, delimiter='\t', quotechar='"')
            for row in file_reader:
                date_reported = row['date']
                d = BlueprintDateReportedFactory.create_new_object_for_vaccination(my_date_reported=date_reported)
                o = VaccinationImportFactory.create_new(date_reported=date_reported, d=d, row=row)
                db.session.add(o)
                oo = VaccinationFlatFactory.create_new(date_reported=date_reported, d=d, row=row)
                db.session.add(oo)
                k += 1
                if (k % 100) == 0:
                    db.session.commit()
                    app.logger.info(" [Vaccination] import  ... " + str(k) + " rows")
            db.session.commit()
            app.logger.info(" [Vaccination] import  ... " + str(k) + " rows total")
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [Vaccination] imported into TABLE: "+self.cfg.tablename+" <--- from FILE "+self.cfg.cvsfile_path)
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [Vaccination] import [done]")
        app.logger.info("------------------------------------------------------------")
        return self
