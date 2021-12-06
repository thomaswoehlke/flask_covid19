from flask import url_for
from tests.test_flask_covid19 import app
from tests.test_flask_covid19 import client


def test_empty_db(client, app):
    """Start with a blank database."""

    rv = client.get("/")
    assert b"<title>404 Not Found</title>" in rv.data
