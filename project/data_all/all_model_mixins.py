class AllEntityMixinBase:
    @classmethod
    def get_by_id(cls, other_id: int):
        pass

    @classmethod
    def find_by_id(cls, other_id: int):
        pass

    @classmethod
    def remove_all(cls):
        return None

    @classmethod
    def __query_all(cls):
        pass

    @classmethod
    def find_all(cls):
        pass

    @classmethod
    def get_all(cls, page: int):
        pass

    @classmethod
    def find_all_as_dict(cls):
        pass

    @classmethod
    def find_all_as_str(cls):
        pass

    @classmethod
    def count(cls):
        pass


class AllEntityWorkerProgressMixin:
    def set_processed_update(self):
        pass

    def set_processed_full_update(self):
        pass

    def unset_processed_update(self):
        pass

    def unset_processed_full_update(self):
        pass

    @classmethod
    def find_by_not_processed_update(cls):
        pass

    @classmethod
    def find_by_not_processed_full_update(cls):
        pass

    @classmethod
    def set_all_processed_full_update(cls):
        pass

    @classmethod
    def set_all_processed_update(cls):
        pass


class AllEntityMixin(AllEntityMixinBase, AllEntityWorkerProgressMixin):
    pass
