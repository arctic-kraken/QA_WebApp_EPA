import pytest, datetime
from app import create_app
from db import db
from config import test_config
from models.Account import Account
from models.User import User
from models.UserAccountRole import UserAccountRole
from services.appService import app_service
from flask import template_rendered

@pytest.fixture()
def app():
    app = create_app(config=test_config)
    db.drop_all()
    db.create_all()
    test_user_admin = User(
        name='test_user_admin',
        password='5f0244dbfcf71200df884e4addee7c1cab66fd5728659b2a4fe4f10ee5e894ee' # Testing123$ with salt 'test hash'
    )
    db.session.add(test_user_admin)
    db.session.commit()
    db.session.refresh(test_user_admin)

    test_user_basic = User(
        name='test_user_basic',
        password='5f0244dbfcf71200df884e4addee7c1cab66fd5728659b2a4fe4f10ee5e894ee' # Testing123$ with salt 'test hash'
    )
    db.session.add(test_user_basic)
    db.session.commit()
    db.session.refresh(test_user_basic)

    account = Account(
        name='test',
        reference='test reference',
        date_created=datetime.datetime.now(),
        currency_code='GBP'
    )
    db.session.add(account)
    db.session.commit()
    db.session.refresh(account)

    role_admin = UserAccountRole(
        user_id=test_user_admin.id,
        account_id=account.id,
        is_admin=True
    )
    db.session.add(role_admin)
    db.session.commit()

    role_basic = UserAccountRole(
        user_id=test_user_basic.id,
        account_id=account.id,
        is_admin=False
    )
    db.session.add(role_basic)
    db.session.commit()

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

def login_as(client, username: str, password: str):
    client.get('/login')
    assert app_service.get_current_user_id() is None
    response = client.post(
        '/login',
        data=dict(username=username, password=password),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert app_service.get_current_user_id() is not None
    assert app_service.get_current_account_id() is not None
    assert response.request.path == '/account/view'

def logout(client):
    client.get('/logout')
    assert app_service.get_current_user_id() is None
    assert app_service.get_current_account_id() is None

def import_statement(client, filepath: str, filename: str):
    with open(filepath, 'rb') as file:
        response = client.post(
            '/statement/list',
            data=dict(file=(file, filename, 'text/csv')),
            follow_redirects=True,
            content_type='multipart/form-data'
        )

    assert response.status_code == 200
    assert response.request.path == '/statement/list'