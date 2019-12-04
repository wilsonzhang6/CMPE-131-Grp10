#NOT WORKING

import pytest

from config import Config
from flask import Flask
from app import routes, models

@pytest.fixture
def app():
   app = Flask(__name__)
   return app

@app.route('/')
def index():
    return app.response_class('OK')
'''
def test_example(client):
    response = client.get("/")
    assert response.status_code == 200
'''