from flask_sqlalchemy import SQLAlchemy
from flask import render_template, redirect, url_for, request, abort
from models import User

db = SQLAlchemy()

def create():
    return render_template("userController.html")

def edit():
    return render_template("edit.html")

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