
from datetime import date
from flask_covid19.app_config.database import db, app, celery, items_per_page
from flask_covid19.data_all.all_model_location_group_mixins import AllLocationGroupMixin
from flask_covid19.data_all.all_model import AllEntity


class AllLocationGroup(AllEntity, AllLocationGroupMixin):
    __tablename__ = 'all_location_group'
    __table_args__ = (
        db.UniqueConstraint(
            'location_group',
            'type',
            name='uix_all_location_group'),
    )

    def __str__(self):
        result = " " + self.location_group + " "
        return result

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    location_group = db.Column(db.String(255), nullable=False, index=True)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'all_location_group'
    }

    @classmethod
    def __query_all(cls):
        return db.session.query(cls).order_by(cls.location_group)

    @classmethod
    def get_last(cls):
        return db.session.query(cls).order_by(cls.location_group).all().pop()

    @classmethod
    def get_by_location_group(cls, location_group: str):
        return db.session.query(cls)\
            .filter(cls.location_group == location_group)\
            .one()

    @classmethod
    def find_by_location_group(cls, location_group: str):
        return db.session.query(cls) \
            .filter(cls.location_group == location_group) \
            .one_or_none()

    @classmethod
    def get_all(cls, page: int):
        return db.session.query(cls)\
            .order_by(cls.location_group)\
            .paginate(page, per_page=items_per_page)

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
