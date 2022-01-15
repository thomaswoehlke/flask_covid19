from project.data.database import app, db
from project.web_admin.app_admin_service import AdminService
from project.web_user.user_service import UserService
from project.web.web.web_service import WebService
from project.data_all.services.all_service import AllServiceDispachterMatrix
from project.data_ecdc.services.ecdc_service import EcdcService
from project.data_owid.services.owid_service import OwidService
from project.data_rki.services.rki_service import RkiService
from project.data_vaccination.services.vaccination_service import VaccinationService
from project.data_who.services.who_service import WhoService
from project.data_all_notifications.notifications_service import NotificationService

#######################################################################################
#
# Services
#
admin_service = AdminService(db)
web_user_service = UserService(db)
web_service = WebService(db, web_user_service)
notification_service = NotificationService(db)

who_service = WhoService(db)
owid_service = OwidService(db)
ecdc_service = EcdcService(db)
vaccination_service = VaccinationService(db)
rki_service = RkiService(db)

all_dispachter_matrix_service = AllServiceDispachterMatrix(
    who_service=who_service,
    owid_service=owid_service,
    rki_service=rki_service,
    vaccination_service=vaccination_service,
    ecdc_service=ecdc_service,
)

with app.app_context():
    db.create_all()
