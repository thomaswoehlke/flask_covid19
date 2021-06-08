import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__) + os.sep  + 'src'))

from flask_covid19.blueprints.app_web.web_views import app as application
