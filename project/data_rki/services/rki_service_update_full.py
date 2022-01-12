from project.data.database import app
from project.data.database import db
from project.data_all.model.all_model_date_reported_factory import (
    AllDateReportedFactory,
)
from project.data_all.services.all_service_mixins import AllServiceMixinUpdateFull

from project.data_all_notifications.notifications_model import Notification
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
        task = Notification.create(sector="RKI", task_name="__full_update_meldedatum")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] full update meldedatum [begin]")
        app.logger.info("------------------------------------------------------------")
        RkiMeldedatum.remove_all()
        i = 0
        output_lines = []
        for meldedatum_from_import in RkiImport.get_datum_of_all_import():
            i += 1
            o = AllDateReportedFactory.create_new_object_for_rki_meldedatum(
                my_meldedatum=meldedatum_from_import
            )
            db.session.add(o)
            output = " [RKI] meldedatum [ {} ] full update ... {}".format(
                str(i), str(o)
            )
            output_lines.append(output)
            app.logger.info(output)
        db.session.commit()
        for output in output_lines:
            app.logger.info(output)
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] full update meldedatum [done]")
        app.logger.info("------------------------------------------------------------")
        Notification.finish(task_id=task.id)
        return self

    def __full_update_altersgruppe(self):
        task = Notification.create(sector="RKI", task_name="__full_update_altersgruppe")
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
            output = " [RKI] altersgruppe [ {} ] full update ... {}".format(
                str(i), str(o)
            )
            output_lines.append(output)
        db.session.commit()
        for output in output_lines:
            app.logger.info(output)
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] full update altersgruppe [done]")
        app.logger.info("------------------------------------------------------------")
        Notification.finish(task_id=task.id)
        return self

    def __full_update_bundesland(self):
        task = Notification.create(sector="RKI", task_name="__full_update_bundesland")
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
            output = " [RKI] bundesland [ {} ] full update ... {}".format(
                str(i), str(o)
            )
            output_lines.append(output)
        db.session.commit()
        for output in output_lines:
            app.logger.info(output)
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] full update bundesland [done]")
        app.logger.info("------------------------------------------------------------")
        Notification.finish(task_id=task.id)
        return self

    def __full_update_landkreis(self):
        task = Notification.create(sector="RKI", task_name="__full_update_landkreis")
        RkiLandkreis.remove_all()
        self.__full_update_bundesland()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] __full_update_landkreis [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        output_lines = []
        for bundesland in RkiBundesland.find_all():
            for landkreis_from_import in RkiImport.get_landkreis_for_bundesland(
                bundesland=bundesland.location_group
            ):
                i += 1
                my_landkreis = RkiLandkreisFactory.get_my_landkreis(
                    landkreis_from_import=landkreis_from_import
                )
                o = RkiLandkreisFactory.create_new(
                    my_landkreis=my_landkreis, bundesland=bundesland
                )
                db.session.add(o)
                output = " [RKI] __full_update_landkreis [ {} ] ... {}".format(
                    str(i),
                    str(o)
                )
                output_lines.append(output)
            db.session.commit()
            for output in output_lines:
                app.logger.info(output)
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] __full_update_landkreis [done]")
        app.logger.info("------------------------------------------------------------")
        Notification.finish(task_id=task.id)
        return self

    def __full_update_data(self):
        task = Notification.create(sector="RKI", task_name="__full_update_data")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] __full_update_data [begin]")
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
        for my_meldedatum in RkiMeldedatum.find_all():
            my_meldedatum_datum = my_meldedatum.datum
            task_meldedatum = Notification.create(
                sector="RKI",
                task_name="__full_update_data: {} ".format(str(my_meldedatum_datum)))\
                .read()
            for my_landkreis in RkiLandkreis.find_all():
                my_landkreis_key = my_landkreis.location
                list_imports = RkiImport.find_by_meldedatum_and_landkreis(
                    my_datum=my_meldedatum_datum, my_landkreis=my_landkreis_key
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
                    k += 1
                    i += 1
                    c += 1
                    if (c % 5000) == 0:
                        db.session.commit()
                db.session.commit()
            d += 1
            sd = str(my_meldedatum)
            Notification.finish(task_id=task_meldedatum.id)
            app.logger.info(
                " [RKI] __full_update_data ... {} rows ... {} ( {} )".format(
                    str(i), sd, str(k)
                )
            )
            k = 0
        db.session.commit()
        app.logger.info(" [RKI] __full_update_data ... {} total rows".format(str(i)))
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] __full_update_data [done]")
        app.logger.info("------------------------------------------------------------")
        Notification.finish(task_id=task.id)
        return self

    def __clean_dimension_tables(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] __clean_dimension_tables [begin]")
        app.logger.info("------------------------------------------------------------")
        RkiData.remove_all()
        RkiMeldedatum.remove_all()
        RkiAltersgruppe.remove_all()
        RkiLandkreis.remove_all()
        RkiBundesland.remove_all()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] __clean_dimension_tables [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def full_update_dimension_tables(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] full_update_dimension_tables [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__clean_dimension_tables()
        self.__full_update_meldedatum()
        self.__full_update_altersgruppe()
        self.__full_update_landkreis()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] full_update_dimension_tables [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def full_update_fact_table(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] full_update_fact_table [begin]")
        app.logger.info("------------------------------------------------------------")
        RkiData.remove_all()
        self.__full_update_data()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [RKI] full_update_fact_table [done]")
        app.logger.info("------------------------------------------------------------")
        return self
