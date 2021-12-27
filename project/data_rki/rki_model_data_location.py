from project.app_bootstrap.database import db
from project.data_all.framework.model.all_model_location import AllLocation
from project.data_rki.rki_model_data_location_group import RkiBundesland


class RkiLandkreis(AllLocation):
    __mapper_args__ = {"polymorphic_identity": "rki_location"}

    id_landkreis = db.Column(db.String(255))
    location_name = db.Column(db.String(255))

    @classmethod
    def get_bochum(cls):
        return db.session.query(cls).filter(cls.location == "SK Bochum").one()


class RkiLandkreisFactory:
    @classmethod
    def get_my_landkreis(cls, landkreis_from_import):
        my_location_tmp = landkreis_from_import[0].split(sep=" ", maxsplit=1)
        my_landkreis = {
            "location": landkreis_from_import[0],
            "location_code": my_location_tmp[0],
            "location_name": my_location_tmp[1],
            "id_landkreis": landkreis_from_import[1],
        }
        return my_landkreis

    @classmethod
    def create_new(cls, my_landkreis, bundesland: RkiBundesland):
        o = RkiLandkreis(
            location=my_landkreis["location"],
            location_code=my_landkreis["location_code"],
            location_name=my_landkreis["location_name"],
            id_landkreis=my_landkreis["id_landkreis"],
            location_group=bundesland,
            processed_update=False,
            processed_full_update=True,
        )
        return o
