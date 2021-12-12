from datetime import date

from project.data_all.all_model_date_reported import AllDateReported
from project.data_ecdc.ecdc_model import EcdcDateReported
from project.data_owid.owid_model_date_reported import OwidDateReported
from project.data_rki.rki_model_date_reported import RkiMeldedatum
from project.data_vaccination.vaccination_model_date_reported import (
    VaccinationDateReported,
)
from project.data_who.who_model_date_reported import WhoDateReported


class BlueprintDateReportedFactory:
    @classmethod
    def __create_new_object_factory(cls, date_reported_import_str: str, my_datum: date):
        (my_iso_year, week_number, weekday) = my_datum.isocalendar()
        day_of_year = cls.__get_day_of_year(my_datum)
        my_year_month = cls.__get_year_month_as_str(my_datum)
        my_year_day_of_year = cls.__get_year_day_of_year_as_str(my_datum, day_of_year)
        my_year_week = cls.__get_year_week_as_str(my_iso_year, week_number)
        return AllDateReported(
            date_reported_import_str=date_reported_import_str,
            datum=my_datum,
            year_day_of_year=my_year_day_of_year,
            year_month=my_year_month,
            year_week=my_year_week,
            year=my_datum.year,
            month=my_datum.month,
            day_of_month=my_datum.day,
            day_of_week=weekday,
            day_of_year=day_of_year,
            week_of_year=week_number,
            processed_update=False,
            processed_full_update=False,
        )

    @classmethod
    def __create_new_object_factory_for_isoformat(cls, my_date_rep: str):
        my_datum = date.fromisoformat(my_date_rep)
        return cls.__create_new_object_factory(
            date_reported_import_str=my_date_rep, my_datum=my_datum
        )

    @classmethod
    def __get_datetime_parts_for_ecdc(cls, my_datetime: str):
        my_date_parts = my_datetime.split("/")
        my_day = int(my_date_parts[0])
        my_month = int(my_date_parts[1])
        my_year = int(my_date_parts[2])
        datum_parts = (my_year, my_month, my_day)
        return datum_parts

    @classmethod
    def __get_datetime_parts(cls, my_datetime: str):
        my_datetime_parts = my_datetime.split(" ")
        my_date_rep = my_datetime_parts[0]
        my_date_parts = my_date_rep.split("/")
        my_year = int(my_date_parts[0])
        my_month = int(my_date_parts[1])
        my_day = int(my_date_parts[2])
        datum_parts = (my_year, my_month, my_day)
        return datum_parts

    @classmethod
    def __get_datetime_german_parts(cls, my_datetime: str):
        my_datetime_parts = my_datetime.split(",")
        my_date_rep = my_datetime_parts[0]
        my_date_parts = my_date_rep.split(".")
        my_day = int(my_date_parts[0])
        my_month = int(my_date_parts[1])
        my_year = int(my_date_parts[2])
        datum_parts = (my_year, my_month, my_day)
        return datum_parts

    @classmethod
    def __get_datum_parts(cls, my_date_rep: str):
        my_date_parts = my_date_rep.split("-")
        my_year = int(my_date_parts[0])
        my_month = int(my_date_parts[1])
        my_day = int(my_date_parts[2])
        datum_parts = (my_year, my_month, my_day)
        return datum_parts

    @classmethod
    def __get_year_week_as_str(cls, my_iso_year: int, week_number: int):
        my_year_week = "" + str(my_iso_year)
        if week_number < 10:
            my_year_week += "-0"
        else:
            my_year_week += "-"
        my_year_week += str(week_number)
        return my_year_week

    @classmethod
    def __get_year_month_as_str(cls, my_datum: date):
        year_month = "" + str(my_datum.year)
        my_month = my_datum.month
        if my_month < 10:
            year_month += "-0"
        else:
            year_month += "-"
        year_month += str(my_month)
        return year_month

    @classmethod
    def __get_day_of_year(cls, my_datum):
        return my_datum.toordinal() - date(my_datum.year, 1, 1).toordinal() + 1

    @classmethod
    def __get_year_day_of_year_as_str(cls, my_datum, day_of_year):
        year = str(my_datum.year)
        if day_of_year < 100:
            if day_of_year < 10:
                return year + "-00" + str(day_of_year)
            else:
                return year + "-0" + str(day_of_year)
        else:
            return year + "-" + str(day_of_year)

    @classmethod
    def __get_ecdc(cls, o: AllDateReported):
        return EcdcDateReported(
            date_reported_import_str=o.date_reported_import_str,
            datum=o.datum,
            year_day_of_year=o.year_day_of_year,
            year_month=o.year_month,
            year_week=o.year_week,
            year=o.year,
            month=o.month,
            day_of_month=o.day_of_month,
            day_of_week=o.day_of_week,
            day_of_year=o.day_of_year,
            week_of_year=o.week_of_year,
            processed_update=False,
            processed_full_update=False,
        )

    @classmethod
    def __get_owid(cls, o: AllDateReported):
        return OwidDateReported(
            date_reported_import_str=o.date_reported_import_str,
            datum=o.datum,
            year_day_of_year=o.year_day_of_year,
            year_month=o.year_month,
            year_week=o.year_week,
            year=o.year,
            month=o.month,
            day_of_month=o.day_of_month,
            day_of_week=o.day_of_week,
            day_of_year=o.day_of_year,
            week_of_year=o.week_of_year,
            processed_update=False,
            processed_full_update=False,
        )

    @classmethod
    def __get_rki(cls, o: AllDateReported):
        return RkiMeldedatum(
            date_reported_import_str=o.date_reported_import_str,
            datum=o.datum,
            year_day_of_year=o.year_day_of_year,
            year_month=o.year_month,
            year_week=o.year_week,
            year=o.year,
            month=o.month,
            day_of_month=o.day_of_month,
            day_of_week=o.day_of_week,
            day_of_year=o.day_of_year,
            week_of_year=o.week_of_year,
            processed_update=False,
            processed_full_update=False,
        )

    @classmethod
    def __get_vaccination(cls, o: AllDateReported):
        return VaccinationDateReported(
            date_reported_import_str=o.date_reported_import_str,
            datum=o.datum,
            year_day_of_year=o.year_day_of_year,
            year_month=o.year_month,
            year_week=o.year_week,
            year=o.year,
            month=o.month,
            day_of_month=o.day_of_month,
            day_of_week=o.day_of_week,
            day_of_year=o.day_of_year,
            week_of_year=o.week_of_year,
            processed_update=False,
            processed_full_update=False,
        )

    @classmethod
    def __get_who(cls, o: AllDateReported):
        return WhoDateReported(
            date_reported_import_str=o.date_reported_import_str,
            datum=o.datum,
            year_day_of_year=o.year_day_of_year,
            year_month=o.year_month,
            year_week=o.year_week,
            year=o.year,
            month=o.month,
            day_of_month=o.day_of_month,
            day_of_week=o.day_of_week,
            day_of_year=o.day_of_year,
            week_of_year=o.week_of_year,
            processed_update=False,
            processed_full_update=False,
        )

    @classmethod
    def create_new_object_for_divi(cls, my_date_reported: str):
        o = cls.__create_new_object_factory_for_isoformat(my_date_reported)
        return cls.__get_divi(o)

    @classmethod
    def create_new_object_for_ecdc(cls, my_date_reported: str):
        (my_year, my_month, my_day) = cls.__get_datetime_parts_for_ecdc(
            my_date_reported
        )
        my_datum = date(my_year, my_month, my_day)
        o = cls.__create_new_object_factory(
            date_reported_import_str=my_date_reported, my_datum=my_datum
        )
        return cls.__get_ecdc(o)

    @classmethod
    def create_new_object_for_owid(cls, my_date_reported: str):
        o = cls.__create_new_object_factory_for_isoformat(my_date_reported)
        return cls.__get_owid(o)

    @classmethod
    def create_new_object_for_rki_meldedatum(cls, my_meldedatum: str):
        (my_year, my_month, my_day) = cls.__get_datetime_parts(my_meldedatum)
        my_datum = date(my_year, my_month, my_day)
        o = cls.__create_new_object_factory(
            date_reported_import_str=my_meldedatum, my_datum=my_datum
        )
        return cls.__get_rki(o)

    @classmethod
    def create_new_object_for_rki_date_datenstand(cls, my_date_datenstand: str):
        (my_year, my_month, my_day) = cls.__get_datetime_german_parts(
            my_datetime=my_date_datenstand
        )
        my_datum = date(my_year, my_month, my_day)
        o = cls.__create_new_object_factory(
            date_reported_import_str=my_date_datenstand, my_datum=my_datum
        )
        return cls.__get_rki(o)

    @classmethod
    def create_new_object_for_rki_ref_datum(cls, my_ref_datum: str):
        (my_year, my_month, my_day) = cls.__get_datetime_parts(my_ref_datum)
        my_datum = date(my_year, my_month, my_day)
        o = cls.__create_new_object_factory(
            date_reported_import_str=my_ref_datum, my_datum=my_datum
        )
        return cls.__get_rki(o)

    @classmethod
    def create_new_object_for_vaccination(cls, my_date_reported: str):
        o = cls.__create_new_object_factory_for_isoformat(my_date_reported)
        return cls.__get_vaccination(o)

    @classmethod
    def create_new_object_for_who(cls, my_date_reported: str):
        o = cls.__create_new_object_factory_for_isoformat(my_date_reported)
        return cls.__get_who(o)
