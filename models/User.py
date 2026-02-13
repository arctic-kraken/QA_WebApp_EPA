from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String(50), nullable=False, unique=True)
    password = db.Column('password', db.Text, nullable=False)