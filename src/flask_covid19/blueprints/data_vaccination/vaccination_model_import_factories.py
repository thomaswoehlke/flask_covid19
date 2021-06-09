from database import db, ITEMS_PER_PAGE #, cache
from flask_covid19 import VaccinationImport, VaccinationFlat


class VaccinationImportFactory:

    @classmethod
    def __int(cls, input_string: str):
        if input_string == '#REF!':
            return 0
        else:
            return int(input_string)

    @classmethod
    def create_new(cls, date_reported, d, row):
        o = VaccinationImport(
            dosen_kumulativ=cls.__int(row['dosen_kumulativ']),
            dosen_differenz_zum_vortag=cls.__int(row['dosen_differenz_zum_vortag']),
            dosen_biontech_kumulativ=cls.__int(row['dosen_biontech_kumulativ']),
            dosen_moderna_kumulativ=cls.__int(row['dosen_moderna_kumulativ']),
            personen_erst_kumulativ=cls.__int(row['personen_erst_kumulativ']),
            personen_voll_kumulativ=cls.__int(row['personen_voll_kumulativ']),
            impf_quote_erst=float(row['impf_quote_erst']),
            impf_quote_voll=float(row['impf_quote_voll']),
            indikation_alter_dosen=cls.__int(row['indikation_alter_dosen']),
            indikation_beruf_dosen=cls.__int(row['indikation_beruf_dosen']),
            indikation_medizinisch_dosen=cls.__int(row['indikation_medizinisch_dosen']),
            indikation_pflegeheim_dosen=cls.__int(row['indikation_pflegeheim_dosen']),
            indikation_alter_erst=cls.__int(row['indikation_alter_erst']),
            indikation_beruf_erst=cls.__int(row['indikation_beruf_erst']),
            indikation_medizinisch_erst=cls.__int(row['indikation_medizinisch_erst']),
            indikation_pflegeheim_erst=cls.__int(row['indikation_pflegeheim_erst']),
            indikation_alter_voll=cls.__int(row['indikation_alter_voll']),
            indikation_beruf_voll=cls.__int(row['indikation_beruf_voll']),
            indikation_medizinisch_voll=cls.__int(row['indikation_medizinisch_voll']),
            indikation_pflegeheim_voll=cls.__int(row['indikation_pflegeheim_voll']),
            date_reported_import_str=date_reported,
            datum=d.datum,
            processed_update=False,
            processed_full_update=False,
        )
        return o


class VaccinationFlatFactory:

    @classmethod
    def __int(cls, input_string: str):
        if input_string == '#REF!':
            return 0
        else:
            return int(input_string)

    @classmethod
    def create_new(cls, date_reported, d, row):
        oo = VaccinationFlat(
            datum=d.datum,
            year=d.year,
            month=d.month,
            day_of_month=d.day_of_month,
            day_of_week=d.day_of_week,
            week_of_year=d.week_of_year,
            day_of_year=d.day_of_year,
            year_week=d.year_week,
            year_day_of_year=d.year_day_of_year,
            date_reported_import_str=date_reported,
            year_month=d.year_month,
            location_code="",
            location="",
            location_group="",
            processed_update=False,
            processed_full_update=False,
            #
            dosen_kumulativ=cls.__int(row['dosen_kumulativ']),
            dosen_differenz_zum_vortag=cls.__int(row['dosen_differenz_zum_vortag']),
            dosen_biontech_kumulativ=cls.__int(row['dosen_biontech_kumulativ']),
            dosen_moderna_kumulativ=cls.__int(row['dosen_moderna_kumulativ']),
            personen_erst_kumulativ=cls.__int(row['personen_erst_kumulativ']),
            personen_voll_kumulativ=cls.__int(row['personen_voll_kumulativ']),
            impf_quote_erst=float(row['impf_quote_erst']),
            impf_quote_voll=float(row['impf_quote_voll']),
            indikation_alter_dosen=cls.__int(row['indikation_alter_dosen']),
            indikation_beruf_dosen=cls.__int(row['indikation_beruf_dosen']),
            indikation_medizinisch_dosen=cls.__int(row['indikation_medizinisch_dosen']),
            indikation_pflegeheim_dosen=cls.__int(row['indikation_pflegeheim_dosen']),
            indikation_alter_erst=cls.__int(row['indikation_alter_erst']),
            indikation_beruf_erst=cls.__int(row['indikation_beruf_erst']),
            indikation_medizinisch_erst=cls.__int(row['indikation_medizinisch_erst']),
            indikation_pflegeheim_erst=cls.__int(row['indikation_pflegeheim_erst']),
            indikation_alter_voll=cls.__int(row['indikation_alter_voll']),
            indikation_beruf_voll=cls.__int(row['indikation_beruf_voll']),
            indikation_medizinisch_voll=cls.__int(row['indikation_medizinisch_voll']),
            indikation_pflegeheim_voll=cls.__int(row['indikation_pflegeheim_voll']),
        )
        return oo
