import pytest
from flask import url_for
from unittest import TestCase
from conftest import app, client


class Test(TestCase):
    def __init__(self, client):
        self.client = client
        self.url_admin_tasks = url_for('admin.url_admin_tasks', _external=True)
        self.url_admin_info = url_for('admin.url_admin_info', _external=True)

    def test_run_test_01(self):
        self.assertTrue(True)

    def test_run_test_02(self):
        self.assertTrue(True)

    def test_url_admin_tasks(self):
        assert self.client.get(self.url_admin_tasks).status_code == 200

    def test_url_admin_info(self):
        assert self.client.get(self.url_admin_info).status_code == 200
