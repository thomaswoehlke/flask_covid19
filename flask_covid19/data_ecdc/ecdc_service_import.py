import csv
# import psycopg2

from flask_covid19_conf.database import db, app
from flask_covid19_app_all.all_service_mixins import AllServiceMixinImport
from flask_covid19_app_all.all_config import BlueprintConfig
from flask_covid19_app_web.web_model_factory import BlueprintDateReportedFactory
from data_ecdc.ecdc_model_import import EcdcImport, EcdcFlat


class EcdcImportFactory:

    @classmethod
    def create_new(cls, date_reported, d, row):
        o = EcdcImport(
            date_reported_import_str=d.date_reported_import_str,
            datum=d.datum,
            processed_update=False,
            processed_full_update=False,
            date_rep=date_reported,
            day=row['day'],
            month=row['month'],
            year=row['year'],
            cases=row['cases'],
            deaths=row['deaths'],
            countries_and_territories=row['countriesAndTerritories'],
            geo_id=row['geoId'],
            country_territory_code=row['countryterritoryCode'],
            pop_data_2019=row['popData2019'],
            continent_exp=row['continentExp'],
            cumulative_number_for_14_days_of_covid19_cases_per_100000
            =row['Cumulative_number_for_14_days_of_COVID-19_cases_per_100000'],
        )
        return o


class EcdcFlatFactory:

    @classmethod
    def create_new(cls, d, row):
        oo = EcdcFlat(
            date_reported_import_str=d.date_reported_import_str,
            datum=d.datum,
            year=d.year,
            month=d.month,
            day_of_month=d.day_of_month,
            day_of_week=d.day_of_week,
            week_of_year=d.week_of_year,
            day_of_year=d.day_of_year,
            year_week=d.year_week,
            year_day_of_year=d.year_day_of_year,
            year_month=d.year_month,
            location=row['countriesAndTerritories'],
            location_group=row['continentExp'],
            location_code=row['countryterritoryCode'],
            processed_update=False,
            processed_full_update=False,
            #
            cases=int(row['cases']),
            deaths=int(row['deaths']),
            geo_id=row['geoId'],
            pop_data_2019=row['popData2019'],
            cumulative_number_for_14_days_of_covid19_cases_per_100000
            =0.0 if '' == row['Cumulative_number_for_14_days_of_COVID-19_cases_per_100000'] else float(row['Cumulative_number_for_14_days_of_COVID-19_cases_per_100000']),
        )
        return oo


class EcdcServiceImport(AllServiceMixinImport):
    def __init__(self, database, config: BlueprintConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" ECDC Service Import [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" ECDC Service Import [ready] ")
        app.logger.debug("------------------------------------------------------------")

    def import_file(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" import ECDC [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" import into TABLE: "+self.cfg.tablename+" <--- from FILE "+self.cfg.cvsfile_path)
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
                    app.logger.info("  import ECDC  ...  " + str(k) + " rows")
                if self.cfg.reached_limit_import_for_testing(row_number=k):
                    break
            db.session.commit()
            app.logger.info("  import ECDC  ...  " + str(k) + " rows total")
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" imported into TABLE: "+self.cfg.tablename+" <--- from FILE "+self.cfg.cvsfile_path)
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" import ECDC [done]")
        app.logger.info("------------------------------------------------------------")
        return self
