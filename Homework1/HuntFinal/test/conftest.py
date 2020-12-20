import pytest
from flask import Flask
from flask.testing import FlaskClient

from action.opt import bp



@pytest.fixture
def client() -> FlaskClient:   
    app = Flask(__name__)
    app.register_blueprint(bp)
    client = app.test_client()
    return client
