import os
import socket

WTF_CSRF_ENABLED = True
DEBUG = True
SECRET_KEY = "vfdjv423ndf654&%%"
CELERY_BROKER_URL = "redis://localhost:6379/0"
MY_CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_CONF_WORKER_SEND_TASK_EVENTS = True
CELERY_CONF_TASK_SEND_SENT_EVENT = True
CELERY_LOG_REDIRECT = "1"
CELERY_LOG_REDIRECT_LEVEL = "INFO"
CACHE_TYPE = "MemcachedCache"
CACHE_MEMCACHED_SERVERS = "127.0.0.1:11211"
CACHE_DEFAULT_TIMEOUT = 50
CACHE_THRESHOLD = 100000
CACHE_KEY_PREFIX = "flask_covid19_"
SQLALCHEMY_ITEMS_PER_PAGE = 10
SQLALCHEMY_TRACK_MODIFICATIONS = True
FLASK_ADMIN_SWATCH = "darkly"
FLASK_APP_DEBUGGER_ACTIVE = True
USER_ADMIN_LOGIN = "admin@admin.de"
USER_ADMIN_USERNAME = "applicationmanager"
USER_ADMIN_PASSWORD = "pbkdf2:sha256:260000$My86CbnkUVk5Lx0y$820c8000566cef5489c2baa8ef1aed4f6216822fd78c29b144a8be12f299002f"
FLASK_RUN_PORT = 9090
FLASK_RUN_HOST = socket.gethostname()
PORT = 9090
HOST = socket.gethostname()
TEST_IMPORT_WHO = False
TEST_IMPORT_RKI = False
TEST_IMPORT_ECDC = False
TEST_IMPORT_OWID = False
TEST_IMPORT_DIVI = False
TEST_IMPORT_WHO_THRESHOLD = 10000
TEST_IMPORT_RKI_THRESHOLD = 100000
TEST_IMPORT_ECDC_THRESHOLD = 10000
TEST_IMPORT_OWID_THRESHOLD = 10000
TEST_IMPORT_DIVI_THRESHOLD = 10000
SQLALCHEMY_DATABASE_USER = "flask_covid19"
SQLALCHEMY_DATABASE_PW = "flask_covid19pwd"
# SQLALCHEMY_DATABASE_TYPE = 'mysql'
SQLALCHEMY_DATABASE_TYPE = "postgresql"
# SQLALCHEMY_DATABASE_TYPE = "mariadb"
# SQLALCHEMY_DATABASE_TYPE = "oracle"
# SQLALCHEMY_DATABASE_HOST = "localhost"
# SQLALCHEMY_DATABASE_HOST = 'tw-thinkpad'
SQLALCHEMY_DATABASE_HOST = 'tw-asus7'
# SQLALCHEMY_DATABASE_HOST = 'tw-asus5'
SQLALCHEMY_DATABASE_DB = "flask_covid19"
# SQLALCHEMY_DATABASE_DB = 'flask_covid19_rki'
# SQLALCHEMY_DATABASE_DB = 'flask_covid19_research'
# SQLALCHEMY_DATABASE_DB = 'flask_covid19_who'
# SQLALCHEMY_DATABASE_DB = 'flask_covid19_owid'
# SQLALCHEMY_DATABASE_DB = 'flask_covid19_frontend'
# SQLALCHEMY_DATABASE_DB = 'flask_covid19_development'
SQLALCHEMY_DATABASE_O_USER = "FLASK_COVID19"
SQLALCHEMY_DATABASE_SID = "flaskcovid19"
BOOTSTRAP_SERVE_LOCAL = True
BOOTSTRAP_USE_CDN = False
BOOTSTRAP_CUSTOM_CSS = True
