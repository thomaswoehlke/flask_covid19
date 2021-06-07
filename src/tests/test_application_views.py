import pytest
from flask import url_for
from unittest import TestCase
from conftest import app, client


class Test(TestCase):
    def __init__(self, client):
        self.client = client
        self.url_home = url_for('application.url_home', _external=True)
        self.url_root = url_for('application.url_root', _external=True)

    def test_run_test_01(self):
        self.assertTrue(True)

    def test_run_test_02(self):
        self.assertTrue(True)

    def test_url_home(self):
        assert self.client.get(self.url_home).status_code == 200

    def test_url_root(self):
        assert self.client.get(self.url_root).status_code == 200
