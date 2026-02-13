# from app import app
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def login():
    return render_template('App/Login.html') # make this

def landing():
    return render_template('App/Landing.html')

def dashboard():
    return render_template('App/Dashboard.html')