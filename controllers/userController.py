from db import db
from flask import render_template, redirect, url_for, request, abort
from models.User import User

def create():
    return render_template("userController.html")

def edit(user_id):
    return render_template("User/edit.html", user = db.session.get_one(User, user_id))

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