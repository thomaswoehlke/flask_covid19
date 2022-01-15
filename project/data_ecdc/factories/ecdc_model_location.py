from project.data_ecdc.model import EcdcContinent, EcdcCountry


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
