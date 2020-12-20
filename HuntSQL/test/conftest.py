from flask.globals import current_app
import pytest
from flask import Flask
from flask.testing import FlaskClient
from action.opt import bp
from flask import Flask,app





@pytest.fixture

def client() -> FlaskClient:   
    app = Flask(__name__)
    ctx=app.app_context()
    ctx.push()
    app.register_blueprint(bp)
    
    client = app.test_client()
    return client
