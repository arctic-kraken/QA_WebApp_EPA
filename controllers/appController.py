# from app import app
from flask import render_template, session, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
from flask import request

from models.User import User
from db import db

CONST_ERROR_LOGIN_FAIL = "User does not exist, check your username and password"

def landing():
    if session.get("uuid") is not None:
        return redirect(url_for('app_bp.dashboard'))

    return render_template('App/Landing.html')

def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.session.execute(db.select(User).filter_by(name=username, password=password)).scalar_one_or_none()
        if user is not None:
            session["uuid"] = user.id
            return redirect(url_for('app_bp.dashboard'))
        else:
            session["errors"] = [CONST_ERROR_LOGIN_FAIL]


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
        session["uuid"] = user.id
        return redirect(url_for('app_bp.dashboard'))

    return render_template('App/Signup.html')

def logout():
    session.clear()
    return render_template('App/Logout.html')


def dashboard():
    user_id = session["uuid"]
    user = db.session.get_one(User, user_id)
    return render_template('App/Dashboard.html', user = user)