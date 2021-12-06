from flask_covid19.app_config.database import app
from flask_covid19.app_config.database import db
from flask_covid19.app_web.app_admin_service import AdminService
from flask_covid19.app_web.user_service import UserService
from flask_covid19.app_web.web_service import WebService
from flask_covid19.data_all.all_service import AllDataServiceDispachterMatrix
from flask_covid19.data_ecdc.ecdc_service import EcdcService
from flask_covid19.data_owid.owid_service import OwidService
from flask_covid19.data_rki.rki_service import RkiService
from flask_covid19.data_vaccination.vaccination_service import VaccinationService
from flask_covid19.data_who.who_service import WhoService

############################################################################################
#
# Services
#
app_admin_service = AdminService(db)
app_user_service = UserService(db)
web_service = WebService(db, app_user_service)

who_service = WhoService(db)
owid_service = OwidService(db)
ecdc_service = EcdcService(db)
vaccination_service = VaccinationService(db)
rki_service = RkiService(db)

all_dispachter_matrix_service = AllDataServiceDispachterMatrix(
    who_service=who_service,
    owid_service=owid_service,
    rki_service=rki_service,
    vaccination_service=vaccination_service,
    ecdc_service=ecdc_service,
)

with app.app_context():
    db.create_all()
