

class AllServiceMixinDownload:
    def download(self):
        return self


class AllServiceMixinImport:
    def get_file_date(self):
        pass

    def count_file_rows(self):
        pass

    def import_file(self):
        return self


class AllServiceMixinUpdate:
    def update_dimension_tables(self):
        return self

    def update_fact_table(self):
        return self

    def update(self):
        return self

    def delete_last_day(self):
        return self


class AllServiceMixinUpdateFull:
    def full_update_dimension_tables(self):
        return self

    def full_update_fact_table(self):
        return self

    def full_update(self):
        return self


class AllServiceMixin(
    AllServiceMixinUpdateFull,
    AllServiceMixinUpdate,
    AllServiceMixinDownload,
    AllServiceMixinImport,
):
    pass
