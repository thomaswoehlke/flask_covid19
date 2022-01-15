from project.data.database import app
from project.data.database import db
from project.data_all.model.all_model import AllDateReportedFactory
from project.data_all.services.all_service_base import AllServiceBase
from project.data_all.services.all_service_config import AllServiceConfig
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


class RkiServiceUpdateFull(AllServiceBase, AllServiceMixinUpdateFull):

    def __init__(self, database, config: AllServiceConfig):
        super().__init__(database, config)
        app.logger.info(" ready [{}] {} ".format(
            self.cfg, self.__class__.__name__
        ))

    def __full_update_meldedatum(self):
        task = Notification.create(
            sector=self.cfg.category,
            task_name="__full_update_meldedatum"
        )
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [{}] full update meldedatum [begin]".format(self.cfg.category))
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
            output = " [{}] meldedatum [ {} ] full update ... {}".format(
                self.cfg.category, str(i), str(o)
            )
            output_lines.append(output)
            app.logger.info(output)
        db.session.commit()
        for output in output_lines:
            app.logger.info(output)
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [{}] full update meldedatum [done]")
        app.logger.info("------------------------------------------------------------")
        Notification.finish(task_id=task.id)
        return self

    def __full_update_altersgruppe(self):
        task = Notification.create(
            sector=self.cfg.category,
            task_name="__full_update_altersgruppe"
        )
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [{}] full update altersgruppe [begin]".format(self.cfg.category))
        app.logger.info("------------------------------------------------------------")
        RkiAltersgruppe.remove_all()
        app.logger.info("")
        i = 0
        output_lines = []
        for altersgruppe_of_import in RkiImport.get_altersgruppe_list():
            i += 1
            o = RkiAltersgruppeFactory.create_new(altersgruppe=altersgruppe_of_import)
            db.session.add(o)
            output = " [{}] altersgruppe [ {} ] full update ... {}".format(
                self.cfg.category, str(i), str(o)
            )
            output_lines.append(output)
        db.session.commit()
        for output in output_lines:
            app.logger.info(output)
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [{}] full update altersgruppe [done]".format(self.cfg.category))
        app.logger.info("------------------------------------------------------------")
        Notification.finish(task_id=task.id)
        return self

    def __full_update_bundesland(self):
        task = Notification.create(
            sector=self.cfg.category,
            task_name="__full_update_bundesland"
        )
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [{}] full update bundesland [begin]".format(self.cfg.category))
        app.logger.info("------------------------------------------------------------")
        RkiBundesland.remove_all()
        app.logger.info("")
        i = 0
        output_lines = []
        for bundesland_of_import in RkiImport.get_bundesland_list():
            i += 1
            o = RkiBundeslandFactory.create_new(bundesland_of_import)
            db.session.add(o)
            output = " [{}] bundesland [ {} ] full update ... {}".format(
                self.cfg.category, str(i), str(o)
            )
            output_lines.append(output)
        db.session.commit()
        for output in output_lines:
            app.logger.info(output)
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [{}] full update bundesland [done]".format(self.cfg.category))
        app.logger.info("------------------------------------------------------------")
        Notification.finish(task_id=task.id)
        return self

    def __full_update_landkreis(self):
        task = Notification.create(
            sector=self.cfg.category,
            task_name="__full_update_landkreis"
        )
        RkiLandkreis.remove_all()
        self.__full_update_bundesland()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [{}] __full_update_landkreis [begin]".format(self.cfg.category))
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
                output = " [{}] __full_update_landkreis [ {} ] ... {}".format(
                    self.cfg.category,
                    str(i),
                    str(o)
                )
                output_lines.append(output)
            db.session.commit()
            for output in output_lines:
                app.logger.info(output)
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [{}] __full_update_landkreis [done]".format(self.cfg.category))
        app.logger.info("------------------------------------------------------------")
        Notification.finish(task_id=task.id)
        return self

    def __full_update_data(self):
        task = Notification.create(
            sector=self.cfg.category,
            task_name="__full_update_data"
        )
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [{}] __full_update_data [begin]".format(self.cfg.category))
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
                sector=self.cfg.category,
                task_name="__full_update_data: {} ".format(str(my_meldedatum_datum)))
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
                " [{}] __full_update_data ... {} rows ... {} ( {} )".format(
                    self.cfg.category, str(i), sd, str(k)
                )
            )
            k = 0
        db.session.commit()
        app.logger.info(" [{}] __full_update_data ... {} total rows".format(
            self.cfg.category, str(i))
        )
        app.logger.info("")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [{}] __full_update_data [done]".format(self.cfg.category))
        app.logger.info("------------------------------------------------------------")
        Notification.finish(task_id=task.id)
        return self

    def __clean_dimension_tables(self):
        task = Notification.create(
            sector=self.cfg.category,
            task_name="__clean_dimension_tables"
        )
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [{}] __clean_dimension_tables [begin]".format(self.cfg.category))
        app.logger.info("------------------------------------------------------------")
        RkiData.remove_all()
        RkiMeldedatum.remove_all()
        RkiAltersgruppe.remove_all()
        RkiLandkreis.remove_all()
        RkiBundesland.remove_all()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [{}] __clean_dimension_tables [done]".format(self.cfg.category))
        app.logger.info("------------------------------------------------------------")
        Notification.finish(task_id=task.id)
        return self

    def full_update_dimension_tables(self):
        task = Notification.create(
            sector=self.cfg.category,
            task_name="full_update_dimension_tables"
        )
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [{}] full_update_dimension_tables [begin]".format(self.cfg.category))
        app.logger.info("------------------------------------------------------------")
        self.__clean_dimension_tables()
        self.__full_update_meldedatum()
        self.__full_update_altersgruppe()
        self.__full_update_landkreis()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [{}] full_update_dimension_tables [done]".format(self.cfg.category))
        app.logger.info("------------------------------------------------------------")
        Notification.finish(task_id=task.id)
        return self

    def full_update_fact_table(self):
        task = Notification.create(
            sector=self.cfg.category,
            task_name="full_update_fact_table"
        )
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [{}] full_update_fact_table [begin]".format(self.cfg.category))
        app.logger.info("------------------------------------------------------------")
        RkiData.remove_all()
        self.__full_update_data()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" [{}] full_update_fact_table [done]".format(self.cfg.category))
        app.logger.info("------------------------------------------------------------")
        Notification.finish(task_id=task.id)
        return self
