from database import app

from flask_covid19.blueprints.data_ecdc.ecdc_service import EcdcService
from flask_covid19.blueprints.data_owid.owid_service import OwidService
from flask_covid19.blueprints.data_vaccination.vaccination_service import VaccinationService
from flask_covid19.blueprints.data_who.who_service import WhoService
from flask_covid19.blueprints.data_divi.divi_service import DiviService
from flask_covid19.blueprints.data_rki.rki_service import RkiService

