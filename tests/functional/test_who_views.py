import pytest


@pytest.mark.usefixtures('live_server')
def test_live_server_start(live_server):
    #live_server.start()
    pass


@pytest.mark.usefixtures('app')
@pytest.mark.usefixtures('client')
def test_url_who_info(app, client):
    response = client.get('/who/info')

    assert response.status_code == 200


@pytest.mark.usefixtures('app')
@pytest.mark.usefixtures('client')
def test_url_who_root(app, client):
    response = client.get('/who/')
    assert response.status_code == 200


@pytest.mark.usefixtures('app')
@pytest.mark.usefixtures('client')
def test_url_root(app, client):
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.usefixtures('live_server')
def test_live_server_stop(live_server):
    #live_server.stop()
    pass
