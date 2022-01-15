from project.data_ecdc.model import EcdcDateReported, EcdcCountry, EcdcData


class EcdcDataFactory:
    @classmethod
    def create_new(
        cls,
        my_deaths: int,
        my_cases: int,
        my_cumulative_number: float,
        date_reported: EcdcDateReported,
        location: EcdcCountry,
    ):
        o = EcdcData(
            location=location,
            date_reported=date_reported,
            deaths=int(my_deaths),
            cases=int(my_cases),
            cumulative_number_for_14_days_of_covid19_cases_per_100000=0.0
            if "" == my_cumulative_number
            else float(my_cumulative_number),
            processed_update=False,
            processed_full_update=False,
        )
        return o
