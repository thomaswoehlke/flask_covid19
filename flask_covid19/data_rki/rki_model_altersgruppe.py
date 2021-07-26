
from app_config.database import db, items_per_page
from data_all.all_model import AllEntity


class RkiAltersgruppe(AllEntity):
    __tablename__ = 'rki_altersgruppe'
    __mapper_args__ = {'concrete': True}
    __table_args__ = (
        db.UniqueConstraint('altersgruppe', name="uix_rki_altersgruppe"),
    )

    def __repr__(self):
        return "%s ( %s )" % (self.__class__.__name__, self.altersgruppe)

    def __str__(self):
        return " " + self.altersgruppe + " "

    id = db.Column(db.Integer, primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    #
    altersgruppe = db.Column(db.String(255), nullable=False, unique=True)

    @classmethod
    def __query_all(cls):
        return db.session.query(cls).order_by(cls.altersgruppe)

    @classmethod
    def find_all(cls):
        return cls.__query_all().all()

    @classmethod
    def find_all_as_dict(cls):
        altersgruppe_dict = {}
        for my_altersgruppe in cls.find_all():
            altersgruppe_dict[my_altersgruppe.altersgruppe] = my_altersgruppe
        return altersgruppe_dict

    @classmethod
    def find_all_as_str(cls):
        all_str = []
        for my_altersgruppe in cls.find_all():
            all_str.append(my_altersgruppe.altersgruppe)
        return all_str


class RkiAltersgruppeFactory:

    @classmethod
    def create_new(cls, altersgruppe: str):
        o = RkiAltersgruppe(
            altersgruppe=altersgruppe,
            processed_update=False,
            processed_full_update=False
        )
        return o
