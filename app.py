import flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
import os

app = flask.Flask(__name__)

# create a .env file with the vars, because it is git ignored
app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={os.getenv('DB_CONNECT_URL')}"
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String(50), nullable=False, unique=True)
    password = db.Column('password', db.Text, nullable=False)

with app.app_context():
    try:
        db.engine.connect()
        print("DB connected")
    except Exception as e:
        print(f"DB connection failed: {e}")

@app.route('/')
def hello_world():
    user = db.session.get(User, 1)

    print(f"{user.name} {user.password}")
    return render_template('App/Landing.html')

@app.route('/Dashboard')
def dashboard():
    return render_template('App/Dashboard.html') # just testing stuff :D

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(50), unique=True, nullable=False)

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

