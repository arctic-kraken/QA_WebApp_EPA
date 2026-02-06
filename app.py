from flask import Flask

app = flask.Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'
