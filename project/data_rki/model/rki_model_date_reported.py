# from project.data_all.model.all_model import AllDateReported

from sqlalchemy import not_, Sequence
from project.data.database import db, items_per_page
from project.data_all.model.all_model_mixins import AllDateReportedMixin


class RkiMeldedatum(db.Model, AllDateReportedMixin):

    __tablename__ = "rki_date_reported"
    __mapper_args__ = {"concrete": True}
    __table_args__ = (
        db.UniqueConstraint(
            "date_reported_import_str",
            "datum",
            name="rki_date_reported_uix"
        ),
    )

    id_seq = Sequence('rki_date_reported_id_seq')
    id = db.Column(db.Integer,
                   id_seq,
                   server_default=id_seq.next_value(),
                   primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    date_reported_import_str = db.Column(db.String(255), nullable=False)
    datum = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return "{}({} {})".format(
            self.__class__.__name__,
            self.date_reported_import_str,
            self.datum.isoformat()
        )

    def __str__(self):
        return "{} {}".format(
            self.date_reported_import_str,
            self.datum.isoformat()
        )

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
        all_as_dict = {}
        for o in cls.find_all():
            all_as_dict[o.date_reported_import_str] = o
        return all_as_dict

    @classmethod
    def find_all_as_str(cls):
        all_as_str = []
        for o in cls.find_all():
            all_as_str.append(o.date_reported_import_str)
        return all_as_str

    @classmethod
    def get_joungest_datum(cls):
        return db.session.query(cls).order_by(cls.datum.desc()).first()

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
