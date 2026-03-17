from conftest import *
from models.StatementTrx import StatementTrx
from models.Statement import Statement
import os, datetime

def test_import_statement(client, captured_templates):
    login_as(client, 'test_user_basic', 'Testing123$')
    # windows specific path for the file
    # this file contains trxs for february 2026 only
    import_statement(client, f"{os.getcwd()}\\data\\current_acc_trxs.csv", 'test.csv')
    assert len(captured_templates) == 3
    template, context = captured_templates[1]
    assert "messages" in context
    assert len(context['messages']) == 0

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

    import_statement(client, f"{os.getcwd()}\\data\\current_acc_trxs.csv", 'test.csv')
    assert len(captured_templates) == 3
    template, context = captured_templates[1]
    assert "messages" in context
    assert len(context['messages']) == 0

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

    import_statement(client, f"{os.getcwd()}\\data\\current_acc_trxs.csv", 'test.csv')
    assert len(captured_templates) == 3
    template, context = captured_templates[1]
    assert "messages" in context
    assert len(context['messages']) == 0

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
    template, context = captured_templates[9]
    assert "messages" in context
    assert "success" in context["messages"][0].content
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

    import_statement(client, f"{os.getcwd()}\\data\\current_acc_trxs.csv", 'test.csv')
    assert StatementTrx.query.filter_by(statement_id=1).count() == 90
    assert Statement.query.filter_by(id=1).first().money_in_total == 2736.9
    assert Statement.query.filter_by(id=1).first().money_out_total != -2820.76
    assert Statement.query.filter_by(id=1).first().date_newest != datetime.datetime(2026, 2, 23, 10, 22, 54, 0)
    assert len(captured_templates) == 3
    template, context = captured_templates[1]
    assert "messages" in context
    assert len(context['messages']) == 0

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
    template, context = captured_templates[9]
    assert "messages" in context
    assert len(context['messages']) == 0

# TODO test 'get all available dates'
# TODO test 'get latest available date'
# TODO unit tests for Budgets and for Account View (Budget Summaries)
# TODO make unit tests run before waitress serves the website in the dockerfile



