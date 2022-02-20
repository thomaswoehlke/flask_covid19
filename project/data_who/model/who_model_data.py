
from sqlalchemy import and_, Sequence
from sqlalchemy.orm import joinedload, subqueryload

from project.data.database import db
from project.data.database import items_per_page
from project.data_all.model.all_model_mixins import AllFactTableMixin
from project.data_who.model.who_model_date_reported import WhoDateReported
from project.data_who.model.who_model_location import WhoCountry


class WhoData(db.Model, AllFactTableMixin):
    __tablename__ = "who"
    __mapper_args__ = {"concrete": True}
    __table_args__ = (
        db.UniqueConstraint(
            "date_reported_id",
            "location_id",
            name="who_uix"
        ),
    )

    id_seq = Sequence('who_id_seq')
    id = db.Column(db.Integer,
                   id_seq,
                   server_default=id_seq.next_value(),
                   primary_key=True)
    date_reported_id = db.Column(
        db.Integer, db.ForeignKey("who_date_reported.id"), nullable=False
    )
    date_reported = db.relationship(
        "WhoDateReported",
        lazy="joined",
        cascade="save-update",
        enable_typechecks=True,
        order_by="desc(WhoDateReported.datum)",
    )
    location_id = db.Column(
        db.Integer, db.ForeignKey("who_location.id"), nullable=False
    )
    location = db.relationship(
        "WhoCountry",
        lazy="joined",
        cascade="save-update",
        enable_typechecks=True,
        order_by="asc(WhoCountry.location)",
    )
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    cases_new = db.Column(db.Integer, nullable=False)
    cases_cumulative = db.Column(db.Integer, nullable=False)
    deaths_new = db.Column(db.Integer, nullable=False)
    deaths_cumulative = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "{}({} {} {} {} {} {})".format(
            self.__class__.__name__,
            self.cases_new,
            self.cases_cumulative,
            self.deaths_new,
            self.deaths_cumulative,
            self.date_reported.__repr__(),
            self.location.__repr__(),
        )

    def __str__(self):
        return "{} {} {} {} {} {}".format(
            self.cases_new,
            self.cases_cumulative,
            self.deaths_new,
            self.deaths_cumulative,
            self.date_reported.__str__(),
            self.location.__str__(),
        )

    def __init__(self, cases_new, cases_cumulative, deaths_new, deaths_cumulative,
                 my_date: WhoDateReported, my_country: WhoCountry):
        self.cases_new = cases_new
        self.cases_cumulative = cases_cumulative
        self.deaths_new = deaths_new
        self.deaths_cumulative = deaths_cumulative
        self.date_reported = my_date
        self.location = my_country
        self.processed_update = False
        self.processed_full_update = False

    @classmethod
    def delete_by_datum(cls, datum: WhoDateReported):
        for one_who_date in cls.find_by_datum(datum):
            db.session.delete(one_who_date)
            db.session.commit()
        return None

    @classmethod
    def __query_by_date_reported(cls, date_reported: WhoDateReported):
        return (
            db.session.query(cls)
            .filter(cls.date_reported_id == date_reported.id)
            .populate_existing()
            .options(
                joinedload(cls.location).joinedload(WhoCountry.location_group),
                joinedload(cls.date_reported),
            )
            .order_by(
                cls.deaths_new.desc(),
                cls.cases_new.desc(),
                cls.deaths_cumulative.desc(),
                cls.cases_cumulative.desc(),
            )
        )

    @classmethod
    def __query_by_location(cls, location: WhoCountry):
        return (
            db.session.query(cls)
            .filter(cls.location_id == location.id)
            .populate_existing()
            .options(
                joinedload(cls.location).joinedload(WhoCountry.location_group),
                joinedload(cls.date_reported),
            )
        )

    @classmethod
    def __query_by_date_reported_and_location(
        cls, date_reported: WhoDateReported, location: WhoCountry
    ):
        return db.session.query(cls).filter(
            and_(
                cls.date_reported_id == date_reported.id,
                cls.location_id == location.id
            )
        )

    @classmethod
    def find_by_date_reported(cls, date_reported: WhoDateReported):
        return cls.__query_by_date_reported(date_reported).all()

    @classmethod
    def get_by_date_reported(cls, date_reported: WhoDateReported, page: int):
        return cls.__query_by_date_reported(date_reported).paginate(
            page, per_page=items_per_page
        )

    @classmethod
    def get_by_location(cls, location: WhoCountry, page: int):
        return cls.__query_by_location(location).paginate(page, per_page=items_per_page)

    @classmethod
    def find_by_location(cls, location: WhoCountry):
        return cls.__query_by_location(location).all()

    @classmethod
    def find_by_date_reported_and_location(
        cls, date_reported: WhoDateReported, location: WhoCountry
    ):
        return cls.__query_by_date_reported_and_location(
            date_reported, location
        ).one_or_none()

    @classmethod
    def get_by_date_reported_and_location(
        cls, date_reported: WhoDateReported, location: WhoCountry, page: int
    ):
        return cls.__query_by_date_reported_and_location(date_reported, location).one()

    @classmethod
    def get_by_date_reported_order_by_cases_new(
        cls, date_reported: WhoDateReported, page: int
    ):
        return (
            cls.__query_by_date_reported(date_reported)
            .order_by(cls.cases_new.desc())
            .paginate(page, per_page=items_per_page)
        )

    @classmethod
    def get_by_date_reported_order_by_cases_cumulative(
        cls, date_reported: WhoDateReported, page: int
    ):
        return (
            cls.__query_by_date_reported(date_reported)
            .order_by(cls.cases_cumulative.desc())
            .paginate(page, per_page=items_per_page)
        )

    @classmethod
    def get_by_date_reported_order_by_deaths_new(
        cls, date_reported: WhoDateReported, page: int
    ):
        return (
            cls.__query_by_date_reported(date_reported)
            .order_by(cls.deaths_new.desc())
            .paginate(page, per_page=items_per_page)
        )

    @classmethod
    def get_by_date_reported_order_by_deaths_cumulative(
        cls, date_reported: WhoDateReported, page: int
    ):
        return (
            cls.__query_by_date_reported(date_reported)
            .order_by(cls.deaths_cumulative.desc())
            .paginate(page, per_page=items_per_page)
        )

    @classmethod
    def get_by_location_order_by_cases_new(cls, location: WhoCountry, page: int):
        return (
            cls.__query_by_location(location)
            .order_by(cls.cases_new.desc())
            .paginate(page, per_page=items_per_page)
        )

    @classmethod
    def get_by_location_order_by_cases_cumulative(
        cls, location: WhoDateReported, page: int
    ):
        return (
            cls.__query_by_location(location)
            .order_by(cls.cases_cumulative.desc())
            .paginate(page, per_page=items_per_page)
        )

    @classmethod
    def get_by_location_order_by_deaths_new(cls, location: WhoDateReported, page: int):
        return (
            cls.__query_by_location(location)
            .order_by(cls.deaths_new.desc())
            .paginate(page, per_page=items_per_page)
        )

    @classmethod
    def get_by_location_order_by_deaths_cumulative(
        cls, location: WhoDateReported, page: int
    ):
        return (
            cls.__query_by_location(location)
            .order_by(cls.deaths_cumulative.desc())
            .paginate(page, per_page=items_per_page)
        )

    @classmethod
    def get_data_for_one_day(cls, date_reported: WhoDateReported):
        return db.session.query(cls).filter(
            cls.date_reported_id == date_reported.id
        ).all()

    @classmethod
    def delete_data_for_one_day(cls, date_reported: WhoDateReported):
        db.session.query(cls).filter(cls.date_reported_id == date_reported.id).delete()
        db.session.commit()
        db.session.delete(date_reported)
        db.session.commit()

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


class WhoDataFactory:
    @classmethod
    def create_new(
        cls, my_who_import, my_date: WhoDateReported, my_country: WhoCountry
    ):
        o = WhoData(
            cases_new=my_who_import["new_cases"],
            cases_cumulative=my_who_import["cumulative_cases"],
            deaths_new=my_who_import["new_deaths"],
            deaths_cumulative=my_who_import["cumulative_deaths"],
            my_date=my_date,
            my_country=my_country,
        )
        return o
