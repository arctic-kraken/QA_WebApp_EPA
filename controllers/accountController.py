from flask import render_template, get_template_attribute, session, redirect, url_for, request, abort
from services.accountService import account_service
from models.Currency import Currency
from models.Message import Message
from services.appService import app_service
from services.budgetService import budget_service
from services.statementService import statement_service

def create():
    user_id = app_service.get_current_user_id()
    if user_id is None:
        abort(401)

    currencies = Currency.query.all()

    if request.method == "POST":
        name = request.form["account_name"]
        reference = request.form["account_reference"]
        starting_date = request.form["starting_date"]
        starting_balance = request.form["starting_balance"]
        #currency_code = request.form["currency_code"]

        new_acc, errors = account_service.create_account_for(user_id, name, reference, starting_date, starting_balance, "GBP")

        if errors is not None:
            messages = Message.from_string_list(Message.Level.error, errors)
            return render_template("Account/Create.html", currencies=currencies, messages=messages)
        else:
            app_service.set_current_account_id(new_acc.id)
            return redirect("view")

    return render_template("Account/Create.html", currencies=currencies)

def select():
    return render_template("Account/Select.html")

def join():
    if app_service.get_current_user_id() is None:
        abort(401)

    messages = []
    if request.method == "POST":
        invite_code = request.form["invite_code"]
        result, errors, acc_id = account_service.join_user_to_account(app_service.get_current_user_id(), invite_code)
        if errors is not None or acc_id is None:
            messages = Message.from_string_list(Message.Level.error, errors)
        else:
            app_service.set_current_account_id(acc_id)
            return redirect("view")
    return render_template("Account/Join.html", messages=messages)

def view():
    app_service.check_auth()
    account, user, is_admin = account_service.get_account_user_role_for(app_service.get_current_user_id(), app_service.get_current_account_id())
    messages = []
    viewmodel = []
    date_dict = statement_service.get_all_available_dates(app_service.get_current_account_id())

    latest_year, latest_month = statement_service.get_latest_available_date(date_dict)
    if latest_year is None or latest_month is None:
        latest_year = 0
        latest_month = 0

    currency = "GBP"

    selected_year = latest_year
    selected_month = latest_month

    if request.method == "POST":
        year = request.form["year"]
        month = request.form["month"]
        should_recalc = False
        if request.form.get("recalc") is not None:
            should_recalc = bool(request.form["recalc"])

        if should_recalc is True:
            result, errors = budget_service.calc_all_budget_summaries(app_service.get_current_account_id(), month, year)
            if result is False:
                messages = Message.from_string_list(Message.Level.error, errors)

        selected_year = int(year)
        selected_month = int(month)
            # print(errors)

    viewmodel = budget_service.get_budget_summaries_view_models(app_service.get_current_account_id(), selected_month, selected_year)
    month_name = ""
    if latest_month > 0 and latest_year > 0:
        month_name = app_service.get_month_name(selected_month, selected_year)

    return render_template("Account/View.html", viewmodel=viewmodel, currency=currency, month_name=month_name, month=selected_month, year=selected_year, date_dict=date_dict, user=user, account=account, is_admin=is_admin, messages=messages)

def newinvite():
    app_service.check_auth()
    new_code = account_service.get_new_invite_code(app_service.get_current_user_id(), app_service.get_current_account_id())
    if new_code is None:
        abort(401)

    return f"{new_code}"

def revoke(user_id):
    app_service.check_auth()
    account, curr_user, is_admin = account_service.get_account_user_role_for(app_service.get_current_user_id(),
                                                                        app_service.get_current_account_id())
    if is_admin is False:
        abort(401)

    if curr_user.id == user_id:
        return 'Cannot revoke access from yourself', 405

    result, errors = account_service.revoke_access_from(user_id, app_service.get_current_account_id())
    if result is False:
        print(errors)
        return errors, 405

    return '', 204

