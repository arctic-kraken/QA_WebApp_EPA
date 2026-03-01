from db import db
from flask import render_template, session, redirect, url_for, request, abort

from services.accountService import account_service
from services.appService import app_service
from services.statementService import statement_service
from models.Message import Message

def view(statement_id: int):
    app_service.check_auth()
    account, user, is_admin = account_service.get_account_user_role_for(app_service.get_current_user_id(), app_service.get_current_account_id())

    if statement_id is None or statement_id < 1:
        return '', 403

    messages = []
    # currency = account.currency # does not exist yet
    statement, trxs = statement_service.get_statement_with_trxs(statement_id, app_service.get_current_account_id())

    if statement is None:
        return redirect('/statement/list')

    if request.method == 'POST':
        name = request.form["name"]

        if not statement_service.update_statement_name(statement_id, app_service.get_current_account_id(), name):
            messages.append(Message(Message.level.error, "Failed to update statement name"))
        else:
            messages.append(Message(Message.level.info, "Statement name successfully updated"))

    if request.method == 'DELETE':
        if not statement_service.delete_statement(statement_id, app_service.get_current_account_id()):
            messages.append(Message(Message.level.error, "Failed to delete statement"))
        else:
            messages.append(Message(Message.level.info, "Statement successfully deleted"))

    return render_template("Statement/View.html", statement=statement, trxs=trxs, is_admin=is_admin, currency="GBP", messages=messages)

def list():
    app_service.check_auth()
    account, user, is_admin = account_service.get_account_user_role_for(app_service.get_current_user_id(), app_service.get_current_account_id())
    messages = []

    if request.method == 'POST':
        file = request.files.get('file')
        if file is None:
            messages.append(Message(Message.level.warning, "Please choose a file in '.csv' format to upload"))
            return render_template("Statement/List.html", is_admin=is_admin, messages=messages)

        result, error = statement_service.upload_file(file, app_service.get_current_user_id(), app_service.get_current_account_id())
        if result is False:
            messages.append(Message(Message.level.error, error))
        else:
            messages.append(Message(Message.level.info, "File successfully uploaded"))

    statements = statement_service.get_all_statements_for_account(app_service.get_current_account_id())

    return render_template("Statement/List.html", statements=statements, is_admin=is_admin, messages=messages)

def delete_trx(trx_id: int):
    app_service.check_auth()
    account, curr_user, is_admin = account_service.get_account_user_role_for(app_service.get_current_user_id(),
                                                                             app_service.get_current_account_id())
    if is_admin is False:
        abort(401)

    if trx_id is None or trx_id < 1:
        abort(400)

    result, errors = statement_service.delete_trx(trx_id, app_service.get_current_account_id())
    if result is False:
        print(errors)
        return errors, 405

    return '', 204

