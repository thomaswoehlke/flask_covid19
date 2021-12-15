from datetime import datetime
from datetime import timezone

from project.app_bootstrap.database import db
from project.app_bootstrap.database import items_per_page
from project.data_all.all_model_mixins import AllEntityMixinBase


class Task(db.Model, AllEntityMixinBase):
    __tablename__ = "task"
    __mapper_args__ = {"concrete": True}
    __table_args__ = (
        db.UniqueConstraint(
            "datum_started",
            "datum_finished",
            "sector",
            "task_name",
            "new_notification",
            name="uix_task",
        ),
    )

    def __repr__(self):
        this_id = self.id
        if this_id is None:
            this_id = ""
        df = self.datum_finished.isoformat()
        if df is None:
            df = ""
        return "{}({} {} {})".format(
            self.__class__.__name__,
            this_id,
            self.datum_started.isoformat(),
            df,
        )

    def __str__(self):
        this_id = self.id
        if this_id is None:
            this_id = ""
        df = self.datum_finished.isoformat()
        if df is None:
            df = ""
        return "{} {} {}".format(
            this_id,
            self.datum_started.isoformat(),
            df,
        )

    id = db.Column(db.Integer, primary_key=True)
    datum_started = db.Column(db.DateTime, nullable=False, index=True)
    datum_finished = db.Column(db.DateTime, nullable=True, index=True)
    sector = db.Column(db.String(16), nullable=False, index=True)
    task_name = db.Column(db.String(255), nullable=False, index=True)
    new_notification = db.Column(db.Boolean, nullable=False, index=True)

    def read(self):
        self.new_notification = False
        return self

    @classmethod
    def create(cls, sector: str, task_name: str):
        new_notification = True
        # tz = timezone(offset=+1, name="CEST")
        datum_started = datetime.now()
        o = Task(
            datum_started=datum_started,
            sector=sector,
            task_name=task_name,
            new_notification=new_notification,
        )
        db.session.add(o)
        db.session.commit()
        return o

    @classmethod
    def finish(cls, task_id: int):
        datum_finished = datetime.now()
        o = Task.find_by_id(task_id)
        o.datum_finished = datum_finished
        db.session.add(o)
        db.session.commit()
        return o

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
        return None

    @classmethod
    def find_all_as_str(cls):
        return None

    @classmethod
    def get_by_id(cls, other_id):
        return cls.__query_all().filter(cls.id == other_id).one()

    @classmethod
    def find_by_id(cls, other_id):
        return cls.__query_all().filter(cls.id == other_id).one_or_none()

    @classmethod
    def count(cls):
        return cls.__query_all().count()
