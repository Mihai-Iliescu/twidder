import unittest
import os
import requests
import tempfile

from app import app, database_helpers
from flask import json


class TestCaseApp(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config["DATABASE"] = tempfile.mkstemp()
        app.config["TESTING"] = True
        self.app = app.test_client()
        database_helpers.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config["DATABASE"])

    def create_user(self, email, password, firstname,
                    familyname, gender, city, country):
        data = json.dumps(dict(
            email=email, password=password, firstname=firstname,
            familyname=familyname, gender=gender, city=city, country=country))
        return self.app.post("/sign_up", data=data,
                             headers={'content-type': 'application/json'})

    def signin(self, email, password):
        return self.app.post("/sign_in", data=json.dumps(dict(
                             email=email, password=password)),
                             headers={'content-type': 'application/json'})

    def test_signup(self):
        res = self.create_user("lkja", "ad", "firstname", "lastname",
                               "gender", "city", "country")
        assert "Account created successfully" in res.data
        res = self.create_user("lkja", "ad", "firstname", "lastname",
                               "gender", "city", "country")
        assert "Email already exists" in res.data

    def test_signin(self):
        res = self.create_user("lkja", "ad", "firstname", "lastname",
                               "gender", "city", "country")
        assert "Account created successfully" in res.data
        res = self.signin("kjs", "erae")
        assert "Username or password invalid" in res.data
        res = self.signin("lkja", "ad")
        assert "Welcome" in res.data

if __name__ == '__main__':
    unittest.main()
