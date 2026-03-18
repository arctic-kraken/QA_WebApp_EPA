from conftest import *
from models.Budget import Budget
from models.BudgetSummary import BudgetSummary
from services.accountService import account_service
from services.appService import app_service
from services.budgetService import budget_service
from services.userService import user_service

# most tests in 'test_app.py' use the account service, so there is not much to test left

def test_account_view(client, captured_templates):
    basic_user = user_service.get_user(name="test_user_basic")
    account = account_service.get_account_for(basic_user.id)
    login_as(client, 'test_user_basic', 'Testing123$')

    assert len(captured_templates) == 2
    _, context = captured_templates[1]
    assert context['viewmodel'] == []
    assert context['currency'] == "GBP"
    assert context['month_name'] == ""
    assert context['year'] == 0
    assert context['month'] == 0
    assert context['date_dict'] == dict()
    assert context['is_admin'] == False
    assert context['account'] is not None
    assert context['user'] is not None
    check_last_captured_messages(
        captured_templates
    )

    budget_id = create_budget(client)
    update_budget(
        client,
        budget_id,
        "Test Budget Name",
        2137.0,
        '{"clauses":["Tesco", "Top-up by *4787"]}'
    )

    import_statement(client, "/data/current_acc_trxs.csv", 'test_feb26.csv')
    import_statement(client, "/data/dec_25_statement.csv", 'test_dec25.csv')

    response = client.post(
        '/account/view',
        data=dict(year=2026, month=2, recalc=True),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert response.request.path == '/account/view'

    assert len(captured_templates) == 7
    _, context = captured_templates[6]
    assert len(context['viewmodel']) > 0
    assert context['currency'] == "GBP"
    assert context['month_name'] == "February"
    assert context['year'] == 2026
    assert context['month'] == 2
    assert context['date_dict'] == { 2026: [2], 2025: [12] }
    assert context['is_admin'] == False
    assert context['account'] is not None
    assert context['user'] is not None
    check_last_captured_messages(
        captured_templates
    )

    summary = BudgetSummary.query.filter_by(budget_id=budget_id).first()
    assert summary.account_id == account.id
    assert summary.year == 2026
    assert summary.month_no == 2
    assert summary.total_money_in == 2400
    assert summary.total_money_out == -295.99

    response = client.post(
        '/account/view',
        data=dict(year="notanumber", month="notanumber", recalc=True),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert response.request.path == '/account/view'
    check_last_captured_messages(
        captured_templates,
        ["Failed to calculate", "Date sent is in an incorrect format"],
        check_len=True
    )

    response = client.post(
        '/account/view',
        data=dict(year=2026, month=2, recalc="no bro"),
        follow_redirects=True
    )
    # check that it does not break, it won't calculate
    assert response.status_code == 200
    assert response.request.path == '/account/view'
    check_last_captured_messages(
        captured_templates
    )

