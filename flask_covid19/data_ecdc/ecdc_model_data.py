from sqlalchemy import and_
from sqlalchemy.orm import joinedload
from app_config.database import db, items_per_page
from data_all.all_model_data import AllFactTable
from data_ecdc.ecdc_model import EcdcDateReported
from data_ecdc.ecdc_model_location import EcdcCountry


class EcdcData(AllFactTable):
    __tablename__ = 'ecdc'
    __mapper_args__ = {'concrete': True}
    __table_args__ = (
        db.UniqueConstraint('date_reported_id', 'location_id', name="uix_ecdc"),
    )

    def __repr__(self):
        return "%s(%s %s)" % (self.__class__.__name__, self.date_reported.__repr__(), self.location.__repr__())

    id = db.Column(db.Integer, primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    date_reported_id = db.Column(db.Integer, db.ForeignKey('all_date_reported.id'), nullable=False)
    date_reported = db.relationship(
        'EcdcDateReported',
        lazy='joined',
        cascade='save-update',
        order_by='desc(EcdcDateReported.datum)')
    location_id = db.Column(db.Integer, db.ForeignKey('all_location.id'), nullable=False)
    location = db.relationship(
        'EcdcCountry',
        lazy='joined',
        cascade='save-update',
        order_by='asc(EcdcCountry.location)')
    deaths = db.Column(db.Integer, nullable=False)
    cases = db.Column(db.Integer, nullable=False)
    cumulative_number_for_14_days_of_covid19_cases_per_100000 = db.Column(db.Float, nullable=False)

    @classmethod
    def __query_by_date_reported(cls, date_reported: EcdcDateReported):
        return db.session.query(cls).filter(
            cls.date_reported_id == date_reported.id
        ).populate_existing().options(
            joinedload(cls.location).joinedload(EcdcCountry.location_group),
            joinedload(cls.date_reported)
        )

    @classmethod
    def __query_by_location(cls, location: EcdcCountry):
        return db.session.query(cls).filter(
            cls.location_id == location.id
        ).populate_existing().options(
            joinedload(cls.location).joinedload(EcdcCountry.location_group),
            joinedload(cls.date_reported)
        )

    @classmethod
    def __query_by_date_reported_order_by_notification_rate(cls, date_reported: EcdcDateReported):
        return cls.__query_by_date_reported(date_reported) \
            .order_by(cls.cumulative_number_for_14_days_of_covid19_cases_per_100000.desc())

    @classmethod
    def __query_by_date_reported_order_by_deaths(cls, date_reported: EcdcDateReported):
        return cls.__query_by_date_reported(date_reported) \
            .order_by(cls.deaths.desc())

    @classmethod
    def __query_by_date_reported_order_by_cases(cls, date_reported: EcdcDateReported):
        return cls.__query_by_date_reported(date_reported) \
            .order_by(cls.cases.desc())

    @classmethod
    def __query_by_date_reported_and_location(cls, date_reported: EcdcDateReported, location: EcdcCountry):
        return db.session.query(cls) \
            .filter(and_((cls.location_id == location.id), (cls.date_reported_id == date_reported.id)))

    @classmethod
    def find_by_date_reported(cls, date_reported: EcdcDateReported):
        return cls.__query_by_date_reported(date_reported).all()

    @classmethod
    def get_by_date_reported(cls, date_reported: EcdcDateReported, page: int):
        return cls.__query_by_date_reported(date_reported)\
            .paginate(page, per_page=items_per_page)

    @classmethod
    def find_by_date_reported_order_by_deaths(cls, date_reported: EcdcDateReported):
        return cls.__query_by_date_reported_order_by_deaths(date_reported).all()

    @classmethod
    def find_by_date_reported_order_by_notification_rate(cls, date_reported: EcdcDateReported):
        return cls.__query_by_date_reported_order_by_notification_rate(date_reported)\
            .all()

    @classmethod
    def get_by_date_reported_order_by_notification_rate(cls, date_reported: EcdcDateReported, page: int):
        return cls.__query_by_date_reported_order_by_notification_rate(date_reported)\
            .paginate(page, per_page=items_per_page)

    @classmethod
    def get_by_date_reported_order_by_deaths(cls, date_reported: EcdcDateReported, page: int):
        return cls.__query_by_date_reported_order_by_deaths(date_reported)\
            .paginate(page, per_page=items_per_page)

    @classmethod
    def find_by_date_reported_order_by_cases(cls, date_reported: EcdcDateReported):
        return cls.__query_by_date_reported_order_by_cases(date_reported).all()

    @classmethod
    def get_by_date_reported_order_by_cases(cls, date_reported: EcdcDateReported, page: int):
        return cls.__query_by_date_reported_order_by_cases(date_reported)\
            .paginate(page, per_page=items_per_page)

    @classmethod
    def find_by_location(cls, location: EcdcCountry):
        return cls.__query_by_location(location).all()

    @classmethod
    def get_by_location(cls, location: EcdcCountry, page: int):
        return cls.__query_by_location(location).paginate(page, per_page=items_per_page)

    @classmethod
    def find_by_date_reported_and_location(cls, date_reported: EcdcDateReported, location: EcdcCountry):
        return cls.__query_by_date_reported_and_location(date_reported, location).one_or_none()

    @classmethod
    def get_by_date_reported_and_location(cls, date_reported: EcdcDateReported, location: EcdcCountry, page: int):
        return cls.__query_by_date_reported_and_location(date_reported, location).one()

    @classmethod
    def delete_data_for_one_day(cls, date_reported: EcdcDateReported):
        for data in cls.find_by_date_reported(date_reported):
            db.session.delete(data)
        db.session.delete(date_reported)
        db.session.commit()


class EcdcDataFactory:

    @classmethod
    def create_new(cls, my_deaths: int, my_cases: int, my_cumulative_number: float,
                   date_reported: EcdcDateReported, location: EcdcCountry):
        o = EcdcData(
            location=location,
            date_reported=date_reported,
            deaths=int(my_deaths),
            cases=int(my_cases),
            cumulative_number_for_14_days_of_covid19_cases_per_100000=0.0 if '' == my_cumulative_number else float(my_cumulative_number),
            processed_update=False,
            processed_full_update=False,
        )
        return o