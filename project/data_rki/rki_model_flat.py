from sqlalchemy import Sequence

from project.app_bootstrap.database import db
from project.data_all.all_model_flat import AllFlat


class RkiFlat(AllFlat):
    __tablename__ = "rki_import_flat"
    __mapper_args__ = {"concrete": True}

    def __repr__(self):
        return "{}({} {} {} {} {} {} {} {} {})".format(
            self.__class__.__name__,
            self.fid,
            self.geschlecht,
            self.date_reported_import_str,
            self.datum.isoformat(),
            self.datenstand__date_reported_import_str,
            self.bundesland,
            self.landkreis,
            self.ref_datum__date_reported_import_str,
            self.altersgruppe,
        )

    id_seq = Sequence('id_seq')
    id = db.Column(db.Integer,
                   id_seq,
                   server_default=id_seq.next_value(),
                   primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    date_reported_import_str = db.Column(db.String(255), nullable=False)
    datum = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    location_group = db.Column(db.String(255), nullable=False)
    location_code = db.Column(db.String(255), nullable=False)
    #
    fall_anzahl = db.Column(db.Integer, nullable=False)
    fall_neu = db.Column(db.Integer, nullable=False)
    todesfall_anzahl = db.Column(db.Integer, nullable=False)
    todesfall_neu = db.Column(db.Integer, nullable=False)
    genesen_anzahl = db.Column(db.Integer, nullable=False)
    genesen_neu = db.Column(db.Integer, nullable=False)
    ist_erkrankungsbeginn = db.Column(db.Integer, nullable=False)
    #
    bundesland = db.Column(db.String(255), nullable=False)
    landkreis = db.Column(db.String(255), nullable=False)
    landkreis_type = db.Column(db.String(255), nullable=False)
    landkreis_name = db.Column(db.String(255), nullable=False)
    altersgruppe = db.Column(db.String(255), nullable=False)
    altersgruppe2 = db.Column(db.String(255), nullable=False)
    geschlecht = db.Column(db.String(255), nullable=False)
    #
    fid = db.Column(db.String(255), nullable=False)
    id_bundesland = db.Column(db.String(255), nullable=False)
    id_landkreis = db.Column(db.String(255), nullable=False)
    #
    datenstand__date_reported_import_str = db.Column(db.String(255), nullable=False)
    datenstand__datum = db.Column(db.Date, nullable=False)
    #
    meldedatum__date_reported_import_str = db.Column(db.String(255), nullable=False)
    meldedatum__datum = db.Column(db.Date, nullable=False)
    meldedatum__year_day_of_year = db.Column(db.String(255), nullable=False)
    meldedatum__year_month = db.Column(db.String(255), nullable=False)
    meldedatum__year_week = db.Column(db.String(255), nullable=False)
    meldedatum__year = db.Column(db.Integer, nullable=False)
    meldedatum__month = db.Column(db.Integer, nullable=False)
    meldedatum__day_of_month = db.Column(db.Integer, nullable=False)
    meldedatum__day_of_week = db.Column(db.Integer, nullable=False)
    meldedatum__day_of_year = db.Column(db.Integer, nullable=True)
    meldedatum__week_of_year = db.Column(db.Integer, nullable=False)
    #
    ref_datum__date_reported_import_str = db.Column(db.String(255), nullable=False)
    ref_datum__datum = db.Column(db.Date, nullable=False)
    ref_datum__year_day_of_year = db.Column(db.String(255), nullable=False)
    ref_datum__year_month = db.Column(db.String(255), nullable=False)
    ref_datum__year_week = db.Column(db.String(255), nullable=False)
    ref_datum__year = db.Column(db.Integer, nullable=False)
    ref_datum__month = db.Column(db.Integer, nullable=False)
    ref_datum__day_of_month = db.Column(db.Integer, nullable=False)
    ref_datum__day_of_week = db.Column(db.Integer, nullable=False)
    ref_datum__day_of_year = db.Column(db.Integer, nullable=True)
    ref_datum__week_of_year = db.Column(db.Integer, nullable=False)


class RkiFlatFactory:
    @classmethod
    def create_new(cls, row, my_int_data, my_datum: {}):
        oo = RkiFlat(
            fall_anzahl=my_int_data["AnzahlFall"],
            fall_neu=my_int_data["NeuerFall"],
            todesfall_anzahl=my_int_data["AnzahlTodesfall"],
            todesfall_neu=my_int_data["NeuerTodesfall"],
            genesen_anzahl=my_int_data["AnzahlGenesen"],
            genesen_neu=my_int_data["NeuGenesen"],
            ist_erkrankungsbeginn=my_int_data["IstErkrankungsbeginn"],
            #
            bundesland=row["Bundesland"],
            landkreis=row["Landkreis"],
            landkreis_type=row["Landkreis"],
            landkreis_name=row["Landkreis"],
            altersgruppe=row["Altersgruppe"],
            altersgruppe2=row["Altersgruppe2"],
            geschlecht=row["Geschlecht"],
            #
            fid=row["FID"],
            id_bundesland=row["IdBundesland"],
            id_landkreis=row["IdLandkreis"],
            datenstand__date_reported_import_str=my_datum[
                "d_datenstand"
            ].date_reported_import_str,
            datenstand__datum=my_datum["d_datenstand"].datum,
            #
            meldedatum__date_reported_import_str=my_datum[
                "d_meldedatum"
            ].date_reported_import_str,
            meldedatum__datum=my_datum["d_meldedatum"].datum,
            meldedatum__year_day_of_year=my_datum["d_meldedatum"].year_day_of_year,
            meldedatum__year_month=my_datum["d_meldedatum"].year_month,
            meldedatum__year_week=my_datum["d_meldedatum"].year_week,
            meldedatum__year=my_datum["d_meldedatum"].year,
            meldedatum__month=my_datum["d_meldedatum"].month,
            meldedatum__day_of_month=my_datum["d_meldedatum"].day_of_month,
            meldedatum__day_of_week=my_datum["d_meldedatum"].day_of_week,
            meldedatum__day_of_year=my_datum["d_meldedatum"].day_of_year,
            meldedatum__week_of_year=my_datum["d_meldedatum"].week_of_year,
            #
            ref_datum__date_reported_import_str=my_datum[
                "d_ref_datum"
            ].date_reported_import_str,
            ref_datum__datum=my_datum["d_ref_datum"].datum,
            ref_datum__year_day_of_year=my_datum["d_ref_datum"].year_day_of_year,
            ref_datum__year_month=my_datum["d_ref_datum"].year_month,
            ref_datum__year_week=my_datum["d_ref_datum"].year_week,
            ref_datum__year=my_datum["d_ref_datum"].year,
            ref_datum__month=my_datum["d_ref_datum"].month,
            ref_datum__day_of_month=my_datum["d_ref_datum"].day_of_month,
            ref_datum__day_of_week=my_datum["d_ref_datum"].day_of_week,
            ref_datum__day_of_year=my_datum["d_ref_datum"].day_of_year,
            ref_datum__week_of_year=my_datum["d_ref_datum"].week_of_year,
            #
            location_code=row["IdLandkreis"],
            location=row["Landkreis"],
            location_group=row["Bundesland"],
            date_reported_import_str=my_datum["d_meldedatum"].date_reported_import_str,
            datum=my_datum["d_meldedatum"].datum,
            processed_update=False,
            processed_full_update=False,
        )
        return oo
