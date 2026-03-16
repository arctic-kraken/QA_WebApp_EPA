from conftest import *
from services.appService import app_service

def test_app(client):
    response = client.get('/')
    assert response.status_code == 200

def test_signup(client, captured_templates):
    client.get('/signup')
    assert app_service.get_current_user_id() is None
    response = client.post(
        '/signup',
        data=dict(username='mytests', password='Testing123$', password_confirmed='Testing123$'),
        follow_redirects=True
    )

    assert response.status_code == 200
    assert app_service.get_current_user_id() is not None
    assert response.request.path == '/account/select'

    client.get('/logout')
    assert app_service.get_current_user_id() is None
    response = client.post(
        '/signup',
        data=dict(username='mytests_select', password='testing', password_confirmed='Testing123$'),
        follow_redirects=True
    )

    assert response.status_code == 200
    assert app_service.get_current_user_id() is None
    assert response.request.path == '/signup'
    assert len(captured_templates) == 4
    template, context = captured_templates[3]
    assert "messages" in context
    assert len(context['messages']) > 0

def test_login(client, captured_templates):
    client.get('/login')
    assert app_service.get_current_user_id() is None
    response = client.post(
        '/login',
        data=dict(username='mytests', password=''),
        follow_redirects=True
    )
