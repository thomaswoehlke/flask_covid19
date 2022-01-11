from datetime import date

from sqlalchemy import and_, Sequence
from sqlalchemy.orm import Bundle

from project.app_bootstrap.database import db
from project.app_bootstrap.database import items_per_page
from project.data_all.all_model import AllImport
from project.data_all.all_model_date_reported_factory import (
    AllDateReportedFactory,
)


class RkiImport(AllImport):
    __tablename__ = "rki_import"
    __mapper_args__ = {"concrete": True}

    def __repr__(self):
        return "{}({})".format(
            self.__class__.__name__,
            self.fid
        )

    id_seq = Sequence('rki_import_id_seq')
    id = db.Column(db.Integer,
                   id_seq,
                   server_default=id_seq.next_value(),
                   primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    date_reported_import_str = db.Column(db.String(255), nullable=False)
    datum = db.Column(db.Date, nullable=False)
    fid = db.Column(db.String(255), nullable=False)
    id_bundesland = db.Column(db.String(255), nullable=False)
    bundesland = db.Column(db.String(255), nullable=False)
    landkreis = db.Column(db.String(255), nullable=False)
    altersgruppe = db.Column(db.String(255), nullable=False)
    geschlecht = db.Column(db.String(255), nullable=False)
    anzahl_fall = db.Column(db.String(255), nullable=False)
    anzahl_todesfall = db.Column(db.String(255), nullable=False)
    meldedatum = db.Column(db.String(255), nullable=False)
    id_landkreis = db.Column(db.String(255), nullable=False)
    datenstand = db.Column(db.String(255), nullable=False)
    neuer_fall = db.Column(db.String(255), nullable=False)
    neuer_todesfall = db.Column(db.String(255), nullable=False)
    ref_datum = db.Column(db.String(255), nullable=False)
    neu_genesen = db.Column(db.String(255), nullable=False)
    anzahl_genesen = db.Column(db.String(255), nullable=False)
    ist_erkrankungsbeginn = db.Column(db.String(255), nullable=False)
    altersgruppe2 = db.Column(db.String(255), nullable=False)

    @classmethod
    def count(cls):
        return db.session.query(cls).count()

    @classmethod
    def get_all(cls, page: int):
        return db.session.query(cls).paginate(page, per_page=items_per_page)

    @classmethod
    def get_date_datenstand_of_all_import(cls):
        dates_reported = []
        bu = Bundle("datenstand", cls.datenstand)
        for meldedatum in (
            db.session.query(bu).distinct().order_by(cls.datenstand.desc())
        ):
            item = meldedatum[0][0]
            if item not in dates_reported:
                dates_reported.append(item)
        return dates_reported

    @classmethod
    def get_date_ref_datum_of_all_import(cls):
        dates_reported = []
        bu = Bundle("ref_datum", cls.ref_datum)
        for meldedatum in (
            db.session.query(bu).distinct().order_by(cls.ref_datum.desc())
        ):
            item = meldedatum[0][0]
            if item not in dates_reported:
                dates_reported.append(item)
        return dates_reported

    @classmethod
    def get_datum_of_all_import(cls):
        dates_reported = []
        bu = Bundle("meldedatum", cls.meldedatum)
        for meldedatum in db.session.query(bu).distinct():
            item = meldedatum[0][0]
            if item not in dates_reported:
                dates_reported.append(item)
        return dates_reported

    @classmethod
    def get_meldedatum_list(cls):
        return db.session.query(cls.meldedatum).distinct().all()

    @classmethod
    def get_date_reported_import_str_list(cls):
        date_reported_import_str_list = []
        bu = Bundle("date_reported_import_str", cls.date_reported_import_str)
        oi_list = (
            db.session.query(bu)
            .distinct()
            .order_by(cls.date_reported_import_str.desc())
        )
        for date_reported_import_str_row in oi_list:
            item = date_reported_import_str_row[0]
            if item not in date_reported_import_str_list:
                date_reported_import_str_list.append(item)
        return date_reported_import_str_list

    @classmethod
    def get_bundesland_list(cls):
        bundesland_list = []
        bu = Bundle("bundesland", cls.bundesland, cls.id_bundesland)
        for bundesland_row in db.session.query(bu).distinct():
            item = bundesland_row[0]
            if item not in bundesland_list:
                bundesland_list.append(item)
        return bundesland_list

    @classmethod
    def get_altersgruppe_list(cls):
        altersgruppe_list = []
        bu = Bundle("altersgruppe", cls.altersgruppe)
        for altersgruppe_row in db.session.query(bu).distinct():
            item = altersgruppe_row[0][0]
            if item not in altersgruppe_list:
                altersgruppe_list.append(item)
        return altersgruppe_list

    @classmethod
    def get_landkreis_for_bundesland(cls, bundesland: str):
        return (
            db.session.query(cls.landkreis, cls.id_landkreis)
            .filter(cls.bundesland == bundesland)
            .distinct()
            .order_by(cls.landkreis.asc())
            .all()
        )

    @classmethod
    def find_by_datum(cls, my_datum: date):
        return (
            db.session.query(cls)
            .filter(cls.datum == my_datum)
            .order_by(cls.landkreis.asc())
            .all()
        )

    @classmethod
    def find_by_meldedatum_and_landkreis(cls, my_datum: date, my_landkreis: str):
        return (
            db.session.query(cls)
            .filter(and_((cls.datum == my_datum), (cls.landkreis == my_landkreis)))
            .order_by(cls.landkreis.asc())
            .all()
        )


class RkiServiceImportFactory:
    @classmethod
    def row_str_to_date_fields(cls, row):
        my_datum = {
            "d_meldedatum_str": row["Meldedatum"],
            "d_ref_datum_str": row["Refdatum"],
            "d_datenstand_str": row["Datenstand"],
        }
        my_datum[
            "d_meldedatum"
        ] = AllDateReportedFactory.create_new_object_for_rki_meldedatum(
            my_meldedatum=my_datum["d_meldedatum_str"]
        )
        my_datum[
            "d_ref_datum"
        ] = AllDateReportedFactory.create_new_object_for_rki_ref_datum(
            my_ref_datum=my_datum["d_ref_datum_str"]
        )
        my_datum[
            "d_datenstand"
        ] = AllDateReportedFactory.create_new_object_for_rki_date_datenstand(
            my_date_datenstand=my_datum["d_datenstand_str"]
        )
        return my_datum

    @classmethod
    def row_str_to_int_fields(cls, row):
        my_str_to_int_data_keys = [
            "AnzahlFall",
            "NeuerFall",
            "AnzahlTodesfall",
            "NeuerTodesfall",
            "AnzahlGenesen",
            "NeuGenesen",
            "IstErkrankungsbeginn",
        ]
        my_str_to_int_data = {}
        for my_str_to_int_data_key in my_str_to_int_data_keys:
            my_data_str = row[my_str_to_int_data_key]
            int_data = int(my_data_str)
            my_str_to_int_data[my_str_to_int_data_key] = int_data
        return my_str_to_int_data


class RkiImportFactory:
    @classmethod
    def create_new(cls, row, my_datum):
        o = RkiImport(
            date_reported_import_str=my_datum["d_meldedatum"].date_reported_import_str,
            datum=my_datum["d_meldedatum"].datum,
            fid=row["FID"],
            id_bundesland=row["IdBundesland"],
            bundesland=row["Bundesland"],
            landkreis=row["Landkreis"],
            altersgruppe=row["Altersgruppe"],
            geschlecht=row["Geschlecht"],
            anzahl_fall=row["AnzahlFall"],
            anzahl_todesfall=row["AnzahlTodesfall"],
            meldedatum=row["Meldedatum"],
            id_landkreis=row["IdLandkreis"],
            datenstand=row["Datenstand"],
            neuer_fall=row["NeuerFall"],
            neuer_todesfall=row["NeuerTodesfall"],
            ref_datum=row["Refdatum"],
            neu_genesen=row["NeuGenesen"],
            anzahl_genesen=row["AnzahlGenesen"],
            ist_erkrankungsbeginn=row["IstErkrankungsbeginn"],
            altersgruppe2=row["Altersgruppe2"],
            processed_update=False,
            processed_full_update=False,
        )
        return o
