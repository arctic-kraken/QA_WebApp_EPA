from conftest import *
from services.appService import app_service
from services.accountService import account_service
from services.userService import user_service

def test_access_to_user_list(client):
    login_as(client, 'test_user_admin', 'Testing123$')

    response = client.get('/user/list')
    assert response.status_code == 200
    assert response.request.path == '/user/list'

    logout(client)
    login_as(client, 'test_user_basic', 'Testing123$')

    response = client.get('/user/list')
    assert response.status_code == 401
    assert response.request.path == '/user/list'

def test_revoke_access(client):
    # revoke_access/int endpoint is triggered from a javascript fetch,
    # it does not return a template, but refreshes the page after successful delete
    admin_user = user_service.get_user(name="test_user_admin")
    basic_user = user_service.get_user(name="test_user_basic")
    account = account_service.get_account_for(admin_user.id)

    users, _ = account_service.get_all_users_for_account(account.id)
    assert len(users) == 2

    login_as(client, 'test_user_basic', 'Testing123$')

    response = client.delete(f"/account/revoke_access/{basic_user.id}")
    assert response.status_code == 401
    users, _ = account_service.get_all_users_for_account(account.id)
    assert len(users) == 2

    logout(client)
    login_as(client, 'test_user_admin', 'Testing123$')

    response = client.delete(f"/account/revoke_access/{admin_user.id}")
    assert response.status_code == 405
    users, _ = account_service.get_all_users_for_account(account.id)
    assert len(users) == 2

    response = client.delete(f"/account/revoke_access/{basic_user.id}")
    assert response.status_code == 204
    users, _ = account_service.get_all_users_for_account(account.id)
    assert len(users) == 1

def test_invite(client, captured_templates):
    admin_user = user_service.get_user(name="test_user_admin")
    basic_user = user_service.get_user(name="test_user_basic")
    # remove basic user from account and invite him again
    UserAccountRole.query.filter_by(user_id=basic_user.id).delete()
    db.session.commit()

    login_as(client, 'test_user_admin', 'Testing123$')

    response = client.get('/account/new_invite')
    assert response.status_code == 200
    logout(client)
    account = account_service.get_account_for(admin_user.id)
    invite_code = account.latest_invite_code

    response = client.post(
        '/login',
        data=dict(username='test_user_basic', password='Testing123$'),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert app_service.get_current_user_id() is not None
    assert app_service.get_current_account_id() is None
    assert response.request.path == '/account/select'

    response = client.post(
        '/account/join',
        data=dict(invite_code='not an invite code'),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert app_service.get_current_user_id() is not None
    assert app_service.get_current_account_id() is None
    assert response.request.path == '/account/join'

    assert len(captured_templates) == 5
    template, context = captured_templates[4]
    assert "messages" in context
    assert len(context['messages']) == 1
    assert "Invalid Invite Code" in context['messages'][0].content

    response = client.post(
        '/account/join',
        data=dict(invite_code=invite_code),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert app_service.get_current_user_id() is not None
    assert app_service.get_current_account_id() is not None
    assert response.request.path == '/account/view'





