from conftest import *
from models.Budget import Budget
from services.appService import app_service

def test_budget_create_and_update(client, captured_templates):
    login_as(client, 'test_user_basic', 'Testing123$')

    budget_id = create_budget(client)

    update_budget(
        client,
        budget_id,
        "Test Budget Name",
        2137.0,
        '{"clauses":["Tesco", "Top-up by *4787"]}'
    )
    assert len(captured_templates) == 4
    check_last_captured_messages(
        captured_templates,
        ["success"],
        check_len=True
    )

    update_budget(
        client,
        budget_id,
        "Test Budget Name select * from users where 1=1",
        "NaN",
        '{"clauses":["/[]# not a valid string"]}'
    )
    assert len(captured_templates) == 5
    check_last_captured_messages(
        captured_templates,
        [app_service.CONST_REGEX_ERROR_MSG, "Invalid float value"],
        check_len=True
    )

    update_budget(
        client,
        budget_id,
        "Test Budget Name",
        20.0,
        '{"clauses":["/# []]] not a valid string"]}'
    )
    assert len(captured_templates) == 6
    check_last_captured_messages(
        captured_templates,
        [app_service.CONST_REGEX_ERROR_MSG],
        check_len=True
    )

    update_budget(
        client,
        budget_id,
        "Test Budget Name",
        "NaN",
        '{"clauses":["a valid string"]}'
    )
    assert len(captured_templates) == 7
    check_last_captured_messages(
        captured_templates,
        ["Invalid float value"],
        check_len=True
    )

    update_budget(
        client,
        budget_id,
        "Test Budget Name",
        "notanumber",
        '{"clauses":["a valid string"]}'
    )
    assert len(captured_templates) == 8
    check_last_captured_messages(
        captured_templates,
        ["Budget Limit must be a number"],
        check_len=True
    )

def test_delete_budget(client, captured_templates):
    login_as(client, 'test_user_basic', 'Testing123$')

    budget_id = create_budget(client)
    assert Budget.query.filter_by(id=budget_id).count() == 1
    update_budget(
        client,
        budget_id,
        "Test Budget Name",
        20.0,
        '{"clauses":["Tesco"]}'
    )

    import_statement(client, "/data/current_acc_trxs.csv", 'test_feb26.csv')

    response = client.post(
        '/account/view',
        data=dict(year=2026, month=2, recalc=True),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert response.request.path == '/account/view'

    response = client.delete(
        f"/budget/delete/{budget_id}",
        follow_redirects=True
    )
    assert response.status_code == 401
    assert response.request.path == '/budget/delete/1'
    assert Budget.query.filter_by(id=budget_id).count() == 1

    logout(client)
    login_as(client, 'test_user_admin', 'Testing123$')

    response = client.delete(
        '/budget/delete/0',
        follow_redirects=True
    )
    assert response.status_code == 400
    assert response.request.path == '/budget/delete/0'
    assert Budget.query.filter_by(id=budget_id).count() == 1

    response = client.delete(
        f"/budget/delete/{budget_id * -1}",
        follow_redirects=True
    )
    assert response.status_code == 404
    assert response.request.path == f"/budget/delete/{budget_id * -1}"
    assert Budget.query.filter_by(id=budget_id).count() == 1

    response = client.delete(
        f"/budget/delete/{budget_id + 1}",
        follow_redirects=True
    )
    assert response.status_code == 405
    assert response.request.path ==  f"/budget/delete/{budget_id + 1}"
    assert Budget.query.filter_by(id=budget_id).count() == 1

    response = client.delete(
        f"/budget/delete/{budget_id}",
        follow_redirects=True
    )
    assert response.status_code == 204
    assert response.request.path == f"/budget/delete/{budget_id}"
    assert Budget.query.filter_by(id=budget_id).count() == 0

