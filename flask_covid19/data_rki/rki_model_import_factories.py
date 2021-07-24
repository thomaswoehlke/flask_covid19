from data_rki.rki_model_import import RkiImport


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
