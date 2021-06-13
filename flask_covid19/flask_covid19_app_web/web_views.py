from flask import render_template, redirect, url_for, Blueprint

from flask_covid19_conf.database import app  # , cache

from flask_covid19_app_web.web_model_transient import WebPageContent

from flask_covid19_app_web.user_views import blueprint_app_user
from flask_covid19_app_web.app_admin_views import blueprint_app_admin
from flask_covid19_app_all.all_views import blueprint_app_all

from flask_covid19_data_who.who_views import app_who
from data_owid.owid_views import app_owid
from flask_covid19_app.blueprints.data_ecdc.ecdc_views import app_ecdc
from data_vaccination.vaccination_views import app_vaccination
from data_rki.rki_views import app_rki
from flask_covid19_app.blueprints.data_divi.divi_views import app_divi

blueprint_application = Blueprint('flask_covid19_app_web', __name__, template_folder='templates', url_prefix='/')

app.register_blueprint(blueprint_application, url_prefix='/')

app.register_blueprint(blueprint_app_user, url_prefix='/app/usr')
app.register_blueprint(blueprint_app_admin, url_prefix='/app/admin')
app.register_blueprint(blueprint_app_all, url_prefix='/app/all')

app.register_blueprint(app_who, url_prefix='/who')
app.register_blueprint(app_owid, url_prefix='/owid')
app.register_blueprint(app_ecdc, url_prefix='/ecdc')
app.register_blueprint(app_vaccination, url_prefix='/vaccination')
app.register_blueprint(app_rki, url_prefix='/rki/')
app.register_blueprint(app_divi, url_prefix='/divi')


############################################################################################
#
# WEB
#
@app.route('/home')
def url_home():
    page_info = WebPageContent('Home', "Covid19 Data")
    return render_template(
        'app_application/page_home.html',
        page_info=page_info)


@app.route('/')
def url_root():
    return redirect(url_for('url_home'))


@app.route('/admin')
def url_admin_index():
    page_info = WebPageContent('Admin', "Covid19 Admin")
    return render_template(
        'app_application/index.html',
        page_info=page_info)

