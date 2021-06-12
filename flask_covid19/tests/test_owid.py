import pytest
from flask import url_for
from unittest import TestCase
from conftest import app, client


class Test(TestCase):
    def __init__(self, client):
        self.client = client

    def test_run_test_01(self):
        self.assertTrue(True)

    def test_run_test_02(self):
        self.assertTrue(True)
