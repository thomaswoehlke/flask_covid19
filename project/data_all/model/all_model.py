
from sqlalchemy import not_, and_, Sequence
from sqlalchemy.orm import subqueryload
from datetime import date


from project.data_all.model.all_model_mixins import AllEntityMixin, AllImportMixin
from project.data_all.model.all_model_mixins import AllDateReportedMixin, AllLocationMixin
from project.data_all.model.all_model_mixins import AllFactTableTimeSeriesMixin
from project.data_all.model.all_model_mixins import AllLocationGroupMixin, AllFactTableMixin
from project.data.database import db, items_per_page
from project.data_ecdc.model.ecdc_model_date_reported import EcdcDateReported
from project.data_owid.model.owid_model_date_reported import OwidDateReported
from project.data_rki.model.rki_model_date_reported import RkiMeldedatum
from project.data_vaccination.model.vaccination_model_date_reported import VaccinationDateReported
from project.data_who.model.who_model_date_reported import WhoDateReported


class AllEntity(db.Model, AllEntityMixin):
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
            "date_reported_import_str", "datum", "type", name="uix_all_date_reported"
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


class AllDateReportedFactory:

    @classmethod
    def __create_new_object_factory(cls, date_reported_import_str: str, my_datum: date):
        (my_iso_year, week_number, weekday) = my_datum.isocalendar()
        day_of_year = cls.__get_day_of_year(my_datum)
        my_year_month = cls.__get_year_month_as_str(my_datum)
        my_year_day_of_year = cls.__get_year_day_of_year_as_str(my_datum, day_of_year)
        my_year_week = cls.__get_year_week_as_str(my_iso_year, week_number)
        return AllDateReported(
            date_reported_import_str=date_reported_import_str,
            datum=my_datum,
            year_day_of_year=my_year_day_of_year,
            year_month=my_year_month,
            year_week=my_year_week,
            year=my_datum.year,
            month=my_datum.month,
            day_of_month=my_datum.day,
            day_of_week=weekday,
            day_of_year=day_of_year,
            week_of_year=week_number,
            processed_update=False,
            processed_full_update=False,
        )

    @classmethod
    def __create_new_object_factory_for_isoformat(cls, my_date_rep: str):
        my_datum = date.fromisoformat(my_date_rep)
        return cls.__create_new_object_factory(
            date_reported_import_str=my_date_rep, my_datum=my_datum
        )

    @classmethod
    def __get_datetime_parts_for_ecdc(cls, my_datetime: str):
        my_date_parts = my_datetime.split("/")
        my_day = int(my_date_parts[0])
        my_month = int(my_date_parts[1])
        my_year = int(my_date_parts[2])
        datum_parts = (my_year, my_month, my_day)
        return datum_parts

    @classmethod
    def __get_datetime_parts(cls, my_datetime: str):
        my_datetime_parts = my_datetime.split(" ")
        my_date_rep = my_datetime_parts[0]
        my_date_parts = my_date_rep.split("/")
        my_year = int(my_date_parts[0])
        my_month = int(my_date_parts[1])
        my_day = int(my_date_parts[2])
        datum_parts = (my_year, my_month, my_day)
        return datum_parts

    @classmethod
    def __get_datetime_german_parts(cls, my_datetime: str):
        my_datetime_parts = my_datetime.split(",")
        my_date_rep = my_datetime_parts[0]
        my_date_parts = my_date_rep.split(".")
        my_day = int(my_date_parts[0])
        my_month = int(my_date_parts[1])
        my_year = int(my_date_parts[2])
        datum_parts = (my_year, my_month, my_day)
        return datum_parts

    @classmethod
    def __get_datum_parts(cls, my_date_rep: str):
        my_date_parts = my_date_rep.split("-")
        my_year = int(my_date_parts[0])
        my_month = int(my_date_parts[1])
        my_day = int(my_date_parts[2])
        datum_parts = (my_year, my_month, my_day)
        return datum_parts

    @classmethod
    def __get_year_week_as_str(cls, my_iso_year: int, week_number: int):
        my_year_week = "" + str(my_iso_year)
        if week_number < 10:
            my_year_week += "-0"
        else:
            my_year_week += "-"
        my_year_week += str(week_number)
        return my_year_week

    @classmethod
    def __get_year_month_as_str(cls, my_datum: date):
        year_month = "" + str(my_datum.year)
        my_month = my_datum.month
        if my_month < 10:
            year_month += "-0"
        else:
            year_month += "-"
        year_month += str(my_month)
        return year_month

    @classmethod
    def __get_day_of_year(cls, my_datum):
        return my_datum.toordinal() - date(my_datum.year, 1, 1).toordinal() + 1

    @classmethod
    def __get_year_day_of_year_as_str(cls, my_datum, day_of_year):
        year = str(my_datum.year)
        if day_of_year < 100:
            if day_of_year < 10:
                return year + "-00" + str(day_of_year)
            else:
                return year + "-0" + str(day_of_year)
        else:
            return year + "-" + str(day_of_year)

    @classmethod
    def __get_ecdc(cls, o: AllDateReported):
        return EcdcDateReported(
            date_reported_import_str=o.date_reported_import_str,
            datum=o.datum,
            year_day_of_year=o.year_day_of_year,
            year_month=o.year_month,
            year_week=o.year_week,
            year=o.year,
            month=o.month,
            day_of_month=o.day_of_month,
            day_of_week=o.day_of_week,
            day_of_year=o.day_of_year,
            week_of_year=o.week_of_year,
            processed_update=False,
            processed_full_update=False,
        )

    @classmethod
    def __get_owid(cls, o: AllDateReported):
        return OwidDateReported(
            date_reported_import_str=o.date_reported_import_str,
            datum=o.datum,
            year_day_of_year=o.year_day_of_year,
            year_month=o.year_month,
            year_week=o.year_week,
            year=o.year,
            month=o.month,
            day_of_month=o.day_of_month,
            day_of_week=o.day_of_week,
            day_of_year=o.day_of_year,
            week_of_year=o.week_of_year,
            processed_update=False,
            processed_full_update=False,
        )

    @classmethod
    def __get_rki(cls, o: AllDateReported):
        return RkiMeldedatum(
            date_reported_import_str=o.date_reported_import_str,
            datum=o.datum,
            year_day_of_year=o.year_day_of_year,
            year_month=o.year_month,
            year_week=o.year_week,
            year=o.year,
            month=o.month,
            day_of_month=o.day_of_month,
            day_of_week=o.day_of_week,
            day_of_year=o.day_of_year,
            week_of_year=o.week_of_year,
            processed_update=False,
            processed_full_update=False,
        )

    @classmethod
    def __get_vaccination(cls, o: AllDateReported):
        return VaccinationDateReported(
            date_reported_import_str=o.date_reported_import_str,
            datum=o.datum,
            year_day_of_year=o.year_day_of_year,
            year_month=o.year_month,
            year_week=o.year_week,
            year=o.year,
            month=o.month,
            day_of_month=o.day_of_month,
            day_of_week=o.day_of_week,
            day_of_year=o.day_of_year,
            week_of_year=o.week_of_year,
            processed_update=False,
            processed_full_update=False,
        )

    @classmethod
    def __get_who(cls, o: AllDateReported):
        return WhoDateReported(
            date_reported_import_str=o.date_reported_import_str,
            datum=o.datum,
            year_day_of_year=o.year_day_of_year,
            year_month=o.year_month,
            year_week=o.year_week,
            year=o.year,
            month=o.month,
            day_of_month=o.day_of_month,
            day_of_week=o.day_of_week,
            day_of_year=o.day_of_year,
            week_of_year=o.week_of_year,
            processed_update=False,
            processed_full_update=False,
        )

    @classmethod
    def create_new_object_for_divi(cls, my_date_reported: str):
        o = cls.__create_new_object_factory_for_isoformat(my_date_reported)
        return cls.__get_divi(o)

    @classmethod
    def create_new_object_for_ecdc(cls, my_date_reported: str):
        (my_year, my_month, my_day) = cls.__get_datetime_parts_for_ecdc(
            my_date_reported
        )
        my_datum = date(my_year, my_month, my_day)
        o = cls.__create_new_object_factory(
            date_reported_import_str=my_date_reported, my_datum=my_datum
        )
        return cls.__get_ecdc(o)

    @classmethod
    def create_new_object_for_owid(cls, my_date_reported: str):
        o = cls.__create_new_object_factory_for_isoformat(my_date_reported)
        return cls.__get_owid(o)

    @classmethod
    def create_new_object_for_rki_meldedatum(cls, my_meldedatum: str):
        (my_year, my_month, my_day) = cls.__get_datetime_parts(my_meldedatum)
        my_datum = date(my_year, my_month, my_day)
        o = cls.__create_new_object_factory(
            date_reported_import_str=my_meldedatum, my_datum=my_datum
        )
        return cls.__get_rki(o)

    @classmethod
    def create_new_object_for_rki_date_datenstand(cls, my_date_datenstand: str):
        (my_year, my_month, my_day) = cls.__get_datetime_german_parts(
            my_datetime=my_date_datenstand
        )
        my_datum = date(my_year, my_month, my_day)
        o = cls.__create_new_object_factory(
            date_reported_import_str=my_date_datenstand, my_datum=my_datum
        )
        return cls.__get_rki(o)

    @classmethod
    def create_new_object_for_rki_ref_datum(cls, my_ref_datum: str):
        (my_year, my_month, my_day) = cls.__get_datetime_parts(my_ref_datum)
        my_datum = date(my_year, my_month, my_day)
        o = cls.__create_new_object_factory(
            date_reported_import_str=my_ref_datum, my_datum=my_datum
        )
        return cls.__get_rki(o)

    @classmethod
    def create_new_object_for_vaccination(cls, my_date_reported: str):
        o = cls.__create_new_object_factory_for_isoformat(my_date_reported)
        return cls.__get_vaccination(o)

    @classmethod
    def create_new_object_for_who(cls, my_date_reported: str):
        o = cls.__create_new_object_factory_for_isoformat(my_date_reported)
        return cls.__get_who(o)
