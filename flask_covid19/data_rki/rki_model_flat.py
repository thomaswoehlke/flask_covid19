from app_config.database import db
from data_all.all_model_flat import AllFlat


class RkiFlat(AllFlat):
    __tablename__ = 'rki_import_flat'
    __mapper_args__ = {'concrete': True}

    def __repr__(self):
        return "%s(%s %s %s %s %s %s %s %s %s)" % (self.__class__.__name__,
                                                   self.fid,
                                                   self.geschlecht,
                                                   self.date_reported_import_str,
                                                   self.datum.isoformat(),
                                                   self.datenstand__date_reported_import_str,
                                                   self.bundesland,
                                                   self.landkreis,
                                                   self.ref_datum__date_reported_import_str,
                                                   self.altersgruppe)

    id = db.Column(db.Integer, primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    date_reported_import_str = db.Column(db.String(255), nullable=False)
    datum = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    location_group = db.Column(db.String(255), nullable=False)
    location_code = db.Column(db.String(255), nullable=False)
    #
    fall_anzahl = db.Column(db.Integer, nullable=False, index=True)
    fall_neu = db.Column(db.Integer, nullable=False, index=True)
    todesfall_anzahl = db.Column(db.Integer, nullable=False, index=True)
    todesfall_neu = db.Column(db.Integer, nullable=False, index=True)
    genesen_anzahl = db.Column(db.Integer, nullable=False, index=True)
    genesen_neu = db.Column(db.Integer, nullable=False, index=True)
    ist_erkrankungsbeginn = db.Column(db.Integer, nullable=False, index=True)
    #
    bundesland = db.Column(db.String(255), nullable=False, index=True)
    landkreis = db.Column(db.String(255), nullable=False, index=True)
    landkreis_type = db.Column(db.String(255), nullable=False, index=True)
    landkreis_name = db.Column(db.String(255), nullable=False, index=True)
    altersgruppe = db.Column(db.String(255), nullable=False, index=True)
    altersgruppe2 = db.Column(db.String(255), nullable=False)
    geschlecht = db.Column(db.String(255), nullable=False)
    #
    fid = db.Column(db.String(255), nullable=False, index=True)
    id_bundesland = db.Column(db.String(255), nullable=False)
    id_landkreis = db.Column(db.String(255), nullable=False)
    #
    datenstand__date_reported_import_str = db.Column(db.String(255), nullable=False)
    datenstand__datum = db.Column(db.Date, nullable=False)
    #
    meldedatum__date_reported_import_str = db.Column(db.String(255), nullable=False, index=True)
    meldedatum__datum = db.Column(db.Date, nullable=False, index=True)
    meldedatum__year_day_of_year = db.Column(db.String(255), nullable=False, index=True)
    meldedatum__year_month = db.Column(db.String(255), nullable=False)
    meldedatum__year_week = db.Column(db.String(255), nullable=False)
    meldedatum__year = db.Column(db.Integer, nullable=False)
    meldedatum__month = db.Column(db.Integer, nullable=False)
    meldedatum__day_of_month = db.Column(db.Integer, nullable=False)
    meldedatum__day_of_week = db.Column(db.Integer, nullable=False)
    meldedatum__day_of_year = db.Column(db.Integer, nullable=True)
    meldedatum__week_of_year = db.Column(db.Integer, nullable=False)
    #
    ref_datum__date_reported_import_str = db.Column(db.String(255), nullable=False, index=True)
    ref_datum__datum = db.Column(db.Date, nullable=False, index=True)
    ref_datum__year_day_of_year = db.Column(db.String(255), nullable=False, index=True)
    ref_datum__year_month = db.Column(db.String(255), nullable=False)
    ref_datum__year_week = db.Column(db.String(255), nullable=False)
    ref_datum__year = db.Column(db.Integer, nullable=False)
    ref_datum__month = db.Column(db.Integer, nullable=False)
    ref_datum__day_of_month = db.Column(db.Integer, nullable=False)
    ref_datum__day_of_week = db.Column(db.Integer, nullable=False)
    ref_datum__day_of_year = db.Column(db.Integer, nullable=True)
    ref_datum__week_of_year = db.Column(db.Integer, nullable=False)
