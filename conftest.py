import pytest
from app import create_app
from db import db
from config import test_config
from models.User import User
from flask import template_rendered

@pytest.fixture()
def app():
    app = create_app(config=test_config)
    db.drop_all()
    db.create_all()
    db.session.add(User(
        name='test_user',
        password='5f0244dbfcf71200df884e4addee7c1cab66fd5728659b2a4fe4f10ee5e894ee' # Testing123$ with salt 'test hash'
    ))

    yield app

@pytest.fixture()
def client(app):
    with app.test_client() as client:
        with client.session_transaction() as session:
            # session['uid'] = 1
            yield client

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture()
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

# @pytest.fixture()
# def create_test_user():
#