from sqlalchemy import not_, and_, Sequence

from project.data.database import db, items_per_page

from project.data_all.model.all_model import AllLocationGroup


class EcdcContinent(db.Model, AllLocationGroup):
    __tablename__ = "ecdc_location_group"
    __mapper_args__ = {"concrete": True}
    __table_args__ = (
        db.UniqueConstraint("location_group", name="ecdc_location_group_uix"),
    )

    id_seq = Sequence('ecdc_location_group_id_seq')
    id = db.Column(db.Integer,
                   id_seq,
                   server_default=id_seq.next_value(),
                   primary_key=True)
    type = db.Column(db.String(50))
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    location_group = db.Column(db.String(255), nullable=False)

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

    # @classmethod
    # def __query_all(cls):
    #     return db.session.query(cls)

    @classmethod
    def __query_all(cls):
        return db.session.query(cls).order_by(cls.location_group)

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

    @classmethod
    def get_last(cls):
        return db.session.query(cls).order_by(cls.location_group).all().pop()

    @classmethod
    def get_by_location_group(cls, location_group: str):
        return db.session.query(cls).filter(cls.location_group == location_group).one()

    @classmethod
    def find_by_location_group(cls, location_group: str):
        return (
            db.session.query(cls)
            .filter(cls.location_group == location_group)
            .one_or_none()
        )

    @classmethod
    def get_all(cls, page: int):
        return (
            db.session.query(cls)
            .order_by(cls.location_group)
            .paginate(page, per_page=items_per_page)
        )

    @classmethod
    def find_all(cls):
        return db.session.query(cls).order_by(cls.location_group).all()

    @classmethod
    def find_all_as_dict(cls):
        dates_reported = {}
        for my_location_group in cls.find_all():
            dates_reported[my_location_group.location_group] = my_location_group
        return dates_reported

    @classmethod
    def find_all_as_str(cls):
        all_str = []
        for my_location_group in cls.find_all():
            all_str.append(my_location_group.location_group)
        return all_str




