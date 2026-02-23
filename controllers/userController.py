from db import db
from flask import render_template, session, redirect, url_for, request, abort
from models.User import User
from uuid import uuid4
from services.appService import app_service
from services.accountService import account_service

def create():
    return render_template("userController.html")

def edit():
    user_id = session["uid"]
    return render_template("User/edit.html", user = db.session.get_one(User, user_id))

def admin_list():
    app_service.check_auth()
    account, user, is_admin = account_service.get_account_user_role_for(app_service.get_current_user_id(), app_service.get_current_account_id())
    if not is_admin:
        abort(401)

    # user wants a new invite code
    if request.method == "POST":
        account_service.get_new_invite_code(user.id, account.id)

    db.session.refresh(account)

    return render_template("User/List.html", user=user, is_admin=is_admin, invite_code=account.latest_invite_code)

# class CRUDOperations:
#     def create(self, username, email):
#         item = User(username=username, email=email)
#         db.session.add(item)
#         db.session.commit()
#         return item
#
#     def read(self, item_id):
#         return db.session.get(User, item_id)
#
#     def update(self, item_id, new_username, new_email):
#         item = db.session.get(User, item_id)
#         if item:
#             item.username = new_username
#             item.email = new_email
#             db.session.commit()
#         return item
#
#     def delete(self, item_id):
#         item = db.session.get(User, item_id)
#         if item:
#             db.session.delete(item)
#             db.session.commit()
#         return item