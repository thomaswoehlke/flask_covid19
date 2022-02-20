from sqlalchemy import not_, and_, Sequence

from project.data.database import db, items_per_page
from project.data_all.model.all_model_mixins import AllLocationMixin
# from project.data_all.model.all_model import AllLocation

from project.data_ecdc.model.ecdc_model_location_group import EcdcContinent


class EcdcCountry(db.Model, AllLocationMixin):
    __tablename__ = "ecdc_location"
    __mapper_args__ = {"concrete": True}
    __table_args__ = (
        db.UniqueConstraint("location", name="ecdc_location_uix"),
    )

    id_seq = Sequence('ecdc_location_id_seq')
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
        db.Integer, db.ForeignKey("ecdc_location_group.id"), nullable=False
    )
    location_group = db.relationship(
        "EcdcContinent",
        lazy="joined",
        cascade="all",
        order_by="EcdcContinent.location_group",
    )
    pop_data_2019 = db.Column(db.String(255))
    geo_id = db.Column(db.String(255))

    def __repr__(self):
        return "{}({}, {}, {}; {}, {})".format(
            self.__class__.__name__,
            self.location_group.__repr__(),
            self.location_code,
            self.location,
            self.pop_data_2019,
            self.geo_id,
        )

    def __str__(self):
        return " {} : {} | {} | {} | {}".format(
            self.location_group.location_group,
            self.geo_id,
            self.location_code,
            self.location,
            self.pop_data_2019
        )

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
    def get_by(cls, location: str = "", geo_id: str = "", location_code: str = ""):
        return (
            db.session.query(cls)
            .filter(
                and_(
                    (cls.location == location),
                    (cls.geo_id == geo_id),
                    (cls.location_code == location_code),
                )
            )
            .one()
        )

    @classmethod
    def find_by(cls, location: str = "", geo_id: str = "", location_code: str = ""):
        return (
            db.session.query(cls)
            .filter(
                and_(
                    (cls.location == location),
                    (cls.geo_id == geo_id),
                    (cls.location_code == location_code),
                )
            )
            .one_or_none()
        )

    @classmethod
    def find_germany(cls):
        return db.session.query(cls).filter(cls.location_code == "DEU").one_or_none()

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
    def find_by_location_group(cls, location_group: EcdcContinent):
        return (
            db.session.query(cls)
                .filter(cls.location_group == location_group)
                .order_by(cls.location)
                .all()
        )

    @classmethod
    def get_by_location_group(cls, location_group: EcdcContinent, page: int):
        return (
            db.session.query(cls)
                .filter(cls.location_group == location_group)
                .order_by(cls.location)
                .paginate(page, per_page=items_per_page)
        )

    @classmethod
    def find_by_location_code_and_location_and_location_group(
        cls, location_code: str, location: str, location_group: EcdcContinent
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
        cls, location_code: str, location: str, location_group: EcdcContinent
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
            .filter(
                and_(cls.location_code == location_code, cls.location == location)
            )
            .order_by(cls.location)
            .one_or_none()
        )

    @classmethod
    def get_by_location_code_and_location(cls, location_code: str, location: str):
        return (
            db.session.query(cls)
            .filter(
                and_(cls.location_code == location_code, cls.location == location)
            )
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

    @classmethod
    def remove_all(cls):
        db.session.query(cls).delete()
        db.session.commit()
        return None

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

