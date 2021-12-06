from flask_covid19.app_config.database import db
from flask_covid19.app_config.database import items_per_page
from flask_covid19.data_all.all_model_location import AllLocation
from flask_covid19.data_ecdc.ecdc_model_location_group import EcdcContinent
from sqlalchemy import and_


class EcdcCountry(AllLocation):
    __mapper_args__ = {"polymorphic_identity": "ecdc_location"}

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
        return (
            " "
            + self.location_group.location_group
            + " : "
            + self.geo_id
            + " | "
            + self.location_code
            + " | "
            + self.location
            + " | "
            + self.pop_data_2019
        )

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


class EcdcCountryFactory:
    @classmethod
    def create_new(cls, c: [], my_continent: EcdcContinent):
        o = EcdcCountry(
            location=c[0],
            pop_data_2019=c[1],
            geo_id=c[2],
            location_code=c[3],
            location_group=my_continent,
            processed_update=False,
            processed_full_update=False,
        )
        return o
