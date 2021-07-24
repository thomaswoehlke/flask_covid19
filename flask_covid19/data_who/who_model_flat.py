from app_config.database import db
from data_all.all_model_flat import AllFlat
from data_all.all_model_import_mixins import AllImportFlatMixin


class WhoFlat(AllFlat, AllImportFlatMixin):
    __tablename__ = 'who_import_flat'
    __mapper_args__ = {'concrete': True}

    def __repr__(self):
        return "%s(%s %s %s %s %s)" % (self.__class__.__name__,
                                       self.datum.isoformat(), self.date_reported_import_str,
                                       self.location_code, self.location, self.location_group)

    def __str__(self):
        return self.datum.isoformat() + " " + self.location_code + " " + self.location + " " + str(self.location_group)

    id = db.Column(db.Integer, primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    #
    date_reported_import_str = db.Column(db.String(255), nullable=False, index=True)
    datum = db.Column(db.Date, nullable=False, index=True)
    #
    year = db.Column(db.Integer, nullable=False)
    year_month = db.Column(db.String(255), nullable=False)
    year_week = db.Column(db.String(255), nullable=False)
    year_day_of_year = db.Column(db.String(255), nullable=False)
    #
    month = db.Column(db.Integer, nullable=False)
    day_of_month = db.Column(db.Integer, nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)
    week_of_year = db.Column(db.Integer, nullable=False)
    day_of_year = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(255), nullable=False, index=True)
    location_group = db.Column(db.String(255), nullable=False, index=True)
    location_code = db.Column(db.String(255), nullable=False)
    #
    new_cases = db.Column(db.Integer, nullable=False)
    cumulative_cases = db.Column(db.Integer, nullable=False)
    new_deaths = db.Column(db.Integer, nullable=False)
    cumulative_deaths = db.Column(db.Integer, nullable=False)
    country_code = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    who_region = db.Column(db.String(255), nullable=False)
    date_reported = db.Column(db.String(255), nullable=False)
