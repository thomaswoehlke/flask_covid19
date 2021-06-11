from sqlalchemy import and_
from sqlalchemy.orm import joinedload, subqueryload
from database import db, ITEMS_PER_PAGE
from flask_covid19.blueprints.app_all.all_model import AllDateReported, AllLocationGroup
from flask_covid19.blueprints.app_all.all_model import AllLocation, BlueprintFactTable


class DiviDateReported(AllDateReported):
    __mapper_args__ = {
        'polymorphic_identity': 'divi_date_reported'
    }


class DiviRegion(AllLocationGroup):
    __mapper_args__ = {
        'polymorphic_identity': 'divi_location_group'
    }


class DiviCountry(AllLocation):
    __mapper_args__ = {
        'polymorphic_identity': 'divi_location'
    }

    @classmethod
    def get_by(cls, location_code: str, location: str, location_group: DiviRegion):
        return db.session.query(cls).filter(
            and_(
                cls.location_code == location_code,
                cls.location == location,
                cls.location_group_id == location_group.id
            )
        ).one_or_none()

    @classmethod
    def find_by(cls, location_code: str, location: str, location_group: DiviRegion):
        return db.session.query(cls).filter(
            and_(
                cls.location_code == location_code,
                cls.location == location,
                cls.location_group_id == location_group.id
            )
        ).one_or_none()

    @classmethod
    def find_by_location_group(cls, location_group):
        return db.session.query(cls)\
            .filter(cls.location_group == location_group)\
            .order_by(cls.location) \
            .all()

    @classmethod
    def get_by_location_group(cls, location_group, page: int):
        return db.session.query(cls)\
            .filter(cls.location_group == location_group)\
            .order_by(cls.location) \
            .paginate(page, per_page=ITEMS_PER_PAGE)


class DiviData(BlueprintFactTable):
    __tablename__ = 'divi'
    __mapper_args__ = {'concrete': True}

    id = db.Column(db.Integer, primary_key=True)
    date_reported_id = db.Column(db.Integer, db.ForeignKey('all_date_reported.id'), nullable=False)
    date_reported = db.relationship(
        'DiviDateReported',
        lazy='joined',
        cascade='save-update',
        order_by='desc(DiviDateReported.datum)')
    location_id = db.Column(db.Integer, db.ForeignKey('all_location.id'), nullable=False)
    location = db.relationship(
        'DiviCountry',
        lazy='joined',
        cascade='save-update',
        order_by='asc(DiviCountry.location)')
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    #
    cases_new = db.Column(db.Integer, nullable=False)
    cases_cumulative = db.Column(db.Integer, nullable=False)
    deaths_new = db.Column(db.Integer, nullable=False)
    deaths_cumulative = db.Column(db.Integer, nullable=False)

    @classmethod
    def find_by_date_reported_and_location(cls, date_reported: DiviDateReported, location: DiviCountry):
        return db.session.query(cls).filter(
            and_(
                cls.date_reported_id == date_reported.id,
                cls.location_id == location.id
            )
        ).one_or_none()

    @classmethod
    def find_by_location(cls, location: DiviCountry, page):
        return db.session.query(cls).filter(
            cls.location_id == location.id
        ).populate_existing().options(
            joinedload(cls.country).joinedload(DiviCountry.region),
            joinedload(cls.date_reported)
        ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_date_reported_paged(cls, date_reported: DiviDateReported, page):
        return db.session.query(cls).filter(
                cls.date_reported_id == date_reported.id
            ).populate_existing().options(
                joinedload(cls.country).joinedload(DiviCountry.region),
                joinedload(cls.date_reported)
            ).order_by(
                cls.deaths_new.desc(),
                cls.cases_new.desc(),
                cls.deaths_cumulative.desc(),
                cls.cases_cumulative.desc()
            ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_date_reported(cls, date_reported: DiviDateReported):
        return db.session.query(cls).filter(
            cls.date_reported_id == date_reported.id
        ).populate_existing().options(
            joinedload(cls.country).joinedload(DiviCountry.region),
            joinedload(cls.date_reported)
        ).order_by(
            cls.deaths_new.desc(),
            cls.cases_new.desc(),
            cls.deaths_cumulative.desc(),
            cls.cases_cumulative.desc()
        ).all()

    @classmethod
    def delete_data_for_one_day(cls, date_reported: DiviDateReported):
        for one_divi_date in cls.find_by_date_reported(date_reported):
            db.session.delete(one_divi_date)
            db.session.commit()
        return None

    @classmethod
    def find_by_date_reported_order_by_cases_new(cls, date_reported: DiviDateReported, page):
        return db.session.query(cls).filter(
                cls.date_reported_id == date_reported.id
            ).populate_existing().options(
                joinedload(cls.country).joinedload(DiviCountry.region),
                joinedload(cls.date_reported)
            ).order_by(
                cls.cases_new.desc()
            ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_date_reported_order_by_cases_cumulative(cls, date_reported: DiviDateReported, page):
        return db.session.query(cls).filter(
                cls.date_reported_id == date_reported.id
            ).populate_existing().options(
                joinedload(cls.country).joinedload(DiviCountry.region),
                joinedload(cls.date_reported)
            ).order_by(
                cls.cases_cumulative.desc()
            ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_date_reported_order_by_deaths_new(cls, date_reported: DiviDateReported, page):
        return db.session.query(cls).filter(
                cls.date_reported_id == date_reported.id
            ).populate_existing().options(
                joinedload(cls.country).joinedload(DiviCountry.region),
                joinedload(cls.date_reported)
            ).order_by(
                cls.deaths_new.desc()
            ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_location_by_deaths_cumulative(cls, date_reported: DiviDateReported, page):
        return db.session.query(cls).filter(
                cls.date_reported_id == date_reported.id
            ).populate_existing().options(
                joinedload(cls.location).joinedload(DiviCountry.location_group),
                joinedload(cls.date_reported)
            ).order_by(
                cls.deaths_cumulative.desc()
            ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_location_order_by_cases_new(cls, location: DiviCountry, page):
        return db.session.query(cls).filter(
            cls.location_id == location.id
        ).populate_existing().options(
            joinedload(cls.location).joinedload(DiviCountry.location_group),
            joinedload(cls.date_reported)
        ).order_by(
            cls.cases_new.desc()
        ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_location_order_by_cases_cumulative(cls, location: DiviCountry, page):
        return db.session.query(cls).filter(
            cls.location_id == location.id
        ).populate_existing().options(
            joinedload(cls.location).joinedload(DiviCountry.location_group),
            joinedload(cls.date_reported)
        ).order_by(
            cls.cases_cumulative.desc()
        ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_location_order_by_deaths_new(cls, location: DiviCountry, page):
        return db.session.query(cls).filter(
            cls.location_id == location.id
        ).populate_existing().options(
            joinedload(cls.location).joinedload(DiviCountry.location_group),
            joinedload(cls.date_reported)
        ).order_by(
            cls.deaths_new.desc()
        ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_date_reported_order_by_deaths_cumulative(cls, location: DiviCountry, page):
        return db.session.query(cls).filter(
            cls.location_id == location.id
        ).populate_existing().options(
            joinedload(cls.location).joinedload(DiviCountry.location_group),
            joinedload(cls.date_reported)
        ).order_by(
            cls.deaths_cumulative.desc()
        ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_date_reported(cls):
        datum_of_all_divi_data = []
        for data in db.session.query(cls).options(subqueryload("date_reported").load_only("datum")):
            datum = data.date_reported.datum.isoformat()
            if not datum in datum_of_all_divi_data:
                datum_of_all_divi_data.append(datum)
        datum_of_all_divi_data.sort()
        return datum_of_all_divi_data

    @classmethod
    def get_date_reported_list(cls):
        date_reported_list = []
        for data in db.session.query(cls).options(subqueryload("date_reported").load_only("datum")):
            datum = data.date_reported.datum.isoformat()
            if not datum in date_reported_list:
                date_reported_list.append(datum)
        date_reported_list.sort()
        return date_reported_list

    @classmethod
    def get_joungest_date_reported(cls):
        data = cls.get_date_reported_list()
        if len(data) > 0:
            return data.pop()
        else:
            return None
