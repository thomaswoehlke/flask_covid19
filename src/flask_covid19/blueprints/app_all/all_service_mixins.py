class AllServiceMixinUpdate:

    def update_dimension_tables(self):
        return self

    def update_fact_table(self):
        return self

    def update(self):
        return self

    def delete_last_day(self):
        return self

    def delete_last_location_group(self):
        return self


class AllServiceMixinUpdateFull:

    def full_update_dimension_tables(self):
        return self

    def full_update_fact_table(self):
        return self

    def full_update(self):
        return self


class AllServiceMixin(AllServiceMixinUpdateFull, AllServiceMixinUpdate):

    def download(self):
        return self

    def import_file(self):
        return self

