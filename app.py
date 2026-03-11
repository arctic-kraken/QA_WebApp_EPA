import flask
from flask import render_template

from db import db

from routes.app_bp import app_bp
from routes.user_bp import user_bp
from routes.account_bp import account_bp
from routes.statement_bp import statement_bp
from routes.budget_bp import budget_bp
from werkzeug.exceptions import NotFound, HTTPException, Forbidden, BadRequest, GatewayTimeout, InternalServerError, Unauthorized
import os

app = flask.Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={os.environ.get('DB_CONNECT_URL')}"
app.secret_key = os.environ.get('SECRET_KEY')

app.app_context().push()

db.init_app(app)
db.create_all()

app.register_blueprint(app_bp)
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(account_bp, url_prefix="/account")
app.register_blueprint(statement_bp, url_prefix="/statement")
app.register_blueprint(budget_bp, url_prefix="/budget")

@app.errorhandler(BadRequest)
def bad_request(e: HTTPException):
    return render_template("Error/BadRequest.html"), 400

@app.errorhandler(Unauthorized)
def unauthorised(e: HTTPException):
    return render_template("Error/Unauthorised.html"), 401

@app.errorhandler(Forbidden)
def forbidden(e: HTTPException):
    return render_template("Error/Forbidden.html"), 403

@app.errorhandler(NotFound)
def page_not_found(e: HTTPException):
    return render_template("Error/NotFound.html"), 404

@app.errorhandler(InternalServerError)
def internal_server_error(e: HTTPException):
    return render_template("Error/InternalServerError.html"), 500

@app.errorhandler(Exception)
def exception_handler(e: Exception):
    return render_template("Error/Internal.html"), 500

@app.errorhandler(GatewayTimeout)
def gateway_timeout(e: HTTPException):
    return render_template("Error/GatewayTimeout.html"), 504

with app.app_context():
    try:
        db.engine.connect()
        print("DB connected")
    except Exception as e:
        print(f"DB connection failed: {e}")



