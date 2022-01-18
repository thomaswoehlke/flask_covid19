
import json

from sqlalchemy import not_, and_, Sequence
from sqlalchemy.orm import subqueryload
from datetime import date
from flask_serialize import FlaskSerialize

from project.data_all.model.all_model_mixins import AllEntityMixin, AllImportMixin
from project.data_all.model.all_model_mixins import AllDateReportedMixin, AllLocationMixin
from project.data_all.model.all_model_mixins import AllFactTableTimeSeriesMixin
from project.data_all.model.all_model_mixins import AllLocationGroupMixin, AllFactTableMixin
from project.data.database import db, items_per_page

fs_mixin = FlaskSerialize(db)


class AllEntity(db.Model, fs_mixin, AllEntityMixin):
    __abstract__ = True

    all_entity_id_seq = Sequence('all_entity_id_seq')
    id = db.Column(db.Integer,
                   all_entity_id_seq,
                   server_default=all_entity_id_seq.next_value(),
                   primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)

    def set_processed_update(self):
        self.processed_update = True
        return self

    def set_processed_full_update(self):
        self.processed_full_update = True
        return self

    def unset_processed_update(self):
        self.processed_update = False
        return self

    def unset_processed_full_update(self):
        self.processed_full_update = False
        return self

    @classmethod
    def remove_all(cls):
        db.session.query(cls).delete()
        db.session.commit()
        return None

    @classmethod
    def __query_all(cls):
        return db.session.query(cls)

    @classmethod
    def get_all(cls, page: int):
        return cls.__query_all().paginate(page, per_page=items_per_page)

    @classmethod
    def find_all(cls):
        return cls.__query_all().all()

    @classmethod
    def find_all_as_dict(cls):
        pass

    @classmethod
    def find_all_as_str(cls):
        pass

    @classmethod
    def get_by_id(cls, other_id):
        return cls.__query_all().filter(cls.id == other_id).one()

    @classmethod
    def find_by_id(cls, other_id):
        return cls.__query_all().filter(cls.id == other_id).one_or_none()

    @classmethod
    def find_by_not_processed_update(cls):
        return cls.__query_all().filter(not_(cls.processed_update)).all()

    @classmethod
    def find_by_not_processed_full_update(cls):
        return cls.__query_all().filter(not_(cls.processed_full_update)).all()

    @classmethod
    def set_all_processed_full_update(cls):
        for o in cls.find_by_not_processed_full_update():
            o.set_processed_full_update()
        db.session.commit()

    @classmethod
    def set_all_processed_update(cls):
        for o in cls.find_by_not_processed_update():
            o.set_processed_update()
        db.session.commit()

    @classmethod
    def count(cls):
        return cls.__query_all().count()


class AllImport(AllEntity, AllImportMixin):
    __tablename__ = "all_import"
    __mapper_args__ = {"concrete": True}

    def to_json(self):
        return json.dumps(self, default=lambda self: self.__dict__)

    def __str__(self):
        return (
            " [ "
            + self.datum.isoformat()
            + " ] "
            + "updated: "
            + str(self.processed_update)
            + " | full_updated: "
            + str(self.processed_full_update)
        )

    all_import_id_seq = Sequence('all_import_id_seq')
    id = db.Column(db.Integer,
                   all_import_id_seq,
                   server_default=all_import_id_seq.next_value(),
                   primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    #
    date_reported_import_str = db.Column(db.String(255), nullable=False)
    datum = db.Column(db.Date, nullable=False)

    @classmethod
    def find_by_datum(cls, datum: date):
        return db.session.query(cls).filter(cls.datum == datum).all()

    @classmethod
    def find_by_datum_str(cls, datum: date):
        return db.session.query(cls).filter(cls.datum == datum).all()

    @classmethod
    def find_by_datum_reported(cls, datum: date):
        return db.session.query(cls).filter(cls.datum == datum).all()

    @classmethod
    def get_datum_list(cls):
        return (
            db.session.query(cls.date_reported_import_str)
            .group_by(cls.date_reported_import_str)
            .distinct()
            .order_by(cls.date_reported_import_str.desc())
            .all()
        )


class AllDateReported(AllEntity, AllDateReportedMixin):
    __tablename__ = "all_date_reported"
    __table_args__ = (
        db.UniqueConstraint(
            "date_reported_import_str",
            "datum",
            "type",
            name="uix_all_date_reported"
        ),
    )

    id_seq = Sequence('all_date_reported_id_seq')
    id = db.Column(db.Integer,
                   id_seq,
                   server_default=id_seq.next_value(),
                   primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    type = db.Column(db.String(50))
    #
    date_reported_import_str = db.Column(db.String(255), nullable=False)
    datum = db.Column(db.Date, nullable=False)
    #
    year_day_of_year = db.Column(db.String(255), nullable=False)
    #
    year_month = db.Column(db.String(255), nullable=False)
    year_week = db.Column(db.String(255), nullable=False)
    #
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day_of_month = db.Column(db.Integer, nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)
    day_of_year = db.Column(db.Integer, nullable=False)
    week_of_year = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "all_date_reported",
    }

    def __str__(self):
        return self.datum.isoformat()

    def __dict__(self):
        o = dict({
            'id': str(self.id),
            'processed_update': str(self.processed_update),
            'processed_full_update': str(self.processed_full_update),
            'date_reported_import_str': self.date_reported_import_str,
            'datum': str(self.datum.isoformat()),
            'year_day_of_year': str(self.year_day_of_year),
            'year_month': str(self.year_month),
            'year_week': str(self.year_week),
            'year': str(self.year),
            'month': str(self.month),
            'day_of_month': str(self.day_of_month),
            'day_of_year': str(self.day_of_week),
            'week_of_year': str(self.week_of_year),
        })
        return o

    def to_json(self):
        return json.dumps(self, default=lambda self: self.__dict__())

    @classmethod
    def __query_all(cls):
        return db.session.query(cls).order_by(cls.datum.desc())

    @classmethod
    def get_all(cls, page: int):
        return cls.__query_all().paginate(page, per_page=items_per_page)

    @classmethod
    def find_all(cls):
        return cls.__query_all().all()

    def get_name_for_weekday(self):
        return self.get_names_for_weekday()[self.day_of_week]

    @classmethod
    def get_names_for_weekday(cls):
        return {
            1: "Montag",
            2: "Dienstag",
            3: "Mittwoch",
            4: "Donnerstag",
            5: "Freitag",
            6: "Samstag",
            7: "Sonntag",
        }

    def get_name_for_month(self):
        return self.get_names_for_months()[self.month]

    @classmethod
    def get_names_for_months(cls):
        return {
            1: "Januar",
            2: "Februar",
            3: "März",
            4: "April",
            5: "Mai",
            6: "Juni",
            7: "Juli",
            8: "August",
            9: "September",
            10: "Oktober",
            11: "November",
            12: "Dezember",
        }

    @classmethod
    def get_by_datum(cls, datum: date):
        return db.session.query(cls).filter(cls.datum == datum).one()

    @classmethod
    def get_by_date_reported(cls, date_reported_import_str: str):
        return (
            db.session.query(cls)
            .filter(cls.date_reported_import_str == date_reported_import_str)
            .one()
        )

    @classmethod
    def find_by_date_reported(cls, date_reported_import_str: str):
        return (
            db.session.query(cls)
            .filter(cls.date_reported_import_str == date_reported_import_str)
            .one_or_none()
        )

    @classmethod
    def find_by_year_week(cls, year_week: str):
        return db.session.query(cls).filter(cls.year_week == year_week).all()

    @classmethod
    def get_joungest_datum(cls):
        return db.session.query(cls).order_by(cls.datum.desc()).first()

    @classmethod
    def set_all_processed_update(cls):
        for o in cls.find_by_not_processed_update():
            o.set_processed_update()
        db.session.commit()
        return None

    @classmethod
    def find_all(cls):
        return db.session.query(cls).order_by(cls.datum.desc()).all()

    @classmethod
    def find_all_as_dict(cls):
        dates_reported = {}
        for my_date_reported in cls.find_all():
            dates_reported[my_date_reported.date_reported_import_str] = my_date_reported
        return dates_reported

    @classmethod
    def find_all_as_str(cls):
        all_str = []
        for my_date_reported in cls.find_all():
            all_str.append(my_date_reported.date_reported_import_str)
        return all_str

    @classmethod
    def find_by_not_processed_update_limited(cls, limit: int):
        return cls.__query_all()\
            .filter(not_(cls.processed_update))\
            .order_by(cls.datum.desc())\
            .limit(limit)


class AllLocationGroup(AllEntity, AllLocationGroupMixin):
    __tablename__ = "all_location_group"
    __table_args__ = (
        db.UniqueConstraint("location_group", "type", name="uix_all_location_group"),
    )

    def to_json(self):
        return json.dumps(self, default=lambda self: self.__dict__)

    def __str__(self):
        result = " " + self.location_group + " "
        return result

    id_seq = Sequence('all_location_group_id_seq')
    id = db.Column(db.Integer,
                   id_seq,
                   server_default=id_seq.next_value(),
                   primary_key=True)
    type = db.Column(db.String(50))
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    location_group = db.Column(db.String(255), nullable=False)

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "all_location_group",
    }

    @classmethod
    def __query_all(cls):
        return db.session.query(cls).order_by(cls.location_group)

    @classmethod
    def get_last(cls):
        return db.session.query(cls).order_by(cls.location_group).all().pop()

    @classmethod
    def get_by_location_group(cls, location_group: str):
        return db.session.query(cls).filter(cls.location_group == location_group).one()

    @classmethod
    def find_by_location_group(cls, location_group: str):
        return (
            db.session.query(cls)
            .filter(cls.location_group == location_group)
            .one_or_none()
        )

    @classmethod
    def get_all(cls, page: int):
        return (
            db.session.query(cls)
            .order_by(cls.location_group)
            .paginate(page, per_page=items_per_page)
        )

    @classmethod
    def find_all(cls):
        return db.session.query(cls).order_by(cls.location_group).all()

    @classmethod
    def find_all_as_dict(cls):
        dates_reported = {}
        for my_location_group in cls.find_all():
            dates_reported[my_location_group.location_group] = my_location_group
        return dates_reported

    @classmethod
    def find_all_as_str(cls):
        all_str = []
        for my_location_group in cls.find_all():
            all_str.append(my_location_group.location_group)
        return all_str


class AllLocation(AllEntity, AllLocationMixin):
    __tablename__ = "all_location"
    __table_args__ = (db.UniqueConstraint("location", "type", name="uix_all_location"),)

    def to_json(self):
        return json.dumps(self, default=lambda self: self.__dict__)

    def __str__(self):
        return (
            self.location_group.__str__()
            + " : "
            + self.location_code
            + " | "
            + self.location
        )

    id_seq = Sequence('all_location_id_seq')
    id = db.Column(db.Integer,
                   id_seq,
                   server_default=id_seq.next_value(),
                   primary_key=True)
    type = db.Column(db.String(50))
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    location_code = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=False)
    location_group_id = db.Column(
        db.Integer, db.ForeignKey("all_location_group.id"), nullable=False
    )
    location_group = db.relationship(
        "AllLocationGroup",
        lazy="joined",
        cascade="all",
        enable_typechecks=False,
        order_by="AllLocationGroup.location_group",
    )

    __mapper_args__ = {"polymorphic_on": type, "polymorphic_identity": "all_location"}

    @classmethod
    def find_by_location_code(cls, location_code: str):
        return (
            db.session.query(cls)
            .filter(cls.location_code == location_code)
            .one_or_none()
        )

    @classmethod
    def get_by_location_code(cls, location_code: str):
        return db.session.query(cls).filter(cls.location_code == location_code).one()

    @classmethod
    def find_by_location(cls, location: str):
        return db.session.query(cls).filter(cls.location == location).one_or_none()

    @classmethod
    def get_by_location(cls, location: str):
        return db.session.query(cls).filter(cls.location == location).one()

    @classmethod
    def find_by_location_group(cls, location_group: AllLocationGroup):
        return (
            db.session.query(cls)
            .filter(cls.location_group == location_group)
            .order_by(cls.location)
            .all()
        )

    @classmethod
    def get_by_location_group(cls, location_group: AllLocationGroup, page: int):
        return (
            db.session.query(cls)
            .filter(cls.location_group == location_group)
            .order_by(cls.location)
            .paginate(page, per_page=items_per_page)
        )

    @classmethod
    def find_by_location_code_and_location_and_location_group(
        cls, location_code: str, location: str, location_group: AllLocationGroup
    ):
        return (
            db.session.query(cls)
            .filter(
                and_(
                    cls.location_code == location_code,
                    cls.location == location,
                    cls.location_group_id == location_group.id,
                )
            )
            .one_or_none()
        )

    @classmethod
    def get_by_location_code_and_location_and_location_group(
        cls, location_code: str, location: str, location_group: AllLocationGroup
    ):
        return (
            db.session.query(cls)
            .filter(
                and_(
                    cls.location_code == location_code,
                    cls.location == location,
                    cls.location_group_id == location_group.id,
                )
            )
            .one()
        )

    @classmethod
    def find_by_location_code_and_location(cls, location_code: str, location: str):
        return (
            db.session.query(cls)
            .filter(and_(cls.location_code == location_code, cls.location == location))
            .order_by(cls.location)
            .one_or_none()
        )

    @classmethod
    def get_by_location_code_and_location(cls, location_code: str, location: str):
        return (
            db.session.query(cls)
            .filter(and_(cls.location_code == location_code, cls.location == location))
            .one()
        )

    @classmethod
    def __query_all(cls):
        return db.session.query(cls).order_by(cls.location)

    @classmethod
    def find_all(cls):
        return cls.__query_all().all()

    @classmethod
    def find_all_as_str(cls):
        all_str = []
        for my_location in cls.find_all():
            all_str.append(my_location.location)
        return all_str

    @classmethod
    def find_all_as_dict(cls):
        dates_reported = {}
        for my_location in cls.find_all():
            dates_reported[my_location.location] = my_location
        return dates_reported

    @classmethod
    def get_all(cls, page: int):
        return (
            db.session.query(cls)
            .order_by(cls.location)
            .paginate(page, per_page=items_per_page)
        )


class AllFactTableTimeSeries(AllEntity, AllFactTableTimeSeriesMixin):
    __tablename__ = "all_data_timeline"
    __mapper_args__ = {"concrete": True}
    __table_args__ = (
        db.UniqueConstraint("date_reported_id", name="uix_all_data_timeline"),
    )

    def to_json(self):
        return json.dumps(self, default=lambda self: self.__dict__)

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

    def to_json(self):
        return json.dumps(self, default=lambda self: self.__dict__)

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


