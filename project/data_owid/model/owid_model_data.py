from sqlalchemy import Sequence

from project.data.database import db
from project.data.database import items_per_page
from project.data_all.model.all_model import AllFactTable

from project.data_owid.model.owid_model_date_reported import OwidDateReported
from project.data_owid.model.owid_model_import import OwidImport
from project.data_owid.model.owid_model_location import OwidCountry
from sqlalchemy.orm import joinedload


class OwidData(AllFactTable):
    __tablename__ = "owid"
    __mapper_args__ = {"concrete": True}
    __table_args__ = (
        db.UniqueConstraint(
            "date_reported_id",
            "location_id",
            name="uix_owid"
        ),
    )

    def __repr__(self):
        return f"{self.__class__.__name__}({self.date_reported.__repr__()} {self.location.__repr__()})"

    id_seq = Sequence('owid_id_seq')
    id = db.Column(db.Integer,
                   id_seq,
                   server_default=id_seq.next_value(),
                   primary_key=True)
    processed_update = db.Column(db.Boolean, nullable=False)
    processed_full_update = db.Column(db.Boolean, nullable=False)
    #
    date_reported_id = db.Column(
        db.Integer, db.ForeignKey("all_date_reported.id"), nullable=False
    )
    date_reported = db.relationship(
        "OwidDateReported",
        lazy="joined",
        cascade="save-update",
        order_by="desc(OwidDateReported.datum)",
    )
    location_id = db.Column(
        db.Integer, db.ForeignKey("all_location.id"), nullable=False
    )
    location = db.relationship(
        "OwidCountry",
        lazy="joined",
        cascade="save-update",
        order_by="asc(OwidCountry.location)",
    )
    #
    total_cases = db.Column(db.Float, nullable=False)
    new_cases = db.Column(db.Float, nullable=False)
    new_cases_smoothed = db.Column(db.Float, nullable=False)
    total_deaths = db.Column(db.Float, nullable=False)
    new_deaths = db.Column(db.Float, nullable=False)
    new_deaths_smoothed = db.Column(db.Float, nullable=False)
    total_cases_per_million = db.Column(db.Float, nullable=False)
    new_cases_per_million = db.Column(db.Float, nullable=False)
    new_cases_smoothed_per_million = db.Column(db.Float, nullable=False)
    total_deaths_per_million = db.Column(db.Float, nullable=False)
    new_deaths_per_million = db.Column(db.Float, nullable=False)
    new_deaths_smoothed_per_million = db.Column(db.Float, nullable=True)
    reproduction_rate = db.Column(db.Float, nullable=True)
    icu_patients = db.Column(db.Float, nullable=True)
    icu_patients_per_million = db.Column(db.Float, nullable=True)
    hosp_patients = db.Column(db.Float, nullable=True)
    hosp_patients_per_million = db.Column(db.Float, nullable=True)
    weekly_icu_admissions = db.Column(db.Float, nullable=True)
    weekly_icu_admissions_per_million = db.Column(db.Float, nullable=True)
    weekly_hosp_admissions = db.Column(db.Float, nullable=True)
    weekly_hosp_admissions_per_million = db.Column(db.Float, nullable=True)
    new_tests = db.Column(db.Float, nullable=True)
    total_tests = db.Column(db.Float, nullable=True)
    total_tests_per_thousand = db.Column(db.Float, nullable=True)
    new_tests_per_thousand = db.Column(db.Float, nullable=True)
    new_tests_smoothed = db.Column(db.Float, nullable=True)
    new_tests_smoothed_per_thousand = db.Column(db.Float, nullable=True)
    positive_rate = db.Column(db.Float, nullable=True)
    tests_per_case = db.Column(db.Float, nullable=True)
    tests_units = db.Column(db.String(255), nullable=True)
    total_vaccinations = db.Column(db.Float, nullable=True)
    people_vaccinated = db.Column(db.Float, nullable=True)
    people_fully_vaccinated = db.Column(db.Float, nullable=True)
    new_vaccinations = db.Column(db.Float, nullable=True)
    new_vaccinations_smoothed = db.Column(db.Float, nullable=True)
    total_vaccinations_per_hundred = db.Column(db.Float, nullable=True)
    people_vaccinated_per_hundred = db.Column(db.Float, nullable=True)
    people_fully_vaccinated_per_hundred = db.Column(db.Float, nullable=True)
    new_vaccinations_smoothed_per_million = db.Column(db.Float, nullable=True)
    stringency_index = db.Column(db.Float, nullable=True)

    @classmethod
    def __query_by_location(cls, location: OwidCountry):
        return (
            db.session.query(cls)
            .filter(cls.location_id == location.id)
            .populate_existing()
            .options(
                joinedload(cls.location).joinedload(OwidCountry.location_group),
                joinedload(cls.date_reported),
            )
        )

    @classmethod
    def __query_by_date_reported(cls, date_reported: OwidDateReported):
        return (
            db.session.query(cls)
            .filter(cls.date_reported_id == date_reported.id)
            .populate_existing()
            .options(
                joinedload(cls.location).joinedload(OwidCountry.location_group),
                joinedload(cls.date_reported),
            )
        )

    @classmethod
    def find_by_location(cls, location: OwidCountry):
        return (
            cls.__query_by_location(location)
            .order_by(cls.date_reported.datum.desc())
            .all()
        )

    @classmethod
    def get_by_location(cls, location: OwidCountry, page: int):
        return cls.__query_by_location(location).paginate(page, per_page=items_per_page)

    @classmethod
    def delete_by_location(cls, location: OwidCountry):
        cls.__query_by_location(location).delete()
        db.session.commit()
        return None

    @classmethod
    def find_by_date_reported(cls, date_reported: OwidDateReported):
        return (
            cls.__query_by_date_reported(date_reported)
            .order_by(
                cls.new_deaths_per_million.desc(),
                cls.new_cases_per_million.desc(),
                cls.new_deaths.desc(),
                cls.new_cases.desc(),
            )
            .all()
        )

    @classmethod
    def get_by_date_reported(cls, date_reported: OwidDateReported, page: int):
        return (
            cls.__query_by_date_reported(date_reported)
            .order_by(
                cls.new_deaths_per_million.desc(),
                cls.new_cases_per_million.desc(),
                cls.new_deaths.desc(),
                cls.new_cases.desc(),
            )
            .paginate(page, per_page=items_per_page)
        )

    @classmethod
    def find_by_date_reported_order_by_deaths_new(
        cls, date_reported: OwidDateReported, page: int
    ):
        return (
            cls.__query_by_date_reported(date_reported)
            .order_by(
                cls.new_deaths.desc(),
                cls.new_deaths_per_million.desc(),
                cls.new_cases.desc(),
                cls.new_cases_per_million.desc(),
            )
            .paginate(page, per_page=items_per_page)
        )

    @classmethod
    def find_by_date_reported_order_by_deaths_cumulative(
        cls, date_reported: OwidDateReported, page: int
    ):
        return (
            cls.__query_by_date_reported(date_reported)
            .order_by(
                cls.new_deaths_per_million.desc(),
                cls.new_deaths.desc(),
                cls.new_cases_per_million.desc(),
                cls.new_cases.desc(),
            )
            .paginate(page, per_page=items_per_page)
        )

    @classmethod
    def find_by_date_reported_order_by_cases_new(
        cls, date_reported: OwidDateReported, page: int
    ):
        return (
            cls.__query_by_date_reported(date_reported)
            .order_by(
                cls.new_cases.desc(),
                cls.new_cases_per_million.desc(),
                cls.new_deaths.desc(),
                cls.new_deaths_per_million.desc(),
            )
            .paginate(page, per_page=items_per_page)
        )

    @classmethod
    def find_by_date_reported_order_by_cases_cumulative(
        cls, date_reported: OwidDateReported, page: int
    ):
        return (
            cls.__query_by_date_reported(date_reported)
            .order_by(
                cls.new_cases_per_million.desc(),
                cls.new_cases.desc(),
                cls.new_deaths_per_million.desc(),
                cls.new_deaths.desc(),
            )
            .paginate(page, per_page=items_per_page)
        )

    @classmethod
    def delete_data_for_one_day(cls, date_reported: OwidDateReported):
        for data in cls.find_by_date_reported(date_reported):
            db.session.delete(data)
        db.session.delete(date_reported)
        db.session.commit()


class OwidDataFactory:
    @classmethod
    def create_new(
        cls, oi: OwidImport, date_reported: OwidDateReported, location: OwidCountry
    ):
        o = OwidData(
            date_reported=date_reported,
            location=location,
            total_cases=0.0
            if "" == oi.total_cases or oi.total_cases is None
            else float(oi.total_cases),
            new_cases=0.0
            if "" == oi.new_cases or oi.new_cases is None
            else float(oi.new_cases),
            new_cases_smoothed=0.0
            if "" == oi.new_cases_smoothed or oi.new_cases_smoothed is None
            else float(oi.new_cases_smoothed),
            total_deaths=0.0
            if "" == oi.total_deaths or oi.total_deaths is None
            else float(oi.total_deaths),
            new_deaths=0.0
            if "" == oi.new_deaths or oi.new_deaths is None
            else float(oi.new_deaths),
            new_deaths_smoothed=0.0
            if "" == oi.new_deaths_smoothed or oi.new_deaths_smoothed is None
            else float(oi.new_deaths_smoothed),
            total_cases_per_million=0.0
            if "" == oi.total_cases_per_million or oi.total_cases_per_million is None
            else float(oi.total_cases_per_million),
            new_cases_per_million=0.0
            if "" == oi.new_cases_per_million or oi.new_cases_per_million is None
            else float(oi.new_cases_per_million),
            new_cases_smoothed_per_million=0.0
            if "" == oi.new_cases_smoothed_per_million or oi.new_cases_smoothed_per_million is None
            else float(oi.new_cases_smoothed_per_million),
            total_deaths_per_million=0.0
            if "" == oi.total_deaths_per_million or oi.total_deaths_per_million is None
            else float(oi.total_deaths_per_million),
            new_deaths_per_million=0.0
            if "" == oi.new_deaths_per_million or oi.new_deaths_per_million is None
            else float(oi.new_deaths_per_million),
            new_deaths_smoothed_per_million=0.0
            if "" == oi.new_deaths_smoothed_per_million or oi.new_deaths_smoothed_per_million is None
            else float(oi.new_deaths_smoothed_per_million),
            reproduction_rate=0.0
            if "" == oi.reproduction_rate or oi.reproduction_rate is None
            else float(oi.reproduction_rate),
            icu_patients=0.0
            if "" == oi.icu_patients or oi.icu_patients is None
            else float(oi.icu_patients),
            icu_patients_per_million=0.0
            if "" == oi.icu_patients_per_million or oi.icu_patients_per_million is None
            else float(oi.icu_patients_per_million),
            hosp_patients=0.0
            if "" == oi.hosp_patients or oi.hosp_patients is None
            else float(oi.hosp_patients),
            hosp_patients_per_million=0.0
            if "" == oi.hosp_patients_per_million or oi.hosp_patients_per_million is None
            else float(oi.hosp_patients_per_million),
            weekly_icu_admissions=0.0
            if "" == oi.weekly_icu_admissions or oi.weekly_icu_admissions is None
            else float(oi.weekly_icu_admissions),
            weekly_icu_admissions_per_million=0.0
            if "" == oi.weekly_icu_admissions_per_million or oi.weekly_icu_admissions_per_million is None
            else float(oi.weekly_icu_admissions_per_million),
            weekly_hosp_admissions=0.0
            if "" == oi.weekly_hosp_admissions or oi.weekly_hosp_admissions is None
            else float(oi.weekly_hosp_admissions),
            weekly_hosp_admissions_per_million=0.0
            if "" == oi.weekly_hosp_admissions_per_million or oi.weekly_hosp_admissions_per_million is None
            else float(oi.weekly_hosp_admissions_per_million),
            new_tests=0.0
            if "" == oi.new_tests or oi.new_tests is None
            else float(oi.new_tests),
            total_tests=0.0
            if "" == oi.total_tests or oi.total_tests is None
            else float(oi.total_tests),
            total_tests_per_thousand=0.0
            if "" == oi.total_tests_per_thousand or oi.total_tests_per_thousand is None
            else float(oi.total_tests_per_thousand),
            new_tests_per_thousand=0.0
            if "" == oi.new_tests_per_thousand or oi.new_tests_per_thousand is None
            else float(oi.new_tests_per_thousand),
            new_tests_smoothed=0.0
            if "" == oi.new_tests_smoothed or oi.new_tests_smoothed is None
            else float(oi.new_tests_smoothed),
            new_tests_smoothed_per_thousand=0.0
            if "" == oi.new_tests_smoothed_per_thousand or oi.new_tests_smoothed_per_thousand is None
            else float(oi.new_tests_smoothed_per_thousand),
            positive_rate=0.0
            if "" == oi.positive_rate or oi.positive_rate is None
            else float(oi.positive_rate),
            tests_per_case=0.0
            if "" == oi.tests_per_case or oi.tests_per_case is None
            else float(oi.tests_per_case),
            tests_units=oi.tests_units,
            total_vaccinations=0.0
            if "" == oi.total_vaccinations or oi.total_vaccinations is None
            else float(oi.total_vaccinations),
            people_vaccinated=0.0
            if "" == oi.people_vaccinated or oi.people_vaccinated is None
            else float(oi.people_vaccinated),
            people_fully_vaccinated=0.0
            if "" == oi.people_fully_vaccinated or oi.people_fully_vaccinated is None
            else float(oi.people_fully_vaccinated),
            new_vaccinations=0.0
            if "" == oi.new_vaccinations or oi.new_vaccinations is None
            else float(oi.new_vaccinations),
            new_vaccinations_smoothed=0.0
            if "" == oi.new_vaccinations_smoothed or oi.new_vaccinations_smoothed is None
            else float(oi.new_vaccinations_smoothed),
            total_vaccinations_per_hundred=0.0
            if "" == oi.total_vaccinations_per_hundred or oi.total_vaccinations_per_hundred is None
            else float(oi.total_vaccinations_per_hundred),
            people_vaccinated_per_hundred=0.0
            if "" == oi.people_vaccinated_per_hundred or oi.people_vaccinated_per_hundred is None
            else float(oi.people_vaccinated_per_hundred),
            people_fully_vaccinated_per_hundred=0.0
            if "" == oi.people_fully_vaccinated_per_hundred or oi.people_fully_vaccinated_per_hundred is None
            else float(oi.people_fully_vaccinated_per_hundred),
            new_vaccinations_smoothed_per_million=0.0
            if "" == oi.new_vaccinations_smoothed_per_million or oi.new_vaccinations_smoothed_per_million is None
            else float(oi.new_vaccinations_smoothed_per_million),
            stringency_index=0.0
            if "" == oi.stringency_index or oi.stringency_index is None
            else float(oi.stringency_index),
            processed_update=False,
            processed_full_update=False,
        )
        return o
