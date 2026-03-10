from flask import render_template, session, redirect, url_for, abort
from flask import request

from models.User import User
from db import db
from models.UserAccountRole import UserAccountRole
from models.Account import Account
from models.Message import Message
from services.appService import app_service
from services.accountService import account_service
from services.userService import user_service

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

        user = user_service.check_credentials(username, password)
        if user is None:
            messages.append(Message(Message.level.error, CONST_ERROR_LOGIN_FAIL))
            return render_template('App/Login.html', messages=messages)

        app_service.set_current_user_id(user.id)
        # TODO put this in a service
        user_role = db.session.execute(db.select(UserAccountRole).filter_by(user_id=user.id)).scalar_one_or_none()
        if user_role is None:
            return redirect(url_for('account_bp.select'))

        # TODO put this in a service
        account = db.session.execute(db.select(Account).filter_by(id=user_role.account_id)).scalar_one_or_none()
        if account is None:
            UserAccountRole.query.filter_by(id=user_role.id).delete()
            db.session.commit()

            return redirect(url_for('account_bp.select'))

        app_service.set_current_account_id(account.id)
        return redirect("/account/view")

    return render_template('App/Login.html')

# TODO polish this sucker
def signup():
    if app_service.get_current_account_id():
        return redirect('/account/view')

    if app_service.get_current_user_id():
        return redirect('/account/select')

    messages = []

    if request.method == 'POST':
        messages = []
        username = request.form['username']
        password = request.form['password']
        confirmation = request.form['password_confirmed']

        uname_is_good, uname_errors = user_service.validate_user_name(username)
        pwd_is_good, pwd_errors = user_service.validate_password(password, confirmation)
        if uname_is_good is False or pwd_is_good is False:
            messages.extend(Message.from_string_list(Message.level.error, uname_errors))
            messages.extend(Message.from_string_list(Message.level.error, pwd_errors))
            return render_template('App/Signup.html', messages=messages)

        if not user_service.create_user(username, password):
            messages.append(Message(Message.level.error, "Failed to create user"))
            return render_template('App/Signup.html', messages=messages)

        user = user_service.get_user(name=username)
        app_service.set_current_user_id(user.id)

        return redirect(url_for('account_bp.select'))

    if len(messages) == 0:
        messages.append(Message(Message.level.info, "Username must be between 6 and 50 characters long"))
        messages.append(Message(Message.level.info,"Password must contain one or more upper and lower case letter, number and special character (@$!%*#?&)"))
        messages.append(Message(Message.level.info, "Password must be between 6 and 50 characters long"))

    return render_template('App/Signup.html', messages=messages)

def logout():
    session.clear()
    return render_template('App/Logout.html')


def dashboard():
    user_id = app_service.get_current_user_id()
    user = db.session.get_one(User, user_id)
    return render_template('App/Dashboard.html', user = user)