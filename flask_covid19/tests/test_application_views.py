import pytest
from flask_covid19.tests.test_flask_covid19 import client


def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries here so far' in rv.data
