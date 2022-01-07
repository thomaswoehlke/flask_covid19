from datetime import datetime

from sqlalchemy import and_, Sequence

from project.app_bootstrap.database import db
from project.app_bootstrap.database import items_per_page
from project.data_all.all_model_mixins import AllEntityMixinBase


class Task(db.Model, AllEntityMixinBase):
    __tablename__ = "task"
    __mapper_args__ = {"concrete": True}
    __table_args__ = (
        db.UniqueConstraint(
            "id",
            "datum_started",
            "sector",
            "task_name",
            "notification",
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
        return "{}({} {} {} {} {} {})".format(
            self.__class__.__name__,
            this_id,
            self.datum_started.isoformat(),
            df,
            self.sector,
            self.task_name,
            self.new_notification
        )

    def __str__(self):
        this_id = self.id
        if this_id is None:
            this_id = ""
        df = self.datum_finished.isoformat()
        if df is None:
            df = ""
        return "{} {} {} {} {} {}".format(
            this_id,
            self.datum_started.isoformat(),
            df,
            self.sector,
            self.task_name,
            self.new_notification
        )

    task_id_seq = Sequence('task_id_seq')
    id = db.Column(db.Integer,
                   task_id_seq,
                   server_default=task_id_seq.next_value(),
                   primary_key=True)
    datum_started = db.Column(db.DateTime, nullable=False)
    datum_finished = db.Column(db.DateTime, nullable=True)
    sector = db.Column(db.String(16), nullable=False)
    task_name = db.Column(db.String(255), nullable=False)
    notification = db.Column(db.Boolean, nullable=False)
    result_code = db.Column(db.Integer, nullable=False)
    data1_code = db.Column(db.Integer, nullable=False)
    data1_txt = db.Column(db.String(255), nullable=False)
    data2_code = db.Column(db.Integer, nullable=False)
    data2_txt = db.Column(db.String(255), nullable=False)
    data3_code = db.Column(db.Integer, nullable=False)
    data3_txt = db.Column(db.String(255), nullable=False)

    def read(self):
        self.notification = False
        return self

    @classmethod
    def create(cls, sector: str, task_name: str):
        # tz = timezone(offset=+1, name="CEST")
        datum_started = datetime.now()
        o = Task(
            datum_started=datum_started,
            sector=sector,
            task_name=task_name,
            notification=True,
            result_code=0,
            data1_code=0,
            data2_code=0,
            data3_code=0,
            data1_txt="default",
            data2_txt="default",
            data3_txt="default",
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

    @classmethod
    def notifications_count(cls):
        return db.session.query(cls)\
            .filter(and_(cls.datum_finished.is_not(None), cls.notification))\
            .count()

    @classmethod
    def notifications_find(cls):
        return db.session.query(cls)\
            .filter(and_(cls.datum_finished.is_not(None), cls.notification))\
            .order_by(cls.id)

    @classmethod
    def notifications_get(cls, page: int):
        return db.session.query(cls)\
            .filter(cls.notification)\
            .order_by(cls.id)\
            .paginate(page, per_page=items_per_page)

    @classmethod
    def mark_read(cls, page: int):
        page_data = cls.notifications_get(page)
        for pd in page_data.items:
            pass

