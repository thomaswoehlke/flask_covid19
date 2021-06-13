from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from app_config.database import db, items_per_page # , cache
from data_all.all_model import AllDateReported, AllLocationGroup
from data_all.all_model import AllLocation, BlueprintFactTable, AllEntity


class RkiMeldedatum(AllDateReported):
    __mapper_args__ = {
        'polymorphic_identity': 'rki_date_reported'
    }


class RkiBundesland(AllLocationGroup):
    __mapper_args__ = {
        'polymorphic_identity': 'rki_location_group'
    }

    id_bundesland = db.Column(db.String(255))


class RkiLandkreis(AllLocation):
    __mapper_args__ = {
        'polymorphic_identity': 'rki_location'
    }

    id_landkreis = db.Column(db.String(255))
    location_name = db.Column(db.String(255))

    @classmethod
    def get_bochum(cls):
        return db.session.query(cls)\
            .filter(cls.location == 'SK Bochum')\
            .one()


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


class RkiData(BlueprintFactTable):
    __tablename__ = 'rki'
    __mapper_args__ = {'concrete': True}
    __table_args__ = (
        db.UniqueConstraint(
            'fid',
            name="uix_rki"),
    )

    def __repr__(self):
        return "%s (%s %s %s %s %s %s %s)" % (self.__class__.__name__,
                                              self.date_reported.__repr__(),
                                              self.location.__repr__(),
                                              self.altersgruppe.__repr__(),
                                              self.geschlecht,
                                              self.datenstand_datum.isoformat(),
                                              self.ref_datum_datum.isoformat(),
                                              self.fid)

    def __str__(self):
        return "%s (%s, %s, %s, %s, %s, %s, %s)" % (self.__class__.__name__,
                                                self.date_reported.__str__(),
                                                self.location.__str__(),
                                                self.altersgruppe.__str__(),
                                                self.geschlecht,
                                                self.datenstand_datum.isoformat(),
                                                self.ref_datum_datum.isoformat(),
                                                self.fid)

    id = db.Column(db.Integer, primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    date_reported_id = db.Column(db.Integer, db.ForeignKey('all_date_reported.id'), nullable=False)
    date_reported = db.relationship(
        'RkiMeldedatum',
        lazy='joined',
        backref='data',
        cascade='save-update',
        order_by='desc(RkiMeldedatum.datum)',
    )
    location_id = db.Column(db.Integer, db.ForeignKey('all_location.id'), nullable=False)
    location = db.relationship(
        'RkiLandkreis',
        lazy='joined',
        cascade='save-update',
        order_by='asc(RkiLandkreis.location)'
    )
    fid = db.Column(db.String(255), nullable=False, unique=True)
    altersgruppe_id = db.Column(
        db.Integer,
        db.ForeignKey('rki_altersgruppe.id'),
        nullable=False)
    altersgruppe = db.relationship(
        'RkiAltersgruppe',
        lazy='joined',
        cascade='save-update',
        order_by='desc(RkiAltersgruppe.altersgruppe)')
    geschlecht = db.Column(db.String(255), nullable=False)
    anzahl_fall = db.Column(db.Integer, nullable=False)
    anzahl_todesfall = db.Column(db.Integer, nullable=False)
    datenstand_date_reported_import_str = db.Column(db.String(255), nullable=False, index=True)
    datenstand_datum = db.Column(db.Date, nullable=False, index=True)
    neuer_fall = db.Column(db.Integer, nullable=False)
    neuer_todesfall = db.Column(db.Integer, nullable=False)
    ref_datum_date_reported_import_str = db.Column(db.String(255), nullable=False, index=True)
    ref_datum_datum = db.Column(db.Date, nullable=False, index=True)
    neu_genesen = db.Column(db.Integer, nullable=False)
    anzahl_genesen = db.Column(db.Integer, nullable=False)
    ist_erkrankungsbeginn = db.Column(db.Integer, nullable=False)
    altersgruppe2 = db.Column(db.String(255), nullable=False)

    @classmethod
    def delete_all(cls):
        db.session.query(cls).delete()
        db.session.commit()
        return None

    @classmethod
    def __query_by_location(cls, location: RkiLandkreis):
        return db.session.query(cls).filter(
            cls.location_id == location.id
        ).populate_existing().options(
            joinedload(cls.location).joinedload(RkiLandkreis.location_group),
            joinedload(cls.date_reported)
        )

    @classmethod
    def __query_by_date_reported(cls, date_reported: RkiMeldedatum):
        return db.session.query(cls).filter(
            cls.date_reported_id == date_reported.id
        ).populate_existing().options(
            joinedload(cls.location).joinedload(RkiLandkreis.location_group),
            joinedload(cls.date_reported)
        )

    @classmethod
    def find_by_date_reported(cls, date_reported: RkiMeldedatum):
        return cls.__query_by_date_reported(date_reported).all()

    @classmethod
    def get_by_location(cls, location: RkiLandkreis, page: int):
        return cls.__query_by_location(location).paginate(page, per_page=items_per_page)

    @classmethod
    def find_by_location(cls, location: RkiLandkreis):
        return cls.__query_by_location(location).all()

    @classmethod
    def find_by_date_reported_and_location(cls, date_reported: RkiMeldedatum, location: RkiLandkreis):
        return db.session.query(cls)\
            .filter(and_((cls.date_reported_id == date_reported.id), (cls.location_id == location.id)))\
            .all()

    @classmethod
    def get_by_date_reported_and_location(cls, date_reported: RkiMeldedatum, location: RkiLandkreis, page: int):
        return db.session.query(cls)\
            .filter(and_((cls.date_reported_id == date_reported.id), (cls.location_id == location.id)))\
            .paginate(page, per_page=items_per_page)

    @classmethod
    def delete_data_for_one_day(cls, date_reported: RkiMeldedatum):
        for data in cls.find_by_date_reported(date_reported):
            db.session.delete(data)
        db.session.delete(date_reported)
        db.session.commit()

    @classmethod
    def get_by_date_reported(cls, date_reported: RkiMeldedatum, page: int):
        return cls.__query_by_date_reported(date_reported).paginate(page, per_page=items_per_page)
