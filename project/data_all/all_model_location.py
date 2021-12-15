from project.app_bootstrap.database import db
from project.app_bootstrap.database import items_per_page
from project.data_all.all_model import AllEntity
from project.data_all.all_model_location_group import AllLocationGroup
from project.data_all.all_model_location_mixins import AllLocationMixin
from sqlalchemy import and_


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

    id = db.Column(db.Integer, primary_key=True)
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
    def __query_all(cls):
        return db.session.query(cls).order_by(cls.location)

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
