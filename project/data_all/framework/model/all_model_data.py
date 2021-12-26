from sqlalchemy import Sequence

from project.app_bootstrap.database import db
from data_all.framework.model.all_model import AllEntity
from data_all.framework.model.interfaces.all_model_data_mixins import AllFactTableMixin
from data_all.framework.model.interfaces.all_model_data_mixins import AllFactTableTimeSeriesMixin
from sqlalchemy.orm import subqueryload


class AllFactTableTimeSeries(AllEntity, AllFactTableTimeSeriesMixin):
    __tablename__ = "all_data_timeline"
    __mapper_args__ = {"concrete": True}
    __table_args__ = (
        db.UniqueConstraint("date_reported_id", name="uix_all_data_timeline"),
    )

    def __str__(self):
        return self.date_reported.__str__()

    id_seq = Sequence('all_data_timeline_id_seq')
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
        "AllDateReported",
        lazy="joined",
        cascade="all",
        enable_typechecks=False,
        order_by="desc(AllDateReported.datum)",
    )

    @classmethod
    def get_datum_list(cls):
        datum_list = []
        for data in db.session.query(cls).options(
            subqueryload("date_reported").load_only("datum")
        ):
            datum = data.date_reported.datum.isoformat()
            if not datum in datum_list:
                datum_list.append(datum)
        datum_list.sort()
        return datum_list

    @classmethod
    def get_date_reported_list(cls):
        date_reported_list = []
        for data in db.session.query(cls).options(
            subqueryload("date_reported").load_only("datum")
        ):
            datum = data.date_reported.datum.isoformat()
            if not datum in date_reported_list:
                date_reported_list.append(datum)
        date_reported_list.sort()
        return date_reported_list

    @classmethod
    def get_joungest_date_reported(cls):
        data = cls.get_date_reported_list()
        if len(data) > 0:
            return data.pop()
        else:
            return None


class AllFactTable(AllFactTableTimeSeries, AllFactTableMixin):
    __tablename__ = "all_data"
    __mapper_args__ = {"concrete": True}
    __table_args__ = (
        db.UniqueConstraint("location_id", "date_reported_id", name="uix_all_data"),
    )

    def __str__(self):
        return self.date_reported.__str__() + " " + self.location.__str__()

    id_seq = Sequence('all_data_id_seq')
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
        "AllDateReported",
        lazy="joined",
        cascade="all",
        enable_typechecks=False,
        order_by="desc(AllDateReported.datum)",
    )
    location_id = db.Column(
        db.Integer, db.ForeignKey("all_location.id"), nullable=False
    )
    location = db.relationship(
        "AllLocation",
        lazy="joined",
        cascade="all",
        enable_typechecks=False,
        order_by="asc(AllLocation.location)",
    )
