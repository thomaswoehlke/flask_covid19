from datetime import date

from database import db
from flask_covid19.blueprints.app_all.all_model import BlueprintEntity


class AllImport(BlueprintEntity):
    __tablename__ = 'all_import'
    __mapper_args__ = {'concrete': True}

    def __str__(self):
        return " [ " + self.datum.isoformat() + " ] " \
               + "updated: " + str(self.processed_update) \
               + " | full_updated: " + str(self.processed_full_update)

    id = db.Column(db.Integer, primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    #
    date_reported_import_str = db.Column(db.String(255), nullable=False)
    datum = db.Column(db.Date, nullable=False)

    @classmethod
    def find_by_datum(cls, datum: date):
        return db.session.query(cls) \
            .filter(cls.datum == datum) \
            .all()

    @classmethod
    def get_datum_list(cls):
        return db.session.query(cls.date_reported_import_str) \
            .order_by(cls.date_reported_import_str.desc()) \
            .distinct() \
            .all()


class AllFlat(AllImport):
    __tablename__ = 'all_import_flat'
    __mapper_args__ = {'concrete': True}

    def __str__(self):
        return " [ " + self.datum.isoformat() + " ] " \
               + self.location_group + " : " \
               + self.location_code + " | " \
               + self.location\
               + " | updated: " + str(self.processed_update) \
               + " | full_updated: " + str(self.processed_full_update)

    id = db.Column(db.Integer, primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    #
    date_reported_import_str = db.Column(db.String(255), nullable=False)
    datum = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    location_group = db.Column(db.String(255), nullable=False)
    location_code = db.Column(db.String(255), nullable=False)