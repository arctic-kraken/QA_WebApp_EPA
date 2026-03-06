from db import db
from flask import render_template, session, redirect, url_for, request, abort
from models.User import User
from uuid import uuid4
from services.appService import app_service
from services.accountService import account_service
from models.Message import Message

# TODO either remove this or add some functionality to this page
def edit():
    user_id = app_service.get_current_user_id()
    return render_template("User/edit.html", user = db.session.get_one(User, user_id))

def admin_list():
    app_service.check_auth()
    account, user, is_admin = account_service.get_account_user_role_for(app_service.get_current_user_id(), app_service.get_current_account_id())
    if not is_admin:
        abort(401)

    messages = []
    users, errors = account_service.get_all_users_for_account(account.id)
    if users is None:
        messages = Message.from_string_list(Message.level.error, errors)

    return render_template("User/List.html", curr_user=user, is_admin=is_admin, users=users, invite_code=account.latest_invite_code, messages=messages)