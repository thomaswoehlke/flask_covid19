from datetime import date

from sqlalchemy import Sequence

from project.app_bootstrap.database import db
from project.app_bootstrap.database import items_per_page
from project.data_all.framework.model.all_model import AllEntity
from project.data_all.framework.model.interfaces.all_model_date_reported_mixins import AllDateReportedMixin


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