from project.data_ecdc.model.ecdc_model_location_group import EcdcContinent


class EcdcContinentFactory:
    @classmethod
    def create_new(cls, location_group_str: str):
        o = EcdcContinent(
            location_group=location_group_str,
            processed_update=False,
            processed_full_update=False,
        )
        return o
