# import json

from sqlalchemy import Sequence, not_

# from project.data_all.model.all_model import AllLocationGroup
from project.data.database import db, items_per_page
from project.data_all.model.all_model_mixins import AllLocationGroupMixin


class WhoCountryRegion(db.Model, AllLocationGroupMixin):
    __tablename__ = "who_location_group"
    __mapper_args__ = {"concrete": True}
    __table_args__ = (
        db.UniqueConstraint("location_group", name="who_location_group_uix"),
    )

    id_seq = Sequence('who_location_group_id_seq')
    id = db.Column(db.Integer,
                   id_seq,
                   server_default=id_seq.next_value(),
                   primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    location_group = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return "{}({})".format(
            self.__class__.__name__,
            self.location_group
        )

    def __str__(self):
        return "{}".format(
            self.location_group
        )

    def __init__(self, location_group: str):
        self.location_group = location_group
        self.processed_update = False,
        self.processed_full_update = False

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


class WhoCountryRegionFactory:

    @classmethod
    def create_new(cls, location_group_str: str):
        o = WhoCountryRegion(
            location_group=location_group_str
        )
        return o
