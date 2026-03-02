from flask import render_template, session, redirect, url_for, request, abort

from services.accountService import account_service
from services.appService import app_service
from services.budgetService import budget_service

from models.Message import Message

def list():
    app_service.check_auth()
    account, user, is_admin = account_service.get_account_user_role_for(app_service.get_current_user_id(), app_service.get_current_account_id())
    messages = []

    budgets, errors = budget_service.get_budgets_for_account(app_service.get_current_account_id())
    if budgets is None:
        messages = Message.from_string_list(Message.level.error, errors)

    return render_template("Budget/List.html", budgets=budgets, is_admin=is_admin, messages=messages)

def edit(budget_id: int):
    app_service.check_auth()
    if budget_id < 1:
        abort(404)

    account, user, is_admin = account_service.get_account_user_role_for(app_service.get_current_user_id(), app_service.get_current_account_id())
    messages = []

    budget, clauses, errors = budget_service.get(budget_id, app_service.get_current_account_id())
    if budget is None:
        return redirect('/budget/list')

    if request.method == "POST":
        name = request.form["name"]
        limit = request.form["limit"]
        json_clauses = request.form["clauses"]

        result, errors = budget_service.update(budget_id, app_service.get_current_account_id(), name, limit, json_clauses)
        if result is False:
            messages = Message.from_string_list(Message.level.error, errors)
        else:
            messages.append(Message(Message.level.info, "Budget updated successfully"))
            budget, clauses, errors = budget_service.get(budget_id, app_service.get_current_account_id())
            if budget is None:
                messages = Message.from_string_list(Message.level.error, errors)

    return render_template("Budget/Edit.html", budget=budget, clauses=clauses, is_admin=is_admin, messages=messages)

def create():
    app_service.check_auth()

    new_id = budget_service.create(app_service.get_current_account_id())
    if new_id is None:
        abort(500)

    return redirect(url_for("budget_bp.edit", budget_id=new_id))

def delete(budget_id: int):
    app_service.check_auth()
    account, curr_user, is_admin = account_service.get_account_user_role_for(app_service.get_current_user_id(),
                                                                             app_service.get_current_account_id())
    if is_admin is False:
        abort(401)

    if budget_id is None or budget_id < 1:
        abort(400)

    result, errors = budget_service.delete(budget_id, app_service.get_current_account_id())
    if result is False:
        print(errors)
        return errors, 405

    return '', 204

# def delete_trx(trx_id: int):
#     app_service.check_auth()
#     account, curr_user, is_admin = account_service.get_account_user_role_for(app_service.get_current_user_id(),
#                                                                              app_service.get_current_account_id())
#     if is_admin is False:
#         abort(401)
#
#     if trx_id is None or trx_id < 1:
#         abort(400)
#
#     result, errors = statement_service.delete_trx(trx_id, app_service.get_current_account_id())
#     if result is False:
#         print(errors)
#         return errors, 405
#
#     return '', 204

