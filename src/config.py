SECRET_KEY = 'vfdjv423ndf654&%%'
CELERY_BROKER_URL = 'redis://localhost:6379/0'
MY_CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_CONF_WORKER_SEND_TASK_EVENTS = True
CELERY_CONF_TASK_SEND_SENT_EVENT = True
CELERY_LOG_REDIRECT = '1'
CELERY_LOG_REDIRECT_LEVEL = 'INFO'
SQLALCHEMY_DATABASE_USER = 'flask_covid19'
SQLALCHEMY_DATABASE_PW = 'flask_covid19pwd'
CACHE_TYPE = 'MemcachedCache'
CACHE_MEMCACHED_SERVERS = '127.0.0.1:11211'
CACHE_DEFAULT_TIMEOUT = 50
CACHE_THRESHOLD = 100000
CACHE_KEY_PREFIX = 'flask_covid19_'
SQLALCHEMY_ITEMS_PER_PAGE = 10
SQLALCHEMY_TRACK_MODIFICATIONS = True
FLASK_ADMIN_SWATCH = 'superhero'
FLASK_APP_DEBUGGER_ACTIVE = True
USER_ADMIN_LOGIN = 'admin@admin.de'
USER_ADMIN_USERNAME = 'admin'
USER_ADMIN_PASSWORD = 'pbkdf2:sha256:150000$O4SZaWF5$85ad348809215aa7fe0a16f79dc61228e7d0fb214c24df68b0745f1570ffc148'
PORT = 9090
TEST_IMPORT_WHO = False
TEST_IMPORT_RKI = False
TEST_IMPORT_ECDC = False
TEST_IMPORT_OWID = False
TEST_IMPORT_DIVI = False
TEST_IMPORT_WHO_THRESHOLD = 40000
TEST_IMPORT_RKI_THRESHOLD = 40000
TEST_IMPORT_ECDC_THRESHOLD = 40000
TEST_IMPORT_OWID_THRESHOLD = 40000
TEST_IMPORT_DIVI_THRESHOLD = 40000
# SQLALCHEMY_DATABASE_TYPE = 'mysql'
# SQLALCHEMY_DATABASE_TYPE = 'postgresql'
SQLALCHEMY_DATABASE_TYPE = 'mariadb'
# SQLALCHEMY_DATABASE_HOST = 'localhost'
# SQLALCHEMY_DATABASE_HOST = 'tw-thinkpad'
SQLALCHEMY_DATABASE_HOST = 'tw-asus7'
SQLALCHEMY_DATABASE_DB = 'flask_covid19_rki'
# SQLALCHEMY_DATABASE_DB = 'flask_covid19_who'
# SQLALCHEMY_DATABASE_DB = 'flask_covid19_owid'
# SQLALCHEMY_DATABASE_DB = 'flask_covid19_frontend'
# SQLALCHEMY_DATABASE_DB = 'flask_covid19_development'
# SQLALCHEMY_DATABASE_DB = 'flask_covid19'
