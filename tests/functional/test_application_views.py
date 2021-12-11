def test_empty_db(client, app):
    """Start with a blank database."""

    rv = client.get("/")
    assert b"<title>404 Not Found</title>" in rv.data
