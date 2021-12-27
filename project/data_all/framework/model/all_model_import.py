from datetime import date

from sqlalchemy import Sequence

from project.app_bootstrap.database import db
from project.data_all.framework.model.all_model import AllEntity
from project.data_all.framework.model.interfaces.all_model_import_mixins import AllImportMixin


class AllImport(AllEntity, AllImportMixin):
    __tablename__ = "all_import"
    __mapper_args__ = {"concrete": True}

    def __str__(self):
        return (
            " [ "
            + self.datum.isoformat()
            + " ] "
            + "updated: "
            + str(self.processed_update)
            + " | full_updated: "
            + str(self.processed_full_update)
        )

    all_import_id_seq = Sequence('all_import_id_seq')
    id = db.Column(db.Integer,
                   all_import_id_seq,
                   server_default=all_import_id_seq.next_value(),
                   primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    #
    date_reported_import_str = db.Column(db.String(255), nullable=False)
    datum = db.Column(db.Date, nullable=False)

    @classmethod
    def find_by_datum(cls, datum: date):
        return db.session.query(cls).filter(cls.datum == datum).all()

    @classmethod
    def find_by_datum_str(cls, datum: date):
        return db.session.query(cls).filter(cls.datum == datum).all()

    @classmethod
    def find_by_datum_reported(cls, datum: date):
        return db.session.query(cls).filter(cls.datum == datum).all()

    @classmethod
    def get_datum_list(cls):
        return (
            db.session.query(cls.date_reported_import_str)
            .group_by(cls.date_reported_import_str)
            .distinct()
            .order_by(cls.date_reported_import_str.desc())
            .all()
        )
