from flask import render_template, abort
from services.appService import app_service
from services.accountService import account_service
from models.Message import Message

def admin_list():
    app_service.check_auth()
    account, user, is_admin = account_service.get_account_user_role_for(app_service.get_current_user_id(), app_service.get_current_account_id())
    if not is_admin:
        abort(401)

    messages = []
    users, errors = account_service.get_all_users_for_account(account.id)
    if users is None:
        messages = Message.from_string_list(Message.level.error, errors)

    return render_template("User/List.html", curr_user=user, user=user, is_admin=is_admin, users=users, invite_code=account.latest_invite_code, messages=messages)