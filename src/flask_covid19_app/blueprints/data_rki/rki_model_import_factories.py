from flask_covid19 import RkiFlat, RkiImport


class RkiImportFactory:

    @classmethod
    def create_new(cls, row, my_datum):
        o = RkiImport(
            date_reported_import_str=my_datum['d_meldedatum'].date_reported_import_str,
            datum=my_datum['d_meldedatum'].datum,
            fid=row['FID'],
            id_bundesland=row['IdBundesland'],
            bundesland=row['Bundesland'],
            landkreis=row['Landkreis'],
            altersgruppe=row['Altersgruppe'],
            geschlecht=row['Geschlecht'],
            anzahl_fall=row['AnzahlFall'],
            anzahl_todesfall=row['AnzahlTodesfall'],
            meldedatum=row['Meldedatum'],
            id_landkreis=row['IdLandkreis'],
            datenstand=row['Datenstand'],
            neuer_fall=row['NeuerFall'],
            neuer_todesfall=row['NeuerTodesfall'],
            ref_datum=row['Refdatum'],
            neu_genesen=row['NeuGenesen'],
            anzahl_genesen=row['AnzahlGenesen'],
            ist_erkrankungsbeginn=row['IstErkrankungsbeginn'],
            altersgruppe2=row['Altersgruppe2'],
            processed_update=False,
            processed_full_update=False,
        )
        return o


class RkiFlatFactory:

    @classmethod
    def create_new(cls, row, my_int_data, my_datum: {}):
        oo = RkiFlat(
            fall_anzahl=my_int_data['AnzahlFall'],
            fall_neu=my_int_data['NeuerFall'],
            todesfall_anzahl=my_int_data['AnzahlTodesfall'],
            todesfall_neu=my_int_data['NeuerTodesfall'],
            genesen_anzahl=my_int_data['AnzahlGenesen'],
            genesen_neu=my_int_data['NeuGenesen'],
            ist_erkrankungsbeginn=my_int_data['IstErkrankungsbeginn'],
            #
            bundesland=row['Bundesland'],
            landkreis=row['Landkreis'],
            landkreis_type=row['Landkreis'],
            landkreis_name=row['Landkreis'],
            altersgruppe=row['Altersgruppe'],
            altersgruppe2=row['Altersgruppe2'],
            geschlecht=row['Geschlecht'],
            #
            fid=row['FID'],
            id_bundesland=row['IdBundesland'],
            id_landkreis=row['IdLandkreis'],
            datenstand__date_reported_import_str=my_datum['d_datenstand'].date_reported_import_str,
            datenstand__datum=my_datum['d_datenstand'].datum,
            #
            meldedatum__date_reported_import_str=my_datum['d_meldedatum'].date_reported_import_str,
            meldedatum__datum=my_datum['d_meldedatum'].datum,
            meldedatum__year_day_of_year=my_datum['d_meldedatum'].year_day_of_year,
            meldedatum__year_month=my_datum['d_meldedatum'].year_month,
            meldedatum__year_week=my_datum['d_meldedatum'].year_week,
            meldedatum__year=my_datum['d_meldedatum'].year,
            meldedatum__month=my_datum['d_meldedatum'].month,
            meldedatum__day_of_month=my_datum['d_meldedatum'].day_of_month,
            meldedatum__day_of_week=my_datum['d_meldedatum'].day_of_week,
            meldedatum__day_of_year=my_datum['d_meldedatum'].day_of_year,
            meldedatum__week_of_year=my_datum['d_meldedatum'].week_of_year,
            #
            ref_datum__date_reported_import_str=my_datum['d_ref_datum'].date_reported_import_str,
            ref_datum__datum=my_datum['d_ref_datum'].datum,
            ref_datum__year_day_of_year=my_datum['d_ref_datum'].year_day_of_year,
            ref_datum__year_month=my_datum['d_ref_datum'].year_month,
            ref_datum__year_week=my_datum['d_ref_datum'].year_week,
            ref_datum__year=my_datum['d_ref_datum'].year,
            ref_datum__month=my_datum['d_ref_datum'].month,
            ref_datum__day_of_month=my_datum['d_ref_datum'].day_of_month,
            ref_datum__day_of_week=my_datum['d_ref_datum'].day_of_week,
            ref_datum__day_of_year=my_datum['d_ref_datum'].day_of_year,
            ref_datum__week_of_year=my_datum['d_ref_datum'].week_of_year,
            #
            location_code=row['IdLandkreis'],
            location=row['Landkreis'],
            location_group=row['Bundesland'],
            date_reported_import_str=my_datum['d_meldedatum'].date_reported_import_str,
            datum=my_datum['d_meldedatum'].datum,
            processed_update=False,
            processed_full_update=False,
        )
        return oo
