from app_config.database import db, items_per_page
from data_all.all_model_import import AllImport


class EcdcImport(AllImport):
    __tablename__ = 'ecdc_import'
    __mapper_args__ = {'concrete': True}

    def __repr__(self):
        return "%s(%s %s %s %s)" % (self.__class__.__name__,
                           self.date_reported_import_str,
                           self.datum.isoformat(),
                           self.countries_and_territories,
                           self.continent_exp)

    id = db.Column(db.Integer, primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    date_reported_import_str = db.Column(db.String(255), nullable=False, index=True)
    datum = db.Column(db.Date, nullable=False, index=True)
    #
    date_rep = db.Column(db.String(255), nullable=False)
    day = db.Column(db.String(255), nullable=False)
    month = db.Column(db.String(255), nullable=False)
    year = db.Column(db.String(255), nullable=False)
    #
    cases = db.Column(db.String(255), nullable=False)
    deaths = db.Column(db.String(255), nullable=False)
    pop_data_2019 = db.Column(db.String(255), nullable=False)
    #
    countries_and_territories = db.Column(db.String(255), nullable=False, index=True)
    geo_id = db.Column(db.String(255), nullable=False)
    country_territory_code = db.Column(db.String(255), nullable=False)
    continent_exp = db.Column(db.String(255), nullable=False, index=True)
    #
    cumulative_number_for_14_days_of_covid19_cases_per_100000 = db.Column(db.String(255), nullable=False)

    @classmethod
    def get_all(cls, page: int):
        return db.session.query(cls).order_by(
            cls.year,
            cls.month,
            cls.day,
            cls.countries_and_territories
        ).paginate(page, per_page=items_per_page)

    @classmethod
    def get_date_rep(cls):
        return db.session.query(cls.date_rep) \
            .group_by(cls.date_rep)\
            .distinct() \
            .order_by(cls.date_rep.desc())\
            .all()

    @classmethod
    def get_continent(cls):
        return db.session.query(cls.continent_exp) \
            .group_by(cls.continent_exp)\
            .distinct() \
            .order_by(cls.continent_exp.asc()) \
            .all()

    @classmethod
    def get_countries_of_continent(cls, my_continent):
        my_continent_exp = my_continent.location_group
        my_params = {}
        my_params['my_continent_param'] = my_continent_exp
        return db.session.query(
            cls.countries_and_territories,
            cls.pop_data_2019,
            cls.geo_id,
            cls.country_territory_code,
            cls.continent_exp,
        ).filter(
            cls.continent_exp == my_continent_exp
        ).distinct().group_by(
            cls.countries_and_territories,
            cls.pop_data_2019,
            cls.geo_id,
            cls.country_territory_code,
            cls.continent_exp
        ).order_by(cls.countries_and_territories.asc()).all()

    @classmethod
    def find_by_date_reported(cls, p_edcd_date_reported_str: str = ''):
        return db.session.query(cls)\
            .filter(cls.date_rep == p_edcd_date_reported_str) \
            .all()
