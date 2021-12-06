
from flask_covid19.app_config.database import db, items_per_page
from flask_covid19.data_all.all_model_location_group import AllLocationGroup


class RkiBundesland(AllLocationGroup):
    __mapper_args__ = {
        'polymorphic_identity': 'rki_location_group'
    }

    id_bundesland = db.Column(db.String(255))


class RkiBundeslandFactory:

    @classmethod
    def create_new(cls, bundesland_of_import):
        o = RkiBundesland(
            location_group=bundesland_of_import[0],
            id_bundesland=bundesland_of_import[1],
            processed_update=False,
            processed_full_update=False,
        )
        return o
