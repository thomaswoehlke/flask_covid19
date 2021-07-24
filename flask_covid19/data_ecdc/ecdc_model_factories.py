from data_ecdc.ecdc_model import EcdcContinent, EcdcCountry, EcdcDateReported, EcdcData


class EcdcContinentFactory:

    @classmethod
    def create_new(cls, location_group_str: str):
        o = EcdcContinent(
            location_group=location_group_str,
            processed_update=False,
            processed_full_update=False,
        )
        return o


class EcdcCountryFactory:

    @classmethod
    def create_new(cls, c: [], my_continent: EcdcContinent):
        o = EcdcCountry(
            location=c[0],
            pop_data_2019=c[1],
            geo_id=c[2],
            location_code=c[3],
            location_group=my_continent,
            processed_update=False,
            processed_full_update=False,
        )
        return o


class EcdcDataFactory:

    @classmethod
    def create_new(cls, my_deaths: int, my_cases: int, my_cumulative_number: float,
                   date_reported: EcdcDateReported, location: EcdcCountry):
        o = EcdcData(
            location=location,
            date_reported=date_reported,
            deaths=int(my_deaths),
            cases=int(my_cases),
            cumulative_number_for_14_days_of_covid19_cases_per_100000=0.0 if '' == my_cumulative_number else float(my_cumulative_number),
            processed_update=False,
            processed_full_update=False,
        )
        return o
