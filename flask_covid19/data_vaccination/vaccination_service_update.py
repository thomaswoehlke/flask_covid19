from app_config.database import db, app # , cache
from data_all.all_config import BlueprintConfig
from data_all.all_service_mixins import AllServiceMixinUpdate, AllServiceMixinUpdateFull
from app_web.web_model_factory import BlueprintDateReportedFactory
from data_vaccination.vaccination_model_import import VaccinationImport
from data_vaccination.vaccination_model import VaccinationDateReported
from data_vaccination.vaccination_model import VaccinationData


class VaccinationServiceUpdateBase:
    def __init__(self, database, config: BlueprintConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Vaccination Service Update [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" [Vaccination] Service Update [ready] ")
        app.logger.debug("------------------------------------------------------------")


class VaccinationServiceUpdateFull(VaccinationServiceUpdateBase, AllServiceMixinUpdateFull):

    def __full_update_date_reported(self):
        app.logger.info(" [Vaccination] full update date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        VaccinationDateReported.remove_all()
        date_reported_list = VaccinationImport.get_date_reported_as_array()
        i = 0
        for one_date_reported in date_reported_list:
            i += 1
            o = BlueprintDateReportedFactory.create_new_object_for_vaccination(my_date_reported=one_date_reported)
            db.session.add(o)
            output = "  [Vaccination] full update date_reported [ " + str(i) + " ] " + str(o)
            app.logger.info(output)
        db.session.commit()
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [Vaccination] full update date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __full_update_fact_table(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [Vaccination] full update fact_table [begin]")
        app.logger.info("------------------------------------------------------------")
        VaccinationData.remove_all()
        result_date_rep = VaccinationImport.get_date_rep()
        i = 0
        for item_date_rep, in result_date_rep:
            d = VaccinationDateReported.get_by_datum(
                datum=item_date_rep
            )
            for item_import in VaccinationImport.find_by_datum(d.date_reported_import_str):
                o = VaccinationData(
                    date_reported=d,
                    dosen_kumulativ=item_import.dosen_kumulativ,
                    dosen_differenz_zum_vortag=item_import.dosen_differenz_zum_vortag,
                    dosen_biontech_kumulativ=item_import.dosen_biontech_kumulativ,
                    dosen_moderna_kumulativ=item_import.dosen_moderna_kumulativ,
                    personen_erst_kumulativ=item_import.personen_erst_kumulativ,
                    personen_voll_kumulativ=item_import.personen_voll_kumulativ,
                    impf_quote_erst=item_import.impf_quote_erst,
                    impf_quote_voll=item_import.impf_quote_voll,
                    indikation_alter_dosen=item_import.indikation_alter_dosen,
                    indikation_beruf_dosen=item_import.indikation_beruf_dosen,
                    indikation_medizinisch_dosen=item_import.indikation_medizinisch_dosen,
                    indikation_pflegeheim_dosen=item_import.indikation_pflegeheim_dosen,
                    indikation_alter_erst=item_import.indikation_alter_erst,
                    indikation_beruf_erst=item_import.indikation_beruf_erst,
                    indikation_medizinisch_erst=item_import.indikation_medizinisch_erst,
                    indikation_pflegeheim_erst=item_import.indikation_pflegeheim_erst,
                    indikation_alter_voll=item_import.indikation_alter_voll,
                    indikation_beruf_voll=item_import.indikation_beruf_voll,
                    indikation_medizinisch_voll=item_import.indikation_medizinisch_voll,
                    indikation_pflegeheim_voll=item_import.indikation_pflegeheim_voll,
                    processed_update=False,
                    processed_full_update=True,
                )
                item_import.processed_full_update = True
                db.session.add(o)
                i += 1
                if i % 500 == 0:
                    app.logger.info(" [Vaccination] full update data ... " + str(i) + " rows")
                    db.session.commit()
        db.session.commit()
        app.logger.info(" [Vaccination] full update data ... " + str(i) + " rows total")
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [Vaccination] full update fact_table [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def full_update_dimension_tables(self):
        VaccinationData.remove_all()
        self.__full_update_date_reported()
        return self

    def full_update_fact_table(self):
        self.__full_update_fact_table()
        return self


class VaccinationServiceUpdate(VaccinationServiceUpdateBase, AllServiceMixinUpdate):

    def __get_new_dates(self):
        todo = []
        odr_list = VaccinationDateReported.find_all_as_str()
        for oi in VaccinationImport.get_date_reported_import_str_list():
            item = oi[0]
            app.logger.info("o: " + str(item))
            if item not in odr_list:
                todo.append(item)
        return todo

    def __update_date_reported(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [Vaccination] update date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        VaccinationDateReported.set_all_processed_update()
        date_reported_list = VaccinationImport.get_date_reported_as_array()
        i = 0
        for one_date_reported in date_reported_list:
            i += 1
            output = " [Vaccination] date_reported [ " + str(i) + " ] " + str(one_date_reported) + " added"
            o = BlueprintDateReportedFactory.create_new_object_for_vaccination(one_date_reported)
            db.session.add(o)
            app.logger.info(output)
        db.session.commit()
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [Vaccination] update date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_fact_table(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [Vaccination] update fact_table [begin]")
        app.logger.info("------------------------------------------------------------")
        result_date_rep = VaccinationImport.get_daterep_missing_in_vaccination_data()
        i = 0
        for item_date_rep in result_date_rep:
            date_reported = VaccinationDateReported.get_by_date_reported(item_date_rep)
            for item_data_import in VaccinationImport.find_by_datum(item_date_rep):
                o = VaccinationData(
                    date_reported=date_reported,
                    dosen_kumulativ=item_data_import.dosen_kumulativ,
                    dosen_differenz_zum_vortag=item_data_import.dosen_differenz_zum_vortag,
                    dosen_biontech_kumulativ=item_data_import.dosen_biontech_kumulativ,
                    dosen_moderna_kumulativ=item_data_import.dosen_moderna_kumulativ,
                    personen_erst_kumulativ=item_data_import.personen_erst_kumulativ,
                    personen_voll_kumulativ=item_data_import.personen_voll_kumulativ,
                    impf_quote_erst=item_data_import.impf_quote_erst,
                    impf_quote_voll=item_data_import.impf_quote_voll,
                    indikation_alter_dosen=item_data_import.indikation_alter_dosen,
                    indikation_beruf_dosen=item_data_import.indikation_beruf_dosen,
                    indikation_medizinisch_dosen=item_data_import.indikation_medizinisch_dosen,
                    indikation_pflegeheim_dosen=item_data_import.indikation_pflegeheim_dosen,
                    indikation_alter_erst=item_data_import.indikation_alter_erst,
                    indikation_beruf_erst=item_data_import.indikation_beruf_erst,
                    indikation_medizinisch_erst=item_data_import.indikation_medizinisch_erst,
                    indikation_pflegeheim_erst=item_data_import.indikation_pflegeheim_erst,
                    indikation_alter_voll=item_data_import.indikation_alter_voll,
                    indikation_beruf_voll=item_data_import.indikation_beruf_voll,
                    indikation_medizinisch_voll=item_data_import.indikation_medizinisch_voll,
                    indikation_pflegeheim_voll=item_data_import.indikation_pflegeheim_voll,
                    processed_update=True,
                    processed_full_update=False,
                )
                db.session.add(o)
                i += 1
                if i % 500 == 0:
                    app.logger.info(" [Vaccination] update fact_table ... " + str(i) + " rows")
                    db.session.commit()
        db.session.commit()
        app.logger.info(" [Vaccination] update fact_table ... " + str(i) + " rows total")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [Vaccination] update fact_table [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_dimension_tables(self):
        self.__update_date_reported()
        return self

    def update_fact_table(self):
        self.__update_fact_table()
        return self

    def delete_last_day(self):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" VaccinationServiceUpdate.delete_last_day [START]")
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" not implemented")
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" VaccinationServiceUpdate.delete_last_day [DONE]")
        app.logger.debug("------------------------------------------------------------")
        return self


