import pytest
from tests.functional.test_flask_covid19 import app
from tests.functional.test_flask_covid19 import client

from project.data_who.model.who_import_pandas import WhoImportPandas


@pytest.mark.usefixtures("live_server")
def test_live_server_start(live_server):
    live_server.start()
    pass


@pytest.mark.usefixtures("live_server")
def test_count(live_server):
    i = WhoImportPandas.count()
    print(str(i))


@pytest.mark.usefixtures("live_server")
def test_count(live_server):
    i = WhoImportPandas.count()
    print(str(i))


@pytest.mark.usefixtures("live_server")
def test_live_server_stop(live_server):
    live_server.stop()
    pass
