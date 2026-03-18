from conftest import *
from models.StatementTrx import StatementTrx
from models.Statement import Statement
import datetime, time

from services.accountService import account_service
from services.statementService import statement_service
from services.userService import user_service

def test_import_statement(client, captured_templates):
    login_as(client, 'test_user_basic', 'Testing123$')
    # windows specific path for the file
    # this file contains trxs for february 2026 only
    import_statement(client, "/data/current_acc_trxs.csv", 'test.csv')
    assert len(captured_templates) == 3
    check_last_captured_messages(
        captured_templates,
        ["success"]
    )

    response = client.get('/statement/view/1')

    assert response.status_code == 200
    assert response.request.path == '/statement/view/1'

    trxs = StatementTrx.query.filter(StatementTrx.id == 1).all()
    assert len(trxs) > 0

    assert StatementTrx.query.filter(StatementTrx.id == 1).filter_by(money_in=None).count() == 1
    assert StatementTrx.query.filter(StatementTrx.id == 1).filter_by(money_out=None).count() == 0

    for trx in trxs:
        assert trx.description is not None
        assert trx.date is not None
        assert trx.date.strftime("%Y-%m-%d %H:%M:%S")
        assert trx.date.year == 2026
        assert trx.date.month == 2

        if trx.money_in is not None:
            assert round(float(trx.money_in), 2) != 0
        if trx.money_out is not None:
            assert round(float(trx.money_out), 2) != 0

        assert trx.balance is not None

def test_update_statement_name(client, captured_templates):
    login_as(client, 'test_user_basic', 'Testing123$')

    import_statement(client, "/data/current_acc_trxs.csv", 'test.csv')
    assert len(captured_templates) == 3
    check_last_captured_messages(
        captured_templates,
        ["success"]
    )

    response = client.get('/statement/view/1')
    assert response.status_code == 200
    assert response.request.path == '/statement/view/1'

    assert Statement.query.filter_by(name='new test name').first() is None
    response = client.post(
        '/statement/view/1',
        data=dict(name='new test name'),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert response.request.path == '/statement/view/1'
    assert Statement.query.filter_by(name='new test name').first() is not None

def test_delete_statement(client, captured_templates):
    login_as(client, 'test_user_basic', 'Testing123$')

    import_statement(client, "/data/current_acc_trxs.csv", 'test.csv')
    assert len(captured_templates) == 3
    check_last_captured_messages(
        captured_templates,
        ["success"]
    )

    response = client.get(
        '/statement/view/1',
        follow_redirects=True
    )
    assert response.status_code == 200
    assert response.request.path == '/statement/view/1'

    response = client.delete(
        '/statement/view/1',
        follow_redirects=True
    )
    assert response.status_code == 401
    assert response.request.path == '/statement/view/1'
    assert Statement.query.filter_by(id=1).first() is not None

    logout(client)
    login_as(client, 'test_user_admin', 'Testing123$')

    response = client.get(
        '/statement/view/1',
        follow_redirects=True
    )
    assert response.status_code == 200
    assert response.request.path == '/statement/view/1'

    response = client.delete(
        '/statement/view/1',
        follow_redirects=True
    )
    assert response.status_code == 200
    assert response.request.path == '/statement/view/1'
    assert len(captured_templates) == 10
    check_last_captured_messages(
        captured_templates,
        ["success"]
    )
    assert Statement.query.filter_by(id=1).first() is None
    # page should refresh and take back user to the statement list
    response = client.get(
        '/statement/view/1',
        follow_redirects=True
    )
    assert response.status_code == 200
    assert response.request.path == '/statement/list'

def test_delete_statement_trx(client, captured_templates):
    login_as(client, 'test_user_basic', 'Testing123$')

    import_statement(client, "/data/current_acc_trxs.csv", 'test.csv')
    assert StatementTrx.query.filter_by(statement_id=1).count() == 90
    assert Statement.query.filter_by(id=1).first().money_in_total == 2736.9
    assert Statement.query.filter_by(id=1).first().money_out_total != -2820.76
    assert Statement.query.filter_by(id=1).first().date_newest != datetime.datetime(2026, 2, 23, 10, 22, 54, 0)
    assert len(captured_templates) == 3
    check_last_captured_messages(
        captured_templates,
        ["success"]
    )

    response = client.get(
        '/statement/view/1',
        follow_redirects=True
    )
    assert response.status_code == 200
    assert response.request.path == '/statement/view/1'

    response = client.delete(
        '/statement/trx/delete/1',
        follow_redirects=True
    )
    assert response.status_code == 401
    assert response.request.path == '/statement/trx/delete/1'
    assert StatementTrx.query.filter_by(id=1).first() is not None

    logout(client)
    login_as(client, 'test_user_admin', 'Testing123$')

    response = client.get(
        '/statement/view/1',
        follow_redirects=True
    )
    assert response.status_code == 200
    assert response.request.path == '/statement/view/1'

    response = client.delete(
        '/statement/trx/delete/1',
        follow_redirects=True
    )
    assert response.status_code == 204
    assert response.request.path == '/statement/trx/delete/1'

    assert StatementTrx.query.filter_by(statement_id=1).count() == 89
    assert Statement.query.filter_by(id=1).first().money_in_total == 2736.9
    assert Statement.query.filter_by(id=1).first().money_out_total == -2820.76
    assert Statement.query.filter_by(id=1).first().date_newest == datetime.datetime(2026, 2, 23, 10, 22, 54, 0)
    # page should show 'success' message before refresh, showing the 89 trxs
    # cannot test to see 'success' message here as it's added to the page dynamically, via JavaScript
    response = client.get(
        '/statement/view/1',
        follow_redirects=True
    )
    assert response.status_code == 200
    assert response.request.path == '/statement/view/1'
    assert len(captured_templates) == 10
    # check for no messages
    check_last_captured_messages(
        captured_templates
    )

def test_available_dates(client):
    basic_user = user_service.get_user(name="test_user_basic")
    account = account_service.get_account_for(basic_user.id)
    login_as(client, 'test_user_basic', 'Testing123$')

    import_statement(client, "/data/current_acc_trxs.csv", 'test_feb26.csv')
    import_statement(client, "/data/jan26statement.csv", 'test_jan26.csv')
    import_statement(client, "/data/dec_25_statement.csv", 'test_dec25.csv')

    dates = statement_service.get_all_available_dates(account.id)

    assert len(dates) == 2
    keys = dates.keys()
    assert 2025 in keys
    assert len(dates[2025]) == 1
    assert dates[2025][0] == 12

    assert 2026 in keys
    assert len(dates[2026]) == 2
    assert dates[2026][0] == 1
    assert dates[2026][1] == 2

    latest_available_year, latest_available_month = statement_service.get_latest_available_date(dates)

    assert latest_available_year == 2026
    assert latest_available_month == 2




