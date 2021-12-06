
from flask_covid19.app_config.database import db
from flask_covid19.data_all.all_model_flat_mixins import AllImportFlatMixin
from flask_covid19.data_all.all_model_import import AllImport


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
