
from app_config.database import db, items_per_page
from data_all.all_model import AllLocation


class RkiLandkreis(AllLocation):
    __mapper_args__ = {
        'polymorphic_identity': 'rki_location'
    }

    id_landkreis = db.Column(db.String(255))
    location_name = db.Column(db.String(255))

    @classmethod
    def get_bochum(cls):
        return db.session.query(cls)\
            .filter(cls.location == 'SK Bochum')\
            .one()
