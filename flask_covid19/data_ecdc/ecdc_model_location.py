
from sqlalchemy import and_
from app_config.database import db, items_per_page
from data_all.all_model_location import AllLocation


class EcdcCountry(AllLocation):
    __mapper_args__ = {
        'polymorphic_identity': 'ecdc_location'
    }

    pop_data_2019 = db.Column(db.String(255))
    geo_id = db.Column(db.String(255))

    def __repr__(self):
        return "%s(%s, %s, %s; %s, %s)" % (self.__class__.__name__,
                                           self.location_group.__repr__(),
                                           self.location_code,
                                           self.location,
                                           self.pop_data_2019,
                                           self.geo_id)

    def __str__(self):
        return " " + self.location_group.location_group \
             + " : " + self.geo_id \
             + " | " + self.location_code \
             + " | " + self.location \
             + " | " + self.pop_data_2019

    @classmethod
    def get_by(cls, location: str = '', geo_id: str = '', location_code: str = ''):
        return db.session.query(cls).filter(and_(
            (cls.location == location),
            (cls.geo_id == geo_id),
            (cls.location_code == location_code)
        )).one()

    @classmethod
    def find_by(cls, location: str = '', geo_id: str = '', location_code: str = ''):
        return db.session.query(cls).filter(and_(
            (cls.location == location),
            (cls.geo_id == geo_id),
            (cls.location_code == location_code)
        )).one_or_none()

    @classmethod
    def find_germany(cls):
        return db.session.query(cls) \
            .filter(cls.location_code == 'DEU') \
            .one_or_none()
