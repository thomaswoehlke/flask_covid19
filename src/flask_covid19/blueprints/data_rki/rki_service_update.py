from database import db, app#, cache

from flask_covid19.blueprints.app_all.all_config import BlueprintConfig
from flask_covid19.blueprints.app_all.all_service_mixins import AllServiceMixinUpdate, AllServiceMixinUpdateFull
from flask_covid19.blueprints.app_web.web_model_factory import BlueprintDateReportedFactory
from flask_covid19.blueprints.data_rki.rki_model import RkiData, RkiMeldedatum, RkiAltersgruppe, \
    RkiBundesland, RkiLandkreis
from flask_covid19.blueprints.data_rki.rki_model_factories import RkiBundeslandFactory, RkiLandkreisFactory, \
    RkiDataFactory
from flask_covid19.blueprints.data_rki.rki_model_import import RkiImport


class RkiServiceUpdateBase:
    def __init__(self, database, config: BlueprintConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Service Update [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Service Update [ready]")


class RkiServiceUpdateFull(RkiServiceUpdateBase, AllServiceMixinUpdateFull):

    def __full_update_meldedatum(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" RkiServiceUpdateFull.__full_update_meldedatum [begin]")
        app.logger.info("------------------------------------------------------------")
        RkiMeldedatum.remove_all()
        i = 0
        output_lines = []
        for meldedatum_from_import in RkiImport.get_meldedatum_list():
            # app.logger.info(datum_of_import)
            # app.logger.info(datum_of_import[0])
            i += 1
            my_meldedatum_from_import = meldedatum_from_import[0]
            o = BlueprintDateReportedFactory.create_new_object_for_rki_meldedatum(
                my_meldedatum=my_meldedatum_from_import)
            db.session.add(o)
            output = "  [ " + str(i) + " ] full update RKI meldedatum ... " + str(o)
            output_lines.append(output)
            app.logger.info(output)
        db.session.commit()
        for output in output_lines:
            app.logger.info(output)
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" RkiServiceUpdateFull.__full_update_meldedatum [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __full_update_altersgruppe(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" RkiServiceUpdateFull.__full_update_altersgruppe [begin]")
        app.logger.info("------------------------------------------------------------")
        RkiAltersgruppe.remove_all()
        app.logger.info("")
        i = 0
        output_lines = []
        for altersgruppe_of_import in RkiImport.get_altersgruppe_list():
            i += 1
            my_altersgruppe = altersgruppe_of_import[0]
            o = RkiAltersgruppe(
                altersgruppe=my_altersgruppe,
                processed_update=False,
                processed_full_update=False,
            )
            db.session.add(o)
            output = "  [ " + str(i) + " ] full update RKI altersgruppe ... " + str(o)
            output_lines.append(output)
        db.session.commit()
        for output in output_lines:
            app.logger.info(output)
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" RkiServiceUpdateFull.__full_update_altersgruppe [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __full_update_bundesland(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" RkiServiceUpdateFull.__full_update_bundesland [begin]")
        app.logger.info("------------------------------------------------------------")
        RkiBundesland.remove_all()
        app.logger.info("")
        i = 0
        output_lines = []
        for bundesland_of_import in RkiImport.get_bundesland_list():
            i += 1
            o = RkiBundeslandFactory.create_new(bundesland_of_import)
            db.session.add(o)
            output = "  [ " + str(i) + " ] full update RKI bundesland ... " + str(o)
            output_lines.append(output)
        db.session.commit()
        for output in output_lines:
            app.logger.info(output)
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" RkiServiceUpdateFull.__full_update_bundesland [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __full_update_landkreis(self):
        RkiLandkreis.remove_all()
        self.__full_update_bundesland()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" RkiServiceUpdateFull.__full_update_landkreis [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        output_lines = []
        for bundesland in RkiBundesland.find_all():
            for landkreis_from_import in RkiImport.get_landkreis_for_bundesland(bundesland=bundesland.location_group):
                i += 1
                # app.logger.info("landkreis_from_import: "+str(landkreis_from_import))
                my_landkreis = RkiLandkreisFactory.get_my_landkreis(landkreis_from_import=landkreis_from_import)
                o = RkiLandkreisFactory.create_new(my_landkreis=my_landkreis, bundesland=bundesland)
                db.session.add(o)
                output = "  [ " + str(i) + " ] full update RKI landkreis ... " + str(o)
                output_lines.append(output)
            db.session.commit()
            for output in output_lines:
                app.logger.info(output)
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" RkiServiceUpdateFull.__full_update_landkreis [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __full_update_data(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" RkiServiceUpdateFull.__full_update_data [begin]")
        app.logger.info("------------------------------------------------------------")
        RkiData.remove_all()
        i = 0
        d = 0
        k = 0
        dict_altersgruppen = RkiAltersgruppe.find_all_as_dict()
        # for l_key in locations.keys():
        #     app.logger.info(" location: " + str(l_key) + " -> " + str(locations[l_key]))
        # app.logger.info("------------------------------------------------------------")
        for my_meldedatum in RkiMeldedatum.find_all():
            my_meldedatum_datum = my_meldedatum.datum
            for my_landkreis in RkiLandkreis.find_all():
                my_landkreis_key = my_landkreis.location
                # app.logger.info(" my_meldedatum: " + str(my_meldedatum) + " " + d.isoformat())
                # app.logger.info("------------------------------------------------------------")
                list_imports = RkiImport.find_by_meldedatum_and_landkreis(
                    my_datum=my_meldedatum_datum,
                    my_landkreis=my_landkreis_key)
                # if l_imports is None:
                #    app.logger.info("list_imports is None ")
                # else:
                #    nr = len(list_imports)
                #    app.logger.info("len(list_imports): " + str(nr))
                # app.logger.info("------------------------------------------------------------")
                for o_import in list_imports:
                    # app.logger.info("o_import.landkreis " + o_import.landkreis)
                    # app.logger.info(str(my_landkreis))
                    my_datum = RkiDataFactory.row_str_to_date_fields(o_import)
                    rki_data = RkiDataFactory.get_rki_data(dict_altersgruppen, my_datum, my_meldedatum, my_landkreis, o_import)
                    o = RkiDataFactory.create_new(rki_data)
                    db.session.add(o)
                    k += 1
                    i += 1
            d += 1
            db.session.commit()
            sd = str(my_meldedatum)
            app.logger.info(" full update RKI data ... " + str(i) + " rows ... " + sd + " (" + str(k) + ")")
            k = 0
        db.session.commit()
        app.logger.info(" full update RKI data ... " + str(i) + " total rows")
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" RkiServiceUpdateFull.__full_update_data [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __clean_dimension_tables(self):
        RkiData.remove_all()
        RkiMeldedatum.remove_all()
        RkiAltersgruppe.remove_all()
        RkiLandkreis.remove_all()
        RkiBundesland.remove_all()
        return self

    def full_update_dimension_tables(self):
        self.__clean_dimension_tables()
        self.__full_update_meldedatum()
        self.__full_update_altersgruppe()
        self.__full_update_landkreis()
        return self

    def full_update_fact_table(self):
        RkiData.remove_all()
        self.__full_update_data()
        return self


class RkiServiceUpdate(RkiServiceUpdateBase, AllServiceMixinUpdate):

    def __who_import_get_new_dates_reported(self):
        new_dates_reported = []
        list_datum_from_data = RkiData.get_datum_of_all_data()
        list_datum_from_import = RkiImport.get_datum_of_all_import()
        for item_datum_from_import in list_datum_from_import:
            if item_datum_from_import not in list_datum_from_data:
                new_dates_reported.append(item_datum_from_import)
        return new_dates_reported

    def __update_date_reported(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" RkiServiceUpdate.__update_date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        for aktualisierung in RkiImport.get_aktualisierungen_as_array():
            i += 1
            output = " [ " + str(i) + " ] " + aktualisierung
            c = RkiMeldedatum.find_by_date_reported(aktualisierung)
            if c is None:
                o = RkiMeldedatum.create_new_object_factory(aktualisierung=aktualisierung)
                db.session.add(o)
                db.session.commit()
                output += " added"
            else:
                output += " NOT added " + str(c.id)
            app.logger.info(output)
        db.session.commit()
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" RkiServiceUpdate.__update_date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_data(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" RkiServiceUpdate.__update_data [begin]")
        app.logger.info("------------------------------------------------------------")
        aktualisierungen_from_import = RkiImport.get_aktualisierungen_as_array()
        i = 0
        dict_altersgruppen = RkiAltersgruppe.find_all_as_dict()
        my_new_my_meldedatum_list = RkiMeldedatum.find_all()
        for my_meldedatum in my_new_my_meldedatum_list:
            my_meldedatum_datum = my_meldedatum.datum
            for my_landkreis in RkiLandkreis.find_all():
                my_landkreis_key = my_landkreis.location_type + " " + my_landkreis.location
                # app.logger.info(" my_meldedatum: " + str(my_meldedatum) + " " + d.isoformat())
                # app.logger.info("------------------------------------------------------------")
                list_imports = RkiImport.find_by_meldedatum_and_landkreis(
                    my_datum=my_meldedatum_datum,
                    my_landkreis=my_landkreis_key)
                # if l_imports is None:
                #    app.logger.info("list_imports is None ")
                # else:
                #    nr = len(list_imports)
                #    app.logger.info("len(list_imports): " + str(nr))
                # app.logger.info("------------------------------------------------------------")
                my_datenstand_date_datum = None
                my_ref_datum_datum = None
                for o_import in list_imports:
                    my_datum = RkiDataFactory.row_str_to_date_fields(o_import)
                    rki_data = RkiDataFactory.get_rki_data(
                        dict_altersgruppen, my_datum, my_meldedatum, my_landkreis, o_import)
                    o = RkiDataFactory.create_new(rki_data)
                    db.session.add(o)
                    i += 1
                    if i % 500 == 0:
                        app.logger.info(" update RkiBundeslaender short ... "+str(i)+" rows")
                        db.session.commit()
            db.session.commit()
        app.logger.info(" update RkiBundeslaender short :  "+str(i)+" total rows")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" RkiServiceUpdate.__update_data [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_dimension_tables(self):
        self.__update_date_reported()
        return self

    def update_fact_table(self):
        self.__update_data()
        return self

    def delete_last_day(self):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RkiTestService.delete_last_day() [START]")
        app.logger.debug("------------------------------------------------------------")
        joungest_datum = RkiMeldedatum.get_joungest_datum()
        app.logger.info("joungest_datum:")
        app.logger.info(joungest_datum)
        app.logger.info("RkiData.get_data_for_one_day(joungest_datum):")
        i = 0
        for data in RkiData.find_by_date_reported(joungest_datum):
            i += 1
            line = "Owid: to be deleted | " + str(i) + " | " + str(data.date_reported) + " | " + str(data.country) + " | "
            app.logger.info(line)
        app.logger.info("RkiData.delete_data_for_one_day(joungest_datum)")
        RkiData.delete_data_for_one_day(joungest_datum)
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RkiTestService.delete_last_day() [DONE]")
        app.logger.debug("------------------------------------------------------------")
        return self
