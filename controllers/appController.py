# from app import app
from flask import render_template, session, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
from flask import request

from models.User import User
from db import db
from models.UserAccountRole import UserAccountRole
from models.Account import Account
from models.Message import Message
from services.appService import app_service

CONST_ERROR_LOGIN_FAIL = "User does not exist, check your username and password"

def landing():
    if session.get("uid") is not None:
        return redirect(url_for('app_bp.dashboard'))

    return render_template('App/Landing.html')

def login():
    if request.method == 'POST':
        messages = []
        username = request.form['username']
        password = request.form['password']

        user = db.session.execute(db.select(User).filter_by(name=username, password=password)).scalar_one_or_none()
        if user is None:
            messages.append(Message(Message.level.error, CONST_ERROR_LOGIN_FAIL))
            return render_template('App/Login.html', messages=messages)

        app_service.set_current_user_id(user.id)
        user_role = db.session.execute(db.select(UserAccountRole).filter_by(user_id=user.id)).scalar_one_or_none()
        if user_role is None:
            return redirect(url_for('account_bp.select'))

        account = db.session.execute(db.select(Account).filter_by(id=user_role.account_id)).scalar_one_or_none()
        if account is None:
            UserAccountRole.query.filter_by(id=user_role.id).delete()
            db.session.commit()

            return redirect(url_for('account_bp.select'))
            # messages.append(Message(Message.level.error, "Account does not exist"))
            # return render_template('App/Login.html', messages=messages)

        app_service.set_current_account_id(account.id)
        return redirect(url_for('account_bp.view', user=user, account=account))

    return render_template('App/Login.html')

# TODO polish this sucker
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # TODO validate user name is not taken
        db.session.add(User(name=username, password=password))
        db.session.commit()

        user = db.session.execute(db.select(User).filter_by(name=username, password=password)).scalar_one_or_none()

        app_service.set_current_user_id(user.id)
        return redirect(url_for('account_bp.select'))

    return render_template('App/Signup.html')

def logout():
    session.clear()
    return render_template('App/Logout.html')


def dashboard():
    user_id = app_service.get_current_user_id()
    user = db.session.get_one(User, user_id)
    return render_template('App/Dashboard.html', user = user)