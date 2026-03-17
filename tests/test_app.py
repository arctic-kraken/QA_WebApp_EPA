from conftest import *
from services.appService import app_service
from controllers.appController import CONST_ERROR_LOGIN_FAIL
from models.Message import Message

def test_app(client):
    response = client.get('/')
    assert response.status_code == 200

def test_signup(client, captured_templates):
    client.get('/signup')
    assert app_service.get_current_user_id() is None
    # Forbidden chars,
    # not matching passwords,
    # password must contain 1 Upper and lower case char, a number and a special char
    response = client.post(
        '/signup',
        data=dict(username='mytests_ ]', password='testing', password_confirmed='Testing123$'),
        follow_redirects=True
    )

    assert response.status_code == 200
    assert app_service.get_current_user_id() is None
    assert response.request.path == '/signup'
    assert len(captured_templates) == 2
    template, context = captured_templates[1]
    assert "messages" in context
    assert len(context['messages']) == 3
    assert context["messages"][0].level == Message.level.error
    assert context["messages"][1].level == Message.level.error
    assert context["messages"][2].level == Message.level.error

    # Try signing up and creating an account
    response = client.get('/signup')
    assert response.status_code == 200
    assert app_service.get_current_user_id() is None
    assert response.request.path == '/signup'
    assert len(captured_templates) == 3
    template, context = captured_templates[2]
    assert "messages" in context
    assert context["messages"][0].level == Message.level.info
    assert context["messages"][1].level == Message.level.info
    assert context["messages"][2].level == Message.level.info

    response = client.post(
        '/signup',
        data=dict(username='mytests', password='Testing123$', password_confirmed='Testing123$'),
        follow_redirects=True
    )

    assert response.status_code == 200
    assert app_service.get_current_user_id() is not None
    assert response.request.path == '/account/select'

    response = client.get('/account/create')
    assert response.status_code == 200
    assert app_service.get_current_user_id() is not None
    assert app_service.get_current_account_id() is None
    assert response.request.path == '/account/create'

    # we've tested forbidden char validation already,
    # no need to test again as they're the same function,
    # proceed with account creation
    response = client.post(
        '/account/create',
        data=dict(account_name='testing', account_reference='my testing account'),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert app_service.get_current_user_id() is not None
    assert app_service.get_current_account_id() is not None
    assert response.request.path == '/account/view'

def test_login(client, captured_templates):
    client.get('/login')
    assert app_service.get_current_user_id() is None
    response = client.post(
        '/login',
        data=dict(username='test_user_admin', password='Testing123$'),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert app_service.get_current_user_id() is not None
    assert app_service.get_current_account_id() is not None
    assert response.request.path == '/account/view'

    client.get('/logout')
    assert app_service.get_current_user_id() is None
    assert app_service.get_current_account_id() is None

    response = client.post(
        '/login', # forbidden chars
        data=dict(username='test_user[]{{}}; select * from Users where 1=1; then read a book and watch some netflix.', password='Testing123$'),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert app_service.get_current_user_id() is None
    assert app_service.get_current_account_id() is None
    assert response.request.path == '/login'
    assert len(captured_templates) == 4
    template, context = captured_templates[3]
    assert "messages" in context
    assert len(context['messages']) == 1
    assert app_service.CONST_REGEX_ERROR_MSG in context['messages'][0].content

    client.get('/logout')
    assert app_service.get_current_user_id() is None
    assert app_service.get_current_account_id() is None

    response = client.post(
        '/login',  # user does not exist
        data=dict(username='test_user', password='Testing123$'),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert app_service.get_current_user_id() is None
    assert app_service.get_current_account_id() is None
    assert response.request.path == '/login'
    assert len(captured_templates) == 6
    template, context = captured_templates[5]
    assert "messages" in context
    assert len(context['messages']) == 1
    assert CONST_ERROR_LOGIN_FAIL in context['messages'][0].content

def test_encryption(client):
    text = 'Testing123$'
    encrypted_text = app_service.encrypt(text)
    # with salt 'test hash'
    assert encrypted_text == '5f0244dbfcf71200df884e4addee7c1cab66fd5728659b2a4fe4f10ee5e894ee'


