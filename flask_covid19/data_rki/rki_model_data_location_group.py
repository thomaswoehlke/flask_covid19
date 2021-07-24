
from app_config.database import db, items_per_page
from data_all.all_model_location_group import AllLocationGroup


class RkiBundesland(AllLocationGroup):
    __mapper_args__ = {
        'polymorphic_identity': 'rki_location_group'
    }

    id_bundesland = db.Column(db.String(255))
