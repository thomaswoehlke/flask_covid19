import pytest
import socket

from project.app_config.database import Covid19Application
from project.app_config import pytestconfig


@pytest.fixture(scope='session')
def app():
    """
    HALLO app
    """
    covid19_application = Covid19Application(testing=True)
    app = covid19_application.app
    app.config["TESTING"] = True
    app.testing = True
    app.port = app.config["PORT"]
    app.host = socket.gethostname()
    return app


@pytest.fixture(scope='session')
def client():
    """
    HALLO client
    """
    covid19_application = Covid19Application(testing=True)
    app = covid19_application.app
    app.config["TESTING"] = True
    app.testing = True
    app.port = app.config["PORT"]
    app.host = socket.gethostname()
    with app.test_client() as client:
        with app.app_context():
            db = covid19_application.get_db()
        return client
