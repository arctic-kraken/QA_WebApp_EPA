import flask
from db import db
from flask_migrate import Migrate

from routes import budget_bp
from routes.app_bp import app_bp
from routes.user_bp import user_bp
from routes.account_bp import account_bp
from routes.statement_bp import statement_bp
from routes.budget_bp import budget_bp
from werkzeug.exceptions import NotFound, HTTPException
import os

# https://plainenglish.io/blog/flask-crud-application-using-mvc-architecture
app = flask.Flask(__name__)

# create a .env file with the vars, because it is git ignored
app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={os.environ.get('DB_CONNECT_URL')}"
# app.config.from_object('config') # look into this type of config

# app.config['FLASK_DEBUG'] = True
app.secret_key = os.environ.get('SECRET_KEY')
app.app_context().push()
# db = db(app) # apparently does same as line above
db.init_app(app)
db.create_all()
migrate = Migrate(app, db) # CONTINUE TRYING TO DO MIGRATIONS; do the live db upgrade with a production db uri

app.register_blueprint(app_bp)
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(account_bp, url_prefix="/account")
app.register_blueprint(statement_bp, url_prefix="/statement")
app.register_blueprint(budget_bp, url_prefix="/budget")

@app.errorhandler(NotFound)
def page_not_found(e: HTTPException):
    return '', 404

with app.app_context():
    try:
        db.engine.connect()
        print("DB connected")
    except Exception as e:
        print(f"DB connection failed: {e}")

