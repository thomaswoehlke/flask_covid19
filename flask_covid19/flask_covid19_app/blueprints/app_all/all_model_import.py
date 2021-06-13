from datetime import date

from flask_covid19_conf.database import db
from flask_covid19_app.blueprints.app_all.all_model import AllEntity
from flask_covid19_app.blueprints.app_all.all_model_import_mixins import AllImportMixin, AllImportFlatMixin


class AllImport(AllEntity, AllImportMixin):
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
    def find_by_datum_str(cls, datum: date):
        return db.session.query(cls) \
            .filter(cls.datum == datum) \
            .all()

    @classmethod
    def find_by_datum_reported(cls, datum: date):
        return db.session.query(cls) \
            .filter(cls.datum == datum) \
            .all()

    @classmethod
    def get_datum_list(cls):
        return db.session.query(cls.date_reported_import_str) \
            .group_by(cls.date_reported_import_str) \
            .distinct() \
            .order_by(cls.date_reported_import_str.desc()) \
            .all()


class AllFlat(AllImport, AllImportFlatMixin):
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