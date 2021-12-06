
import pytest

from flask_covid19.app_config.database import Covid19Application


@pytest.fixture
def client():
    my_covid19_application = Covid19Application()
    #db_fd, db_path = tempfile.mkstemp()
    app = my_covid19_application.app

    with app.test_client() as client:
        with app.app_context():
            db = my_covid19_application.create_db()
        yield client

    #os.close(db_fd)
    #os.unlink(db_path)


def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries here so far' in rv.data
