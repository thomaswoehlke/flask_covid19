import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.flask_covid19.blueprints.app_web.web_views import app as application
