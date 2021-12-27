from sqlalchemy import Sequence

from project.app_bootstrap.database import db
from project.data_all.framework.model.interfaces.all_model_flat_mixins import AllImportFlatMixin
from project.data_all.framework.model.all_model_import import AllImport


class AllFlat(AllImport, AllImportFlatMixin):
    __tablename__ = "all_import_flat"
    __mapper_args__ = {"concrete": True}

    def __str__(self):
        return (
            " [ "
            + self.datum.isoformat()
            + " ] "
            + self.location_group
            + " : "
            + self.location_code
            + " | "
            + self.location
            + " | updated: "
            + str(self.processed_update)
            + " | full_updated: "
            + str(self.processed_full_update)
        )

    all_import_flat_id_seq = Sequence('all_import_flat_id_seq')
    id = db.Column(db.Integer,
                   all_import_flat_id_seq,
                   server_default=all_import_flat_id_seq.next_value(),
                   primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    #
    date_reported_import_str = db.Column(db.String(255), nullable=False)
    datum = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(255), nullable=True)
    location_group = db.Column(db.String(255), nullable=False)
    location_code = db.Column(db.String(255), nullable=False)
