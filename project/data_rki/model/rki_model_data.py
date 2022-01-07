from project.app_bootstrap.database import db
from project.app_bootstrap.database import items_per_page
from project.data_all.all_model import AllFactTable

from project.data_all.all_model_date_reported_factory import (
    BlueprintDateReportedFactory,
)
from project.data_rki.model.rki_model_data_location import RkiLandkreis
from project.data_rki.model.rki_model_date_reported import RkiMeldedatum
from project.data_rki.model.rki_model_import import RkiImport
from sqlalchemy import and_, Sequence
from sqlalchemy.orm import joinedload


class RkiData(AllFactTable):
    __tablename__ = "rki"
    __mapper_args__ = {"concrete": True}
    __table_args__ = (
        db.UniqueConstraint("fid", name="uix_rki"),
    )

    def __repr__(self):
        return "{} ({} {} {} {} {} {} {})".format(
            self.__class__.__name__,
            self.date_reported.__repr__(),
            self.location.__repr__(),
            self.altersgruppe.__repr__(),
            self.geschlecht,
            self.datenstand_datum.isoformat(),
            self.ref_datum_datum.isoformat(),
            self.fid,
        )

    def __str__(self):
        return "{} ({}, {}, {}, {}, {}, {}, {})".format(
            self.__class__.__name__,
            self.date_reported.__str__(),
            self.location.__str__(),
            self.altersgruppe.__str__(),
            self.geschlecht,
            self.datenstand_datum.isoformat(),
            self.ref_datum_datum.isoformat(),
            self.fid,
        )

    id_seq = Sequence('rki_id_seq')
    id = db.Column(db.Integer,
                   id_seq,
                   server_default=id_seq.next_value(),
                   primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    date_reported_id = db.Column(
        db.Integer, db.ForeignKey("all_date_reported.id"), nullable=False
    )
    date_reported = db.relationship(
        "RkiMeldedatum",
        lazy="joined",
        backref="data",
        cascade="save-update",
        order_by="desc(RkiMeldedatum.datum)",
    )
    location_id = db.Column(
        db.Integer, db.ForeignKey("all_location.id"), nullable=False
    )
    location = db.relationship(
        "RkiLandkreis",
        lazy="joined",
        cascade="save-update",
        order_by="asc(RkiLandkreis.location)",
    )
    fid = db.Column(db.String(255), nullable=False)
    altersgruppe_id = db.Column(
        db.Integer, db.ForeignKey("rki_altersgruppe.id"), nullable=False
    )
    altersgruppe = db.relationship(
        "RkiAltersgruppe",
        lazy="joined",
        cascade="save-update",
        order_by="desc(RkiAltersgruppe.altersgruppe)",
    )
    geschlecht = db.Column(db.String(255), nullable=False)
    anzahl_fall = db.Column(db.Integer, nullable=False)
    anzahl_todesfall = db.Column(db.Integer, nullable=False)
    datenstand_date_reported_import_str = db.Column(
        db.String(255), nullable=False, index=True
    )
    datenstand_datum = db.Column(db.Date, nullable=False, index=True)
    neuer_fall = db.Column(db.Integer, nullable=False)
    neuer_todesfall = db.Column(db.Integer, nullable=False)
    ref_datum_date_reported_import_str = db.Column(
        db.String(255), nullable=False, index=True
    )
    ref_datum_datum = db.Column(db.Date, nullable=False, index=True)
    neu_genesen = db.Column(db.Integer, nullable=False)
    anzahl_genesen = db.Column(db.Integer, nullable=False)
    ist_erkrankungsbeginn = db.Column(db.Integer, nullable=False)
    altersgruppe2 = db.Column(db.String(255), nullable=False)

    @classmethod
    def delete_all(cls):
        db.session.query(cls).delete()
        db.session.commit()
        return None

    @classmethod
    def __query_by_location(cls, location: RkiLandkreis):
        return (
            db.session.query(cls)
            .filter(cls.location_id == location.id)
            .populate_existing()
            .options(
                joinedload(cls.location).joinedload(RkiLandkreis.location_group),
                joinedload(cls.date_reported),
            )
        )

    @classmethod
    def __query_by_date_reported(cls, date_reported: RkiMeldedatum):
        return (
            db.session.query(cls)
            .filter(cls.date_reported_id == date_reported.id)
            .populate_existing()
            .options(
                joinedload(cls.location).joinedload(RkiLandkreis.location_group),
                joinedload(cls.date_reported),
            )
        )

    @classmethod
    def find_by_date_reported(cls, date_reported: RkiMeldedatum):
        return cls.__query_by_date_reported(date_reported).all()

    @classmethod
    def get_by_location(cls, location: RkiLandkreis, page: int):
        return cls.__query_by_location(location).paginate(page, per_page=items_per_page)

    @classmethod
    def find_by_location(cls, location: RkiLandkreis):
        return cls.__query_by_location(location).all()

    @classmethod
    def find_by_date_reported_and_location(
        cls, date_reported: RkiMeldedatum, location: RkiLandkreis
    ):
        return (
            db.session.query(cls)
            .filter(
                and_(
                    (cls.date_reported_id == date_reported.id),
                    (cls.location_id == location.id),
                )
            )
            .all()
        )

    @classmethod
    def get_by_date_reported_and_location(
        cls, date_reported: RkiMeldedatum, location: RkiLandkreis, page: int
    ):
        return (
            db.session.query(cls)
            .filter(
                and_(
                    (cls.date_reported_id == date_reported.id),
                    (cls.location_id == location.id),
                )
            )
            .paginate(page, per_page=items_per_page)
        )

    @classmethod
    def delete_data_for_one_day(cls, date_reported: RkiMeldedatum):
        for data in cls.find_by_date_reported(date_reported):
            db.session.delete(data)
        db.session.delete(date_reported)
        db.session.commit()

    @classmethod
    def get_by_date_reported(cls, date_reported: RkiMeldedatum, page: int):
        return cls.__query_by_date_reported(date_reported).paginate(
            page, per_page=items_per_page
        )


class RkiDataFactory:
    @classmethod
    def row_str_to_date_fields(cls, o_import: RkiImport):
        my_datum = {
            "meldedatum_str": o_import.meldedatum,
            "ref_datum_str": o_import.ref_datum,
            "datenstand_str": o_import.datenstand,
        }
        my_datum[
            "meldedatum"
        ] = BlueprintDateReportedFactory.create_new_object_for_rki_meldedatum(
            my_meldedatum=my_datum["meldedatum_str"]
        )
        my_datum[
            "ref_datum"
        ] = BlueprintDateReportedFactory.create_new_object_for_rki_ref_datum(
            my_ref_datum=my_datum["ref_datum_str"]
        ).datum
        my_datum[
            "datenstand"
        ] = BlueprintDateReportedFactory.create_new_object_for_rki_date_datenstand(
            my_date_datenstand=my_datum["datenstand_str"]
        ).datum
        return my_datum

    @classmethod
    def get_rki_data(
        cls,
        dict_altersgruppen,
        my_datum,
        my_meldedatum,
        my_landkreis,
        o_import: RkiImport,
    ):
        rki_data = {
            "date_reported": my_meldedatum,
            "datenstand_date_reported_import_str": o_import.datenstand,
            "datenstand_datum": my_datum["datenstand"],
            "location": my_landkreis,
            "ref_datum_date_reported_import_str": o_import.ref_datum,
            "ref_datum_datum": my_datum["ref_datum"],
            "altersgruppe": dict_altersgruppen[o_import.altersgruppe],
            "fid": o_import.fid,
            "geschlecht": o_import.geschlecht,
            #
            "anzahl_fall": int(o_import.anzahl_fall),
            "anzahl_todesfall": int(o_import.anzahl_todesfall),
            "neuer_fall": int(o_import.neuer_fall),
            "neuer_todesfall": int(o_import.neuer_todesfall),
            "neu_genesen": int(o_import.neu_genesen),
            "anzahl_genesen": int(o_import.anzahl_genesen),
            "ist_erkrankungsbeginn": int(o_import.ist_erkrankungsbeginn),
            "altersgruppe2": o_import.altersgruppe2,
        }
        return rki_data

    @classmethod
    def create_new(cls, rki_data):
        o = RkiData(
            date_reported=rki_data["date_reported"],
            datenstand_date_reported_import_str=rki_data[
                "datenstand_date_reported_import_str"
            ],
            datenstand_datum=rki_data["datenstand_datum"],
            location=rki_data["location"],
            ref_datum_date_reported_import_str=rki_data[
                "ref_datum_date_reported_import_str"
            ],
            ref_datum_datum=rki_data["ref_datum_datum"],
            altersgruppe=rki_data["altersgruppe"],
            fid=rki_data["fid"],
            geschlecht=rki_data["geschlecht"],
            #
            anzahl_fall=rki_data["anzahl_fall"],
            anzahl_todesfall=rki_data["anzahl_todesfall"],
            neuer_fall=rki_data["neuer_fall"],
            neuer_todesfall=rki_data["neuer_todesfall"],
            neu_genesen=rki_data["neu_genesen"],
            anzahl_genesen=rki_data["anzahl_genesen"],
            ist_erkrankungsbeginn=rki_data["ist_erkrankungsbeginn"],
            altersgruppe2=rki_data["altersgruppe2"],
            processed_update=False,
            processed_full_update=True,
        )
        return o
