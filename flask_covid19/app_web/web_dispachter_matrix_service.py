from app_config.database import db


from app_web.app_admin_service import AdminService
from app_web.user_service import UserService
from app_web.web_service import WebService
from data_ecdc.ecdc_service import EcdcService
from data_owid.owid_service import OwidService
from data_vaccination.vaccination_service import VaccinationService
from data_who.who_service import WhoService
from data_divi.divi_service import DiviService
from data_rki.rki_service import RkiService
from data_all.all_service import AllDataServiceDispachterMatrix

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
divi_service = DiviService(db)

all_dispachter_matrix_service = AllDataServiceDispachterMatrix(
    who_service=who_service,
    owid_service=owid_service,
    rki_service=rki_service,
    vaccination_service=vaccination_service,
    ecdc_service=ecdc_service,
    divi_service=divi_service)

# db.create_all()
