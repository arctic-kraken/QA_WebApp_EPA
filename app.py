import flask
from flask import render_template
# from flask import Flask

app = flask.Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('App/Landing.html')

@app.route('/Dashboard')
def dashboard():
    return render_template('App/Dashboard.html') # just testing stuff :D
