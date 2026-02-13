import flask
from flask_sqlalchemy import SQLAlchemy
# from flask import render_template
from routes.app_bp import app_bp
from routes.user_bp import user_bp
import os

# https://plainenglish.io/blog/flask-crud-application-using-mvc-architecture
app = flask.Flask(__name__)

# create a .env file with the vars, because it is git ignored
app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={os.getenv('DB_CONNECT_URL')}"
# app.config.from_object('config') # look into this type of config

# db.init_app(app) # look into db migrations
# migrate = Migrate(app, db)

db = SQLAlchemy(app)

with app.app_context():
    try:
        db.engine.connect()
        print("DB connected")
    except Exception as e:
        print(f"DB connection failed: {e}")


app.register_blueprint(app_bp)
app.register_blueprint(user_bp, url_prefix="/user")

# user = db.session.get(User, 1)
# print(f"{user.name} {user.password}")




