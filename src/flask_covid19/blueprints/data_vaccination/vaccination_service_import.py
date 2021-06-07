import csv

from database import db, app

from flask_covid19.blueprints.app_all.all_config import BlueprintConfig
from flask_covid19.blueprints.app_web.web_model_factory import BlueprintDateReportedFactory

from flask_covid19.blueprints.data_vaccination.vaccination_model import VaccinationDateReported
from flask_covid19.blueprints.data_vaccination.vaccination_model_import import VaccinationImport, VaccinationFlat


class VaccinationImportFactory:

    @classmethod
    def __int(cls, input_string: str):
        if input_string == '#REF!':
            return 0
        else:
            return int(input_string)

    @classmethod
    def create_new(cls, date_reported, d, row):
        o = VaccinationImport(
            dosen_kumulativ=cls.__int(row['dosen_kumulativ']),
            dosen_differenz_zum_vortag=cls.__int(row['dosen_differenz_zum_vortag']),
            dosen_biontech_kumulativ=cls.__int(row['dosen_biontech_kumulativ']),
            dosen_moderna_kumulativ=cls.__int(row['dosen_moderna_kumulativ']),
            personen_erst_kumulativ=cls.__int(row['personen_erst_kumulativ']),
            personen_voll_kumulativ=cls.__int(row['personen_voll_kumulativ']),
            impf_quote_erst=float(row['impf_quote_erst']),
            impf_quote_voll=float(row['impf_quote_voll']),
            indikation_alter_dosen=cls.__int(row['indikation_alter_dosen']),
            indikation_beruf_dosen=cls.__int(row['indikation_beruf_dosen']),
            indikation_medizinisch_dosen=cls.__int(row['indikation_medizinisch_dosen']),
            indikation_pflegeheim_dosen=cls.__int(row['indikation_pflegeheim_dosen']),
            indikation_alter_erst=cls.__int(row['indikation_alter_erst']),
            indikation_beruf_erst=cls.__int(row['indikation_beruf_erst']),
            indikation_medizinisch_erst=cls.__int(row['indikation_medizinisch_erst']),
            indikation_pflegeheim_erst=cls.__int(row['indikation_pflegeheim_erst']),
            indikation_alter_voll=cls.__int(row['indikation_alter_voll']),
            indikation_beruf_voll=cls.__int(row['indikation_beruf_voll']),
            indikation_medizinisch_voll=cls.__int(row['indikation_medizinisch_voll']),
            indikation_pflegeheim_voll=cls.__int(row['indikation_pflegeheim_voll']),
            date_reported_import_str=date_reported,
            datum=d.datum,
            processed_update=False,
            processed_full_update=False,
        )
        return o


class VaccinationFlatFactory:

    @classmethod
    def __int(cls, input_string: str):
        if input_string == '#REF!':
            return 0
        else:
            return int(input_string)

    @classmethod
    def create_new(cls, date_reported, d, row):
        oo = VaccinationFlat(
            datum=d.datum,
            year=d.year,
            month=d.month,
            day_of_month=d.day_of_month,
            day_of_week=d.day_of_week,
            week_of_year=d.week_of_year,
            day_of_year=d.day_of_year,
            year_week=d.year_week,
            year_day_of_year=d.year_day_of_year,
            date_reported_import_str=date_reported,
            year_month=d.year_month,
            location_code="",
            location="",
            location_group="",
            processed_update=False,
            processed_full_update=False,
            #
            dosen_kumulativ=cls.__int(row['dosen_kumulativ']),
            dosen_differenz_zum_vortag=cls.__int(row['dosen_differenz_zum_vortag']),
            dosen_biontech_kumulativ=cls.__int(row['dosen_biontech_kumulativ']),
            dosen_moderna_kumulativ=cls.__int(row['dosen_moderna_kumulativ']),
            personen_erst_kumulativ=cls.__int(row['personen_erst_kumulativ']),
            personen_voll_kumulativ=cls.__int(row['personen_voll_kumulativ']),
            impf_quote_erst=float(row['impf_quote_erst']),
            impf_quote_voll=float(row['impf_quote_voll']),
            indikation_alter_dosen=cls.__int(row['indikation_alter_dosen']),
            indikation_beruf_dosen=cls.__int(row['indikation_beruf_dosen']),
            indikation_medizinisch_dosen=cls.__int(row['indikation_medizinisch_dosen']),
            indikation_pflegeheim_dosen=cls.__int(row['indikation_pflegeheim_dosen']),
            indikation_alter_erst=cls.__int(row['indikation_alter_erst']),
            indikation_beruf_erst=cls.__int(row['indikation_beruf_erst']),
            indikation_medizinisch_erst=cls.__int(row['indikation_medizinisch_erst']),
            indikation_pflegeheim_erst=cls.__int(row['indikation_pflegeheim_erst']),
            indikation_alter_voll=cls.__int(row['indikation_alter_voll']),
            indikation_beruf_voll=cls.__int(row['indikation_beruf_voll']),
            indikation_medizinisch_voll=cls.__int(row['indikation_medizinisch_voll']),
            indikation_pflegeheim_voll=cls.__int(row['indikation_pflegeheim_voll']),
        )
        return oo


class VaccinationServiceImport:
    def __init__(self, database, config: BlueprintConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Vaccination Service Import [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Vaccination Service Import [ready]")
        app.logger.debug("------------------------------------------------------------")

    def import_file(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" import Vaccination [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" import into TABLE: "+self.cfg.tablename+" <--- from FILE "+self.cfg.cvsfile_path)
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
                    app.logger.info(" import Vaccination  ... " + str(k) + " rows")
            db.session.commit()
            app.logger.info(" import Vaccination  ... " + str(k) + " rows total")
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" imported into TABLE: "+self.cfg.tablename+" <--- from FILE "+self.cfg.cvsfile_path)
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" import Vaccination [done]")
        app.logger.info("------------------------------------------------------------")
        return self
