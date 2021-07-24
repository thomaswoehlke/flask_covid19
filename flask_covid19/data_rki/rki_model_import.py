from datetime import date
from sqlalchemy.orm import Bundle
from sqlalchemy import and_
from app_config.database import db, items_per_page
from data_all.all_model_import import AllImport


class RkiImport(AllImport):
    __tablename__ = 'rki_import'
    __mapper_args__ = {'concrete': True}

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.fid)

    id = db.Column(db.Integer, primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    date_reported_import_str = db.Column(db.String(255), nullable=False, index=True)
    datum = db.Column(db.Date, nullable=False, index=True)
    fid = db.Column(db.String(255), nullable=False, index=True)
    id_bundesland = db.Column(db.String(255), nullable=False)
    bundesland = db.Column(db.String(255), nullable=False, index=True)
    landkreis = db.Column(db.String(255), nullable=False, index=True)
    altersgruppe = db.Column(db.String(255), nullable=False, index=True)
    geschlecht = db.Column(db.String(255), nullable=False, index=True)
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
    def get_all(cls, page: int):
        return db.session.query(cls).paginate(page, per_page=items_per_page)

    @classmethod
    def get_date_datenstand_of_all_import(cls):
        dates_reported = []
        bu = Bundle('datenstand', cls.datenstand)
        for meldedatum in db.session.query(bu).distinct().order_by(cls.datenstand.desc()):
            item = meldedatum[0][0]
            if item not in dates_reported:
                dates_reported.append(item)
        return dates_reported

    @classmethod
    def get_date_ref_datum_of_all_import(cls):
        dates_reported = []
        bu = Bundle('ref_datum', cls.ref_datum)
        for meldedatum in db.session.query(bu).distinct().order_by(cls.ref_datum.desc()):
            item = meldedatum[0][0]
            if item not in dates_reported:
                dates_reported.append(item)
        return dates_reported

    @classmethod
    def get_datum_of_all_import(cls):
        dates_reported = []
        bu = Bundle('meldedatum', cls.meldedatum)
        for meldedatum in db.session.query(bu).distinct().order_by(cls.meldedatum.desc()):
            item = meldedatum[0][0]
            if item not in dates_reported:
                dates_reported.append(item)
        return dates_reported

    @classmethod
    def get_meldedatum_list(cls):
        return db.session.query(cls.meldedatum)\
            .distinct()\
            .order_by(cls.meldedatum.desc())\
            .group_by(cls.meldedatum)\
            .all()

    @classmethod
    def get_date_reported_import_str_list(cls):
        date_reported_import_str_list = []
        bu = Bundle('date_reported_import_str', cls.date_reported_import_str)
        oi_list = db.session.query(bu).distinct().order_by(cls.date_reported_import_str.desc())
        for date_reported_import_str_row in oi_list:
            item = date_reported_import_str_row[0]
            if item not in date_reported_import_str_list:
                date_reported_import_str_list.append(item)
        return date_reported_import_str_list

    @classmethod
    def get_bundesland_list(cls):
        bundesland_list = []
        bu = Bundle('bundesland', cls.bundesland, cls.id_bundesland)
        for bundesland_row in db.session.query(bu).distinct().order_by(cls.bundesland.asc()):
            item = bundesland_row[0]
            if item not in bundesland_list:
                bundesland_list.append(item)
        return bundesland_list

    @classmethod
    def get_altersgruppe_list(cls):
        altersgruppe_list = []
        bu = Bundle('altersgruppe', cls.altersgruppe)
        for altersgruppe_row in db.session.query(bu).distinct().order_by(cls.altersgruppe.asc()):
            item = altersgruppe_row[0]
            if item not in altersgruppe_list:
                altersgruppe_list.append(item)
        return altersgruppe_list

    @classmethod
    def get_landkreis_for_bundesland(cls, bundesland:str):
        return db.session.query(cls.landkreis, cls.id_landkreis) \
            .filter(cls.bundesland == bundesland) \
            .distinct() \
            .order_by(cls.landkreis.asc()) \
            .all()

    @classmethod
    def find_by_datum(cls, my_datum: date):
        return db.session.query(cls) \
            .filter(cls.datum == my_datum) \
            .order_by(cls.landkreis.asc()) \
            .all()

    @classmethod
    def find_by_meldedatum_and_landkreis(cls, my_datum: date, my_landkreis: str):
        return db.session.query(cls) \
            .filter(
                and_(
                    (cls.datum == my_datum),
                    (cls.landkreis == my_landkreis)
                )
            )\
            .order_by(cls.landkreis.asc()) \
            .all()
