from project.data.database import db
from project.data.database import items_per_page
from project.data_all.model.all_model import AllFactTable

from project.data_ecdc.model.ecdc_model_date_reported import EcdcDateReported
from project.data_ecdc.model.ecdc_model_location import EcdcCountry
from sqlalchemy import and_, Sequence
from sqlalchemy.orm import joinedload


class EcdcData(AllFactTable):
    __tablename__ = "ecdc"
    __mapper_args__ = {"concrete": True}
    __table_args__ = (
        db.UniqueConstraint(
            "date_reported_id",
            "location_id",
            name="uix_ecdc"
        ),
    )

    def __repr__(self):
        return "{} ({} {})".format(
            self.__class__.__name__,
            self.date_reported.__repr__(),
            self.location.__repr__()
        )

    def __str__(self):
        return "{} {}".format(
            self.date_reported.__repr__(),
            self.location.__repr__()
        )

    id_seq = Sequence('ecdc_id_seq')
    id = db.Column(db.Integer,
                   id_seq,
                   server_default=id_seq.next_value(),
                   primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    date_reported_id = db.Column(
        db.Integer, db.ForeignKey("ecdc_date_reported.id"), nullable=False
    )
    date_reported = db.relationship(
        "EcdcDateReported",
        lazy="joined",
        cascade="save-update",
        order_by="desc(EcdcDateReported.datum)",
    )
    location_id = db.Column(
        db.Integer, db.ForeignKey("ecdc_location.id"), nullable=False
    )
    location = db.relationship(
        "EcdcCountry",
        lazy="joined",
        cascade="save-update",
        order_by="asc(EcdcCountry.location)",
    )
    deaths = db.Column(db.Integer, nullable=False)
    cases = db.Column(db.Integer, nullable=False)
    cumulative_number_for_14_days_of_covid19_cases_per_100000 = db.Column(
        db.Float, nullable=False
    )

    @classmethod
    def __query_by_date_reported(cls, date_reported: EcdcDateReported):
        return (
            db.session.query(cls)
            .filter(cls.date_reported_id == date_reported.id)
            .populate_existing()
            .options(
                joinedload(cls.location).joinedload(EcdcCountry.location_group),
                joinedload(cls.date_reported),
            )
        )

    @classmethod
    def __query_by_location(cls, location: EcdcCountry):
        return (
            db.session.query(cls)
            .filter(cls.location_id == location.id)
            .populate_existing()
            .options(
                joinedload(cls.location).joinedload(EcdcCountry.location_group),
                joinedload(cls.date_reported),
            )
        )

    @classmethod
    def __query_by_date_reported_order_by_notification_rate(
        cls, date_reported: EcdcDateReported
    ):
        return cls.__query_by_date_reported(date_reported).order_by(
            cls.cumulative_number_for_14_days_of_covid19_cases_per_100000.desc()
        )

    @classmethod
    def __query_by_date_reported_order_by_deaths(cls, date_reported: EcdcDateReported):
        return cls.__query_by_date_reported(date_reported).order_by(cls.deaths.desc())

    @classmethod
    def __query_by_date_reported_order_by_cases(cls, date_reported: EcdcDateReported):
        return cls.__query_by_date_reported(date_reported).order_by(cls.cases.desc())

    @classmethod
    def __query_by_date_reported_and_location(
        cls, date_reported: EcdcDateReported, location: EcdcCountry
    ):
        return db.session.query(cls).filter(
            and_(
                (cls.location_id == location.id),
                (cls.date_reported_id == date_reported.id),
            )
        )

    @classmethod
    def find_by_date_reported(cls, date_reported: EcdcDateReported):
        return cls.__query_by_date_reported(date_reported).all()

    @classmethod
    def get_by_date_reported(cls, date_reported: EcdcDateReported, page: int):
        return cls.__query_by_date_reported(date_reported).paginate(
            page, per_page=items_per_page
        )

    @classmethod
    def find_by_date_reported_order_by_deaths(cls, date_reported: EcdcDateReported):
        return cls.__query_by_date_reported_order_by_deaths(date_reported).all()

    @classmethod
    def find_by_date_reported_order_by_notification_rate(
        cls, date_reported: EcdcDateReported
    ):
        return cls.__query_by_date_reported_order_by_notification_rate(
            date_reported
        ).all()

    @classmethod
    def get_by_date_reported_order_by_notification_rate(
        cls, date_reported: EcdcDateReported, page: int
    ):
        return cls.__query_by_date_reported_order_by_notification_rate(
            date_reported
        ).paginate(page, per_page=items_per_page)

    @classmethod
    def get_by_date_reported_order_by_deaths(
        cls, date_reported: EcdcDateReported, page: int
    ):
        return cls.__query_by_date_reported_order_by_deaths(date_reported).paginate(
            page, per_page=items_per_page
        )

    @classmethod
    def find_by_date_reported_order_by_cases(cls, date_reported: EcdcDateReported):
        return cls.__query_by_date_reported_order_by_cases(date_reported).all()

    @classmethod
    def get_by_date_reported_order_by_cases(
        cls, date_reported: EcdcDateReported, page: int
    ):
        return cls.__query_by_date_reported_order_by_cases(date_reported).paginate(
            page, per_page=items_per_page
        )

    @classmethod
    def find_by_location(cls, location: EcdcCountry):
        return cls.__query_by_location(location).all()

    @classmethod
    def get_by_location(cls, location: EcdcCountry, page: int):
        return cls.__query_by_location(location).paginate(page, per_page=items_per_page)

    @classmethod
    def find_by_date_reported_and_location(
        cls, date_reported: EcdcDateReported, location: EcdcCountry
    ):
        return cls.__query_by_date_reported_and_location(
            date_reported, location
        ).one_or_none()

    @classmethod
    def get_by_date_reported_and_location(
        cls, date_reported: EcdcDateReported, location: EcdcCountry, page: int
    ):
        return cls.__query_by_date_reported_and_location(date_reported, location).one()

    @classmethod
    def delete_data_for_one_day(cls, date_reported: EcdcDateReported):
        for data in cls.find_by_date_reported(date_reported):
            db.session.delete(data)
        db.session.delete(date_reported)
        db.session.commit()
