import os
import sys

sys.path.insert(
    0, os.path.dirname(os.path.abspath(__file__) + os.sep + "flask_covid19")
)

from flask_covid19.app_web.web_views import app as application
