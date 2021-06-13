from flask_covid19_app import RkiImport
from flask_covid19_app_web.web_model_factory import BlueprintDateReportedFactory
from data_rki.rki_model import RkiBundesland, RkiLandkreis, RkiData


class RkiServiceImportFactory:

    @classmethod
    def row_str_to_date_fields(cls, row):
        my_datum = {
            'd_meldedatum_str': row['Meldedatum'],
            'd_ref_datum_str': row['Refdatum'],
            'd_datenstand_str': row['Datenstand'],
        }
        my_datum['d_meldedatum'] = BlueprintDateReportedFactory.create_new_object_for_rki_meldedatum(
            my_meldedatum=my_datum['d_meldedatum_str'])
        my_datum['d_ref_datum'] = BlueprintDateReportedFactory.create_new_object_for_rki_ref_datum(
            my_ref_datum=my_datum['d_ref_datum_str'])
        my_datum['d_datenstand'] = BlueprintDateReportedFactory.create_new_object_for_rki_date_datenstand(
            my_date_datenstand=my_datum['d_datenstand_str'])
        return my_datum

    @classmethod
    def row_str_to_int_fields(cls, row):
        my_str_to_int_data_keys = [
            'AnzahlFall',
            'NeuerFall',
            'AnzahlTodesfall',
            'NeuerTodesfall',
            'AnzahlGenesen',
            'NeuGenesen',
            'IstErkrankungsbeginn'
        ]
        my_str_to_int_data = {}
        for my_str_to_int_data_key in my_str_to_int_data_keys:
            my_data_str = row[my_str_to_int_data_key]
            int_data = int(my_data_str)
            my_str_to_int_data[my_str_to_int_data_key] = int_data
        return my_str_to_int_data


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


class RkiLandkreisFactory:

    @classmethod
    def get_my_landkreis(cls, landkreis_from_import):
        my_location_tmp = landkreis_from_import[0].split(sep=" ", maxsplit=1)
        my_landkreis = {
            'location':  landkreis_from_import[0],
            'location_code': my_location_tmp[0],
            'location_name': my_location_tmp[1],
            'id_landkreis': landkreis_from_import[1],
        }
        return my_landkreis

    @classmethod
    def create_new(cls, my_landkreis, bundesland: RkiBundesland):
        o = RkiLandkreis(
            location=my_landkreis['location'],
            location_code=my_landkreis['location_code'],
            location_name=my_landkreis['location_name'],
            id_landkreis=my_landkreis['id_landkreis'],
            location_group=bundesland,
            processed_update=False,
            processed_full_update=True,
        )
        return o


class RkiDataFactory:

    @classmethod
    def row_str_to_date_fields(cls, o_import: RkiImport):
        my_datum = {
            'meldedatum_str': o_import.meldedatum,
            'ref_datum_str': o_import.ref_datum,
            'datenstand_str': o_import.datenstand,
        }
        my_datum['meldedatum'] = BlueprintDateReportedFactory.create_new_object_for_rki_meldedatum(
            my_meldedatum=my_datum['meldedatum_str'])
        my_datum['ref_datum'] = BlueprintDateReportedFactory.create_new_object_for_rki_ref_datum(
            my_ref_datum=my_datum['ref_datum_str']).datum
        my_datum['datenstand'] = BlueprintDateReportedFactory.create_new_object_for_rki_date_datenstand(
            my_date_datenstand=my_datum['datenstand_str']).datum
        return my_datum

    @classmethod
    def get_rki_data(cls, dict_altersgruppen, my_datum, my_meldedatum, my_landkreis, o_import: RkiImport):
        rki_data = {
            'date_reported': my_meldedatum,
            'datenstand_date_reported_import_str': o_import.datenstand,
            'datenstand_datum': my_datum['datenstand'],
            'location': my_landkreis,
            'ref_datum_date_reported_import_str': o_import.ref_datum,
            'ref_datum_datum': my_datum['ref_datum'],
            'altersgruppe': dict_altersgruppen[o_import.altersgruppe],
            'fid': o_import.fid,
            'geschlecht': o_import.geschlecht,
            #
            'anzahl_fall': int(o_import.anzahl_fall),
            'anzahl_todesfall': int(o_import.anzahl_todesfall),
            'neuer_fall': int(o_import.neuer_fall),
            'neuer_todesfall': int(o_import.neuer_todesfall),
            'neu_genesen': int(o_import.neu_genesen),
            'anzahl_genesen': int(o_import.anzahl_genesen),
            'ist_erkrankungsbeginn': int(o_import.ist_erkrankungsbeginn),
            'altersgruppe2': o_import.altersgruppe2,
        }
        return rki_data

    @classmethod
    def create_new(cls, rki_data):
        o = RkiData(
            date_reported=rki_data['date_reported'],
            datenstand_date_reported_import_str=rki_data['datenstand_date_reported_import_str'],
            datenstand_datum=rki_data['datenstand_datum'],
            location=rki_data['location'],
            ref_datum_date_reported_import_str=rki_data['ref_datum_date_reported_import_str'],
            ref_datum_datum=rki_data['ref_datum_datum'],
            altersgruppe=rki_data['altersgruppe'],
            fid=rki_data['fid'],
            geschlecht=rki_data['geschlecht'],
            #
            anzahl_fall=rki_data['anzahl_fall'],
            anzahl_todesfall=rki_data['anzahl_todesfall'],
            neuer_fall=rki_data['neuer_fall'],
            neuer_todesfall=rki_data['neuer_todesfall'],
            neu_genesen=rki_data['neu_genesen'],
            anzahl_genesen=rki_data['anzahl_genesen'],
            ist_erkrankungsbeginn=rki_data['ist_erkrankungsbeginn'],
            altersgruppe2=rki_data['altersgruppe2'],
            processed_update=False,
            processed_full_update=True,
        )
        return o
