from project.app_bootstrap.database import db
from project.app_bootstrap.database import items_per_page
from project.data_all.all_model_mixins import AllEntityMixin
from sqlalchemy import not_, Sequence


class AllEntity(db.Model, AllEntityMixin):
    __abstract__ = True

    all_entity_id_seq = Sequence('all_entity_id_seq')
    id = db.Column(db.Integer,
                   all_entity_id_seq,
                   server_default=all_entity_id_seq.next_value(),
                   primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)

    def set_processed_update(self):
        self.processed_update = True
        return self

    def set_processed_full_update(self):
        self.processed_full_update = True
        return self

    def unset_processed_update(self):
        self.processed_update = False
        return self

    def unset_processed_full_update(self):
        self.processed_full_update = False
        return self

    @classmethod
    def remove_all(cls):
        db.session.query(cls).delete()
        db.session.commit()
        return None

    @classmethod
    def __query_all(cls):
        return db.session.query(cls)

    @classmethod
    def get_all(cls, page: int):
        return cls.__query_all().paginate(page, per_page=items_per_page)

    @classmethod
    def find_all(cls):
        return cls.__query_all().all()

    @classmethod
    def find_all_as_dict(cls):
        pass

    @classmethod
    def find_all_as_str(cls):
        pass

    @classmethod
    def get_by_id(cls, other_id):
        return cls.__query_all().filter(cls.id == other_id).one()

    @classmethod
    def find_by_id(cls, other_id):
        return cls.__query_all().filter(cls.id == other_id).one_or_none()

    @classmethod
    def find_by_not_processed_update(cls):
        return cls.__query_all().filter(not_(cls.processed_update)).all()

    @classmethod
    def find_by_not_processed_full_update(cls):
        return cls.__query_all().filter(not_(cls.processed_full_update)).all()

    @classmethod
    def set_all_processed_full_update(cls):
        for o in cls.find_by_not_processed_full_update():
            o.set_processed_full_update()
        db.session.commit()

    @classmethod
    def set_all_processed_update(cls):
        for o in cls.find_by_not_processed_update():
            o.set_processed_update()
        db.session.commit()

    @classmethod
    def count(cls):
        return cls.__query_all().count()
