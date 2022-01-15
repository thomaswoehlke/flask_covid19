from project.data.database import app, db
from project.data_ecdc.ecdc_views import ecdc_service
from project.data_owid.owid_views import owid_service
from project.data_rki.rki_views import rki_service
from project.data_vaccination.vaccination_views import vaccination_service
from project.data_who.who_views import who_service
from project.web_admin.web_admin_service import WebAdminService
from project.web_user.user_service import WebUserService
from project.web.services.web_service import WebService
from project.data_all.services.all_service_dispachter import AllServiceDispachterMatrix
from project.data_all_notifications.notifications_service import NotificationService

#######################################################################################
#
# Services
#
notification_service = NotificationService(db)
admin_service = WebAdminService(db)
web_user_service = WebUserService(db)
web_service = WebService(db, web_user_service)


web_service_dispachter_matrix = AllServiceDispachterMatrix(
    who_service=who_service,
    owid_service=owid_service,
    rki_service=rki_service,
    vaccination_service=vaccination_service,
    ecdc_service=ecdc_service,
)

with app.app_context():
    db.create_all()
