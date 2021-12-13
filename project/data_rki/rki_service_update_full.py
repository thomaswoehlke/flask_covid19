from project.app_bootstrap.database import app
from project.app_bootstrap.database import db
from project.data_all.all_task_model import Task
from project.data_all.all_model_date_reported_factory import (
    BlueprintDateReportedFactory,
)
from project.data_all.all_service_update_full_mixins import (
    AllServiceMixinUpdateFull,
)
from project.data_all.all_service_update_mixins import AllServiceMixinUpdate
from project.data_rki.rki_model_altersgruppe import RkiAltersgruppe
from project.data_rki.rki_model_altersgruppe import RkiAltersgruppeFactory
from project.data_rki.rki_model_data import RkiData
from project.data_rki.rki_model_data import RkiDataFactory
from project.data_rki.rki_model_data_location import RkiLandkreis
from project.data_rki.rki_model_data_location import RkiLandkreisFactory
from project.data_rki.rki_model_data_location_group import RkiBundesland
from project.data_rki.rki_model_data_location_group import RkiBundeslandFactory
from project.data_rki.rki_model_date_reported import RkiMeldedatum
from project.data_rki.rki_model_import import RkiImport
from project.data_rki.rki_service_update import RkiServiceUpdateBase


class RkiServiceUpdateFull(RkiServiceUpdateBase, AllServiceMixinUpdateFull):
    def __full_update_meldedatum(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] full update meldedatum [begin]")
        app.logger.info("------------------------------------------------------------")
        RkiMeldedatum.remove_all()
        i = 0
        output_lines = []
        for meldedatum_from_import in RkiImport.get_datum_of_all_import():
            # app.logger.info(datum_of_import)
            # app.logger.info(datum_of_import[0])
            i += 1
            o = BlueprintDateReportedFactory.create_new_object_for_rki_meldedatum(
                my_meldedatum=meldedatum_from_import
            )
            db.session.add(o)
            output = " [RKI] meldedatum [ " + str(i) + " ] full update ... " + str(o)
            output_lines.append(output)
            app.logger.info(output)
        db.session.commit()
        for output in output_lines:
            app.logger.info(output)
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] full update meldedatum [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __full_update_altersgruppe(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] full update altersgruppe [begin]")
        app.logger.info("------------------------------------------------------------")
        RkiAltersgruppe.remove_all()
        app.logger.info("")
        i = 0
        output_lines = []
        for altersgruppe_of_import in RkiImport.get_altersgruppe_list():
            i += 1
            o = RkiAltersgruppeFactory.create_new(altersgruppe=altersgruppe_of_import)
            db.session.add(o)
            output = " [RKI] altersgruppe [ " + str(i) + " ] full update ... " + str(o)
            output_lines.append(output)
        db.session.commit()
        for output in output_lines:
            app.logger.info(output)
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] full update altersgruppe [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __full_update_bundesland(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] full update bundesland [begin]")
        app.logger.info("------------------------------------------------------------")
        RkiBundesland.remove_all()
        app.logger.info("")
        i = 0
        output_lines = []
        for bundesland_of_import in RkiImport.get_bundesland_list():
            i += 1
            o = RkiBundeslandFactory.create_new(bundesland_of_import)
            db.session.add(o)
            output = " [RKI] bundesland [ " + str(i) + " ] full update ... " + str(o)
            output_lines.append(output)
        db.session.commit()
        for output in output_lines:
            app.logger.info(output)
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] full update bundesland [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __full_update_landkreis(self):
        RkiLandkreis.remove_all()
        self.__full_update_bundesland()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] full update landkreis [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        output_lines = []
        for bundesland in RkiBundesland.find_all():
            for landkreis_from_import in RkiImport.get_landkreis_for_bundesland(
                bundesland=bundesland.location_group
            ):
                i += 1
                # app.logger.info("landkreis_from_import: "+str(landkreis_from_import))
                my_landkreis = RkiLandkreisFactory.get_my_landkreis(
                    landkreis_from_import=landkreis_from_import
                )
                o = RkiLandkreisFactory.create_new(
                    my_landkreis=my_landkreis, bundesland=bundesland
                )
                db.session.add(o)
                output = " [RKI] landkreis [ " + str(i) + " ] full update ... " + str(o)
                output_lines.append(output)
            db.session.commit()
            for output in output_lines:
                app.logger.info(output)
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] full update landkreis [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __full_update_data(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] full update data [begin]")
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
                    my_datum=my_meldedatum_datum, my_landkreis=my_landkreis_key
                )
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
                    rki_data = RkiDataFactory.get_rki_data(
                        dict_altersgruppen,
                        my_datum,
                        my_meldedatum,
                        my_landkreis,
                        o_import,
                    )
                    o = RkiDataFactory.create_new(rki_data)
                    db.session.add(o)
                    k += 1
                    i += 1
            d += 1
            db.session.commit()
            sd = str(my_meldedatum)
            app.logger.info(
                " [RKI] full update data ... "
                + str(i)
                + " rows ... "
                + sd
                + " ("
                + str(k)
                + ")"
            )
            k = 0
        db.session.commit()
        app.logger.info(" [RKI] full update data ... " + str(i) + " total rows")
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] full update data [done]")
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
    def __get_new_dates(self):
        todo = []
        odr_list = RkiMeldedatum.find_all_as_str()
        for oi in RkiImport.get_date_reported_import_str_list():
            item = oi[0]
            # app.logger.info(" [RKI] date_reported: " + str(item))
            if item not in odr_list:
                todo.append(item)
        return todo

    def __get_new_location_groups(self):
        todo = []
        bundesland_all = RkiBundesland.find_all_as_str()
        for oi in RkiImport.get_bundesland_list():
            item = oi.bundesland
            # app.logger.info(" [RKI] location_group: " + str(item))
            if item not in bundesland_all:
                todo.append(item)
        return todo

    def __get_new_locations(self):
        todo = []
        landkreis_all = RkiLandkreis.find_all_as_str()
        for my_bundesland in RkiBundesland.find_all_as_str():
            for oi in RkiImport.get_landkreis_for_bundesland(my_bundesland):
                item = oi.landkreis
                # app.logger.info(" [RKI] location: " + str(item) + " -- " + str(my_bundesland))
                if item not in landkreis_all:
                    new_location = (oi.landkreis, oi.id_landkreis, my_bundesland)
                    todo.append(new_location)
        return todo

    def __get_new_altersgruppen(self):
        todo = []
        altersgruppe_all = RkiAltersgruppe.find_all_as_str()
        for altersgruppe in RkiImport.get_altersgruppe_list():
            item = altersgruppe[0]
            # app.logger.info(str(item))
            if item not in altersgruppe_all:
                todo.append(item)
        return todo

    def __update_date_reported(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] update date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        RkiMeldedatum.set_all_processed_update()
        for new_meldedatum in self.__get_new_dates():
            i += 1
            o = BlueprintDateReportedFactory.create_new_object_for_rki_meldedatum(
                my_meldedatum=new_meldedatum
            )
            db.session.add(o)
            db.session.commit()
            output = (
                " [RKI] update date_reported [ " + str(i) + " ] " + str(o) + " added"
            )
            app.logger.info(output)
        db.session.commit()
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] update date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_location_groups(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] update location_groups [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        RkiBundesland.set_all_processed_update()
        for new_location_group in self.__get_new_locations():
            i += 1
            o = RkiBundeslandFactory.create_new(bundesland_of_import=new_location_group)
            db.session.add(o)
            db.session.commit()
            output = (
                " [RKI] update location_group [ " + str(i) + " ] " + str(o) + " added"
            )
            app.logger.info(output)
        db.session.commit()
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] update location_groups [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_locations(self):
        self.__update_location_groups()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] update locations [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        RkiLandkreis.set_all_processed_update()
        location_group_dict = RkiBundesland.find_all_as_dict()
        for new_location in self.__get_new_locations():
            i += 1
            bundesland_str = new_location[2]
            bundesland = location_group_dict[bundesland_str]
            my_landkreis = RkiLandkreisFactory.get_my_landkreis(
                landkreis_from_import=new_location
            )
            o = RkiLandkreisFactory.create_new(
                my_landkreis=my_landkreis, bundesland=bundesland
            )
            db.session.add(o)
            db.session.commit()
            output = " [RKI] update location [ " + str(i) + " ] " + str(o) + " added"
            app.logger.info(output)
        db.session.commit()
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] update locations [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_altersgruppen(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] update altersgruppen [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        RkiAltersgruppe.set_all_processed_update()
        for new_altersgruppe in self.__get_new_altersgruppen():
            app.logger.info(" [RKI] new altersgruppe: " + str(new_altersgruppe))
            i += 1
            o = RkiAltersgruppe.RkiAltersgruppe(altersgruppe=new_altersgruppe)
            db.session.add(o)
            db.session.commit()
            output = " [RKI] altersgruppe [ " + str(i) + " ] " + str(o) + " added"
            app.logger.info(output)
        db.session.commit()
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] update altersgruppen [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_data(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] update data [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        dict_altersgruppen = RkiAltersgruppe.find_all_as_dict()
        for my_meldedatum in RkiMeldedatum.find_by_not_processed_update():
            my_meldedatum_datum = my_meldedatum.datum
            for my_landkreis in RkiLandkreis.find_all():
                my_landkreis_key = my_landkreis.location
                # app.logger.info(" [RKI] my_meldedatum: " + str(my_meldedatum) + " -- " + my_meldedatum_datum.isoformat())
                # app.logger.info("------------------------------------------------------------")
                list_imports = RkiImport.find_by_meldedatum_and_landkreis(
                    my_datum=my_meldedatum_datum, my_landkreis=my_landkreis_key
                )
                if list_imports is None:
                    app.logger.info(" [RKI] list_imports is None ")
                else:
                    nr = len(list_imports)
                    app.logger.info(" [RKI] len(list_imports): " + str(nr))
                app.logger.info(
                    "------------------------------------------------------------"
                )
                for o_import in list_imports:
                    my_datum = RkiDataFactory.row_str_to_date_fields(o_import)
                    rki_data = RkiDataFactory.get_rki_data(
                        dict_altersgruppen,
                        my_datum,
                        my_meldedatum,
                        my_landkreis,
                        o_import,
                    )
                    o = RkiDataFactory.create_new(rki_data)
                    db.session.add(o)
                    i += 1
                    if i % 500 == 0:
                        app.logger.info(" [RKI] update data ... " + str(i) + " rows")
                        db.session.commit()
            db.session.commit()
        app.logger.info(" [RKI] update data :  " + str(i) + " total rows")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] update data [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_dimension_tables(self):
        task = Task.create(sector="RKI", task_name="update_dimension_tables").read()
        self.__update_date_reported()
        self.__update_locations()
        self.__update_altersgruppen()
        Task.finish(task_id=task.id)
        return self

    def update_fact_table(self):
        task = Task.create(sector="RKI", task_name="update_fact_table").read()
        self.__update_data()
        Task.finish(task_id=task.id)
        return self

    def delete_last_day(self):
        task = Task.create(sector="RKI", task_name="delete_last_day").read()
        app.logger.debug("-----------------------------------------------------------")
        app.logger.debug(" [RKI] delete last_day [START]")
        app.logger.debug("-----------------------------------------------------------")
        app.logger.info("")
        joungest_datum = RkiMeldedatum.get_joungest_datum()
        app.logger.info(" [RKI] joungest_datum:" + str(joungest_datum))
        app.logger.info("")
        app.logger.info(" [RKI] RkiData.get_data_for_one_day(joungest_datum):")
        app.logger.info("")
        i = 0
        output_lines = []
        for data in RkiData.find_by_date_reported(joungest_datum):
            i += 1
            line = " [RKI] to be deleted [ " + str(i) + " ] " + str(data)
            output_lines.append(line)
        for line in output_lines:
            app.logger.info(line)
        app.logger.info("")
        app.logger.info(" [RKI] RkiData.delete_data_for_one_day(joungest_datum)")
        app.logger.info("")
        RkiData.delete_data_for_one_day(joungest_datum)
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] delete last_day [DONE]")
        app.logger.info("------------------------------------------------------------")
        Task.finish(task_id=task.id)
        return self
