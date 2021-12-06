import pytest

from flask_covid19.app_config.database import Covid19Application


@pytest.fixture
def app():
    """
    HALLO app
    """
    covid19_application = Covid19Application()
    app = covid19_application.app
    app.config['TESTING'] = True
    app.testing = True
    yield app


@pytest.fixture
def client():
    """
    HALLO client
    """
    covid19_application = Covid19Application()
    app = covid19_application.app
    app.config['TESTING'] = True
    app.testing = True
    #yield app
    with app.test_client() as client:
        with app.app_context():
            db = covid19_application.get_db()
        yield client
