from project.app_bootstrap.database import app
from project.app_bootstrap.database import db
from project.data_all.all_model_date_reported_factory import (
    BlueprintDateReportedFactory,
)
from project.data_all.framework.services.all_service_update_full_mixins import (
    AllServiceMixinUpdateFull,
)
from project.data_all.task.all_task_model import Task
from project.data_rki.model.rki_model_altersgruppe import RkiAltersgruppe
from project.data_rki.model.rki_model_altersgruppe import RkiAltersgruppeFactory
from project.data_rki.model.rki_model_data import RkiData
from project.data_rki.model.rki_model_data import RkiDataFactory
from project.data_rki.model.rki_model_data_location import RkiLandkreis
from project.data_rki.model.rki_model_data_location import RkiLandkreisFactory
from project.data_rki.model.rki_model_data_location_group import RkiBundesland
from project.data_rki.model.rki_model_data_location_group import RkiBundeslandFactory
from project.data_rki.model.rki_model_date_reported import RkiMeldedatum
from project.data_rki.model.rki_model_import import RkiImport
from project.data_rki.services.rki_service_update import RkiServiceUpdateBase


class RkiServiceUpdateFull(RkiServiceUpdateBase, AllServiceMixinUpdateFull):
    def __full_update_meldedatum(self):
        task = Task.create(sector="RKI", task_name="__full_update_meldedatum").read()
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
        Task.finish(task_id=task.id)
        return self

    def __full_update_altersgruppe(self):
        task = Task.create(sector="RKI", task_name="__full_update_altersgruppe").read()
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
        Task.finish(task_id=task.id)
        return self

    def __full_update_bundesland(self):
        task = Task.create(sector="RKI", task_name="__full_update_bundesland").read()
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
        Task.finish(task_id=task.id)
        return self

    def __full_update_landkreis(self):
        task = Task.create(sector="RKI", task_name="__full_update_landkreis").read()
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
        Task.finish(task_id=task.id)
        return self

    def __full_update_data(self):
        task = Task.create(sector="RKI", task_name="__full_update_data").read()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] full update [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info("START: RkiData.remove_all()")
        RkiData.remove_all()
        app.logger.info("DONE: RkiData.remove_all()")
        app.logger.info("------------------------------------------------------------")
        i = 0
        d = 0
        k = 0
        c = 0
        dict_altersgruppen = RkiAltersgruppe.find_all_as_dict()
        # for l_key in locations.keys():
        #     app.logger.info(" location: " + str(l_key) + " -> " + str(locations[l_key]))
        # app.logger.info("------------------------------------------------------------")
        for my_meldedatum in RkiMeldedatum.find_all():
            my_meldedatum_datum = my_meldedatum.datum
            task_meldedatum = Task.create(
                sector="RKI",
                task_name="__full_update_data: "\
                          +str(my_meldedatum_datum)).read()
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
                    c += 1
                    if (c % 5000) == 0:
                        db.session.commit()
                db.session.commit()
            d += 1
            sd = str(my_meldedatum)
            Task.finish(task_id=task_meldedatum.id)
            app.logger.info(
                " [RKI] full update ... "
                + str(i)
                + " rows ... "
                + sd
                + " ("
                + str(k)
                + ")"
            )
            k = 0
        db.session.commit()
        app.logger.info(" [RKI] full update ... " + str(i) + " total rows")
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] full update [done]")
        app.logger.info("------------------------------------------------------------")
        Task.finish(task_id=task.id)
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
